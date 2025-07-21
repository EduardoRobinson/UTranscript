package com.example.UTranscriptBack.controllers;

import org.springframework.http.HttpHeaders;

import org.springframework.http.MediaType;

import java.io.File;
import java.util.List;
import java.util.Map;
import java.util.Optional;

import org.apache.tomcat.util.net.openssl.ciphers.Authentication;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.FileSystemResource;
import org.springframework.http.ContentDisposition;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.client.MultipartBodyBuilder;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestPart;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;

import com.example.UTranscriptBack.dto.VideoAulaDTO;
import com.example.UTranscriptBack.dto.YoutubeRequestDTO;
import com.example.UTranscriptBack.models.CursoModel;
import com.example.UTranscriptBack.models.StatusTranscriptionModel;
import com.example.UTranscriptBack.models.TemaModel;
import com.example.UTranscriptBack.models.TranscriptionModel;
import com.example.UTranscriptBack.models.UniversidadeModel;
import com.example.UTranscriptBack.models.UserModel;
import com.example.UTranscriptBack.models.VideoAulaModel;
import com.example.UTranscriptBack.repositories.StatusTranscriptionRepository;
import com.example.UTranscriptBack.repositories.UserRepository;
import com.example.UTranscriptBack.services.CursoService;
import com.example.UTranscriptBack.services.JwtService;
import com.example.UTranscriptBack.services.TemaService;
import com.example.UTranscriptBack.services.TranscriptionService;
import com.example.UTranscriptBack.services.UniversidadeService;
import com.example.UTranscriptBack.services.VideoAulaService;
import java.util.concurrent.ExecutorService;

import io.jsonwebtoken.io.IOException;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.web.bind.annotation.PutMapping;

@RestController
public class UTranscriptController {

    private final String FASTAPI_URL = "http://127.0.0.1:8000/youtube_download";

    private final VideoAulaService service;

    private final ExecutorService executorService = java.util.concurrent.Executors.newSingleThreadExecutor();

    private TemaService temaService;

    private CursoService cursoService;

    private UniversidadeService universidadeService;

    private TranscriptionService transcriptionService;

    private StatusTranscriptionRepository statusTranscriptionRepository;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private HttpServletRequest request;

    @Autowired
    private JwtService jwtService;

    public UTranscriptController(VideoAulaService service, TemaService temaService, CursoService cursoService,
            UniversidadeService universidadeService, TranscriptionService transcriptionService,
            StatusTranscriptionRepository statusTranscriptionRepository) {
        this.service = service;
        this.temaService = temaService;
        this.cursoService = cursoService;
        this.universidadeService = universidadeService;
        this.transcriptionService = transcriptionService;
        this.statusTranscriptionRepository = statusTranscriptionRepository;
    }

    @GetMapping("/health")
    public String health(Authentication authentication) {
        return "OK";
    }

    @PostMapping("/youtube_download")
    public ResponseEntity<byte[]> baixarYoutube(@RequestBody YoutubeRequestDTO dto, Authentication authentication) {
        RestTemplate restTemplate = new RestTemplate();

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        HttpEntity<YoutubeRequestDTO> request = new HttpEntity<>(dto, headers);

        try {
            ResponseEntity<byte[]> response = restTemplate.exchange(
                    FASTAPI_URL,
                    HttpMethod.POST,
                    request,
                    byte[].class);

            HttpHeaders responseHeaders = new HttpHeaders();
            responseHeaders.setContentType(MediaType.APPLICATION_OCTET_STREAM);
            responseHeaders.setContentDisposition(
                    ContentDisposition.attachment().filename("video.mp4").build());

            return new ResponseEntity<>(response.getBody(), responseHeaders, HttpStatus.OK);

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.BAD_GATEWAY)
                    .body(("Erro ao conectar com FastAPI: " + e.getMessage()).getBytes());
        }
    }

    @PostMapping("/video-aula")
    public ResponseEntity<VideoAulaModel> criar(@RequestPart("dados") VideoAulaDTO dto,
            @RequestPart("file") MultipartFile file, Authentication authentication) throws java.io.IOException {
        String token = request.getHeader("Authorization");

        String jwt = token.substring(7);
        String email = jwtService.extrairEmail(jwt);
        Optional<UserModel> userOptional = userRepository.findByEmail(email);
        if (!userOptional.isPresent()) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }
        UserModel user = userOptional.get();
        VideoAulaModel v = service.create(dto, user);

        TranscriptionModel transcription = new TranscriptionModel();
        transcription.setVideoAula(v);
        transcription.setConteudo("");
        Optional<StatusTranscriptionModel> statusOptional = statusTranscriptionRepository.findByDescricao("Pendente");
        if (!statusOptional.isPresent()) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }
        StatusTranscriptionModel status = statusOptional.get();
        transcription.setStatus(status);
        transcription = transcriptionService.create(transcription);

        // 👇 Salva o arquivo temporário AQUI, enquanto o MultipartFile ainda é válido
        File tempFile;
        try {
            tempFile = File.createTempFile("upload-", ".tmp");
            file.transferTo(tempFile);
        } catch (IOException e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }

        final Long transcriptionId = transcription.getId();
        final File finalTempFile = tempFile;

        executorService.submit(() -> {
            try {
                String cleanToken = token.replace("Bearer ", "");
                System.out.println("🔑 Token limpo enviado pro FastAPI: " + cleanToken);
                enviarArquivoParaFastAPI(transcriptionId, finalTempFile, cleanToken);
            } catch (Exception e) {
                e.printStackTrace();
            } finally {
                finalTempFile.delete(); // limpa o lixo
            }
        });

        return ResponseEntity.ok(v);
    }

    @GetMapping("/cursos")
    public List<CursoModel> cursos(Authentication authentication) {
        return cursoService.findAll();
    }

    @GetMapping("/temas/{id}")
    public List<TemaModel> getTemasPorCurso(@PathVariable Long id, Authentication authentication) {
        return temaService.findByCursoId(id);
    }

    @GetMapping("/universidades")
    public List<UniversidadeModel> universidades(Authentication authentication) {
        return universidadeService.findAll();
    }

    @GetMapping("/video-aulas")
    public List<VideoAulaModel> videoAulas(Authentication authentication) {
        return service.findAll();
    }

    @GetMapping("/video-aulas/user")
    public List<VideoAulaModel> videoAulasPorUsuario(Authentication authentication) {
        String token = request.getHeader("Authorization");

        String jwt = token.substring(7);
        String email = jwtService.extrairEmail(jwt);
        Optional<UserModel> userOptional = userRepository.findByEmail(email);
        if (!userOptional.isPresent()) {
            return List.of(); // Retorna uma lista vazia se o usuário não for encontrado
        }
        UserModel user = userOptional.get();
        return service.findAll().stream()
                .filter(videoAula -> videoAula.getUsuario().getId().equals(user.getId()))
                .toList();

    }

    @GetMapping("/video-aula/{id}")
    public VideoAulaModel videoAulaPorId(@PathVariable Long id, Authentication authentication) {
        return service.findById(id);
    }

    @PostMapping("/video-aula/pdf")
    public ResponseEntity<byte[]> exportarParaPDF(@RequestBody VideoAulaModel videoAula, Authentication auth) {
        RestTemplate restTemplate = new RestTemplate();
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        HttpEntity<VideoAulaModel> request = new HttpEntity<>(videoAula, headers);

        ResponseEntity<byte[]> response = restTemplate
                .postForEntity("http://127.0.0.1:8000/videoAula_pdf", request, byte[].class);

        HttpHeaders responseHeaders = new HttpHeaders();
        responseHeaders.setContentType(MediaType.APPLICATION_PDF);
        responseHeaders.setContentDisposition(ContentDisposition.attachment().filename("transcricao.pdf").build());

        return new ResponseEntity<>(response.getBody(), responseHeaders, HttpStatus.OK);
    }

    @DeleteMapping("/video-aula/{id}")
    public ResponseEntity<Void> deletarVideoAula(@PathVariable Long id, Authentication authentication) {
        VideoAulaModel videoAula = service.findById(id);
        if (videoAula == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }
        service.delete(videoAula);
        return ResponseEntity.noContent().build();
    }

    @PutMapping("/transcription/{id}")
    public ResponseEntity<TranscriptionModel> atualizarTranscricao(
            @PathVariable String id,
            @RequestBody Map<String, String> payload) throws java.io.IOException {

        String conteudo = payload.get("resumo"); // pega o campo "resumo" do JSON
        if (conteudo == null || conteudo.isEmpty()) {
            TranscriptionModel transcription = transcriptionService.findById(Long.parseLong(id));
            transcription.setConteudo("Erro ao processar a transcrição: conteúdo vazio");
            transcription.setStatus(statusTranscriptionRepository.findByDescricao("Cancelado").orElse(null));
            transcription = transcriptionService.update(transcription);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(transcription);
        }
        TranscriptionModel transcription = transcriptionService.findById(Long.parseLong(id));
        transcription.setStatus(statusTranscriptionRepository.findByDescricao("Concluído").orElse(null));
        transcription.setConteudo(conteudo);
        transcription = transcriptionService.update(transcription);

        if (transcription == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }
        return ResponseEntity.ok(transcription);
    }

    private void enviarArquivoParaFastAPI(Long transcriptionId, File file, String token) throws IOException {

        System.out.println("Enviando arquivo para FastAPI...");
        WebClient webClient = WebClient.builder().baseUrl("http://127.0.0.1:8000").defaultHeader("Authorization", token)
                .build();

        // Convert MultipartFile to a temporary File
        try {
            MultipartBodyBuilder builder = new MultipartBodyBuilder();
            builder.part("file", new FileSystemResource(file));
            TranscriptionModel transcriptionUpdate = transcriptionService.findById(transcriptionId);
            transcriptionUpdate.setStatus(statusTranscriptionRepository.findByDescricao("Em Andamento").orElse(null));
            transcriptionService.update(transcriptionUpdate);
            webClient.post()
                    .uri("/transcricao/" + transcriptionId)
                    .contentType(MediaType.MULTIPART_FORM_DATA)
                    .body(BodyInserters.fromMultipartData(builder.build()))
                    .retrieve()
                    .bodyToMono(String.class)
                    .block();

        } catch (Exception e) {
            TranscriptionModel transcriptionUpdate = transcriptionService.findById(transcriptionId);
            transcriptionUpdate.setConteudo("Erro ao enviar o arquivo para FastAPI");
            transcriptionUpdate.setStatus(statusTranscriptionRepository.findByDescricao("Cancelado").orElse(null));
            transcriptionService.update(transcriptionUpdate);
            System.err.println("Erro ao enviar arquivo para FastAPI: " + e.getMessage());
            throw new IOException("Erro ao enviar arquivo para FastAPI", e);
        }
    }

}
