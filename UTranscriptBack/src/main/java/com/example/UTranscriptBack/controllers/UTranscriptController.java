package com.example.UTranscriptBack.controllers;

import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;

import java.io.File;
import java.io.IOException;
import java.time.Duration;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ExecutorService;

// 👇 IMPORT CORRIGIDO PARA O SPRING SECURITY
import org.springframework.security.core.Authentication; 
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.FileSystemResource;
import org.springframework.http.ContentDisposition;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.client.MultipartBodyBuilder;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestPart;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

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

import jakarta.servlet.http.HttpServletRequest;

@RestController
public class UTranscriptController {

    private final String FASTAPI_URL = System.getenv("FASTAPI_URL");
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
        UserModel user = (UserModel) authentication.getPrincipal();
        if (!UserModel.class.isInstance(user)) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
        
        RestTemplate restTemplate = new RestTemplate();
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        HttpEntity<YoutubeRequestDTO> requestEntity = new HttpEntity<>(dto, headers);
        System.out.println("Enviando requisição para FastAPI com URL: "+ FASTAPI_URL);
        
        try {
            ResponseEntity<byte[]> response = restTemplate.exchange(
                    FASTAPI_URL.concat("/youtube_download"),
                    HttpMethod.POST,
                    requestEntity,
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
            @RequestPart("file") MultipartFile file, Authentication authentication) {
                
        UserModel user = (UserModel) authentication.getPrincipal();
        if (!UserModel.class.isInstance(user)) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }

        VideoAulaModel v = service.create(dto, user);
        
        String promptPersonalizado = dto.promptPersonalizado == null ? null : dto.promptPersonalizado.trim();
        boolean extracaoPersonalizada = promptPersonalizado != null && !promptPersonalizado.isEmpty();

        TranscriptionModel transcription = new TranscriptionModel();
        transcription.setVideoAula(v);
        transcription.setConteudo("");
        transcription.setTipoExtracao(extracaoPersonalizada ? "PERSONALIZADO" : "COMUM");
        if (extracaoPersonalizada) {
            transcription.setPromptPersonalizado(promptPersonalizado);
        }
        
        Optional<StatusTranscriptionModel> statusOptional = statusTranscriptionRepository.findByDescricao("Pendente");
        if (!statusOptional.isPresent()) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }
        
        StatusTranscriptionModel status = statusOptional.get();
        transcription.setStatus(status);
        transcription = transcriptionService.create(transcription);

        File tempFile;
        try {
            tempFile = File.createTempFile("upload-", ".tmp");
            file.transferTo(tempFile);
        } catch (IOException e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }

        // 👇 Pegamos o token de dentro dos Cookies
        String tokenFromCookie = "";
        if (request.getCookies() != null) {
            for (jakarta.servlet.http.Cookie cookie : request.getCookies()) {
                if ("token".equals(cookie.getName())) {
                    tokenFromCookie = cookie.getValue();
                    break;
                }
            }
        }

        final Long transcriptionId = transcription.getId();
        final File finalTempFile = tempFile;
        final String finalToken = tokenFromCookie; // Token extraído do cookie para enviar ao FastAPI
        final String promptParaExtracao = extracaoPersonalizada ? promptPersonalizado : null;

        executorService.submit(() -> {
            try {
                // Envia como Bearer token para o FastAPI, se ele exigir
                enviarArquivoParaFastAPI(transcriptionId, finalTempFile, "Bearer " + finalToken, promptParaExtracao);
            } catch (Exception e) {
                e.printStackTrace();
            } finally {
                finalTempFile.delete(); 
            }
        });

        return ResponseEntity.ok(v);
    }

    // 👇 Todas as rotas de GET agora retornam ResponseEntity<List<T>> para poder devolver 401
    @GetMapping("/cursos")
    public ResponseEntity<List<CursoModel>> cursos(Authentication authentication) {
        UserModel user = (UserModel) authentication.getPrincipal();
        if (!UserModel.class.isInstance(user)) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
        return ResponseEntity.ok(cursoService.findAll());
    }

    @GetMapping("/temas/{id}")
    public ResponseEntity<List<TemaModel>> getTemasPorCurso(@PathVariable Long id, Authentication authentication) {
        UserModel user = (UserModel) authentication.getPrincipal();
        if (!UserModel.class.isInstance(user)) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
        return ResponseEntity.ok(temaService.findByCursoId(id));
    }

    @GetMapping("/universidades")
    public ResponseEntity<List<UniversidadeModel>> universidades(Authentication authentication) {
        UserModel user = (UserModel) authentication.getPrincipal();
        if (!UserModel.class.isInstance(user)) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
        return ResponseEntity.ok(universidadeService.findAll());
    }

    @GetMapping("/video-aulas")
    public ResponseEntity<List<VideoAulaModel>> videoAulas(Authentication authentication) {
        UserModel user = (UserModel) authentication.getPrincipal();
        if (!UserModel.class.isInstance(user)) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
        return ResponseEntity.ok(service.findAll());
    }

    // 👇 Rota arrumada (variáveis duplicadas foram removidas)
    @GetMapping("/video-aulas/user")
    public ResponseEntity<List<VideoAulaModel>> videoAulasPorUsuario(Authentication authentication) {
        UserModel user = (UserModel) authentication.getPrincipal();
        if (!UserModel.class.isInstance(user)) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
        
        List<VideoAulaModel> aulas = service.findAll().stream()
                .filter(videoAula -> videoAula.getUsuario().getId().equals(user.getId()))
                .toList();
                
        return ResponseEntity.ok(aulas);
    }

    @GetMapping("/video-aula/{id}")
    public ResponseEntity<VideoAulaModel> videoAulaPorId(@PathVariable Long id, Authentication authentication) {
        UserModel user = (UserModel) authentication.getPrincipal();
        if (!UserModel.class.isInstance(user)) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
        return ResponseEntity.ok(service.findById(id));
    }

    @PostMapping("/video-aula/pdf")
    public ResponseEntity<byte[]> exportarParaPDF(@RequestBody VideoAulaModel videoAula, Authentication auth) {
        UserModel user = (UserModel) auth.getPrincipal();
        if (!UserModel.class.isInstance(user)) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
        
        RestTemplate restTemplate = new RestTemplate();
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        HttpEntity<VideoAulaModel> requestEntity = new HttpEntity<>(videoAula, headers);

        ResponseEntity<byte[]> response = restTemplate
                .postForEntity(FASTAPI_URL.concat("/videoAula_pdf"), requestEntity, byte[].class);

        HttpHeaders responseHeaders = new HttpHeaders();
        responseHeaders.setContentType(MediaType.APPLICATION_PDF);
        responseHeaders.setContentDisposition(ContentDisposition.attachment().filename("transcricao.pdf").build());

        return new ResponseEntity<>(response.getBody(), responseHeaders, HttpStatus.OK);
    }

    @PostMapping("/video-aula/{id}/avaliar")
    public ResponseEntity<?> avaliarVideoAula(@PathVariable Long id, Authentication authentication) {
        UserModel user = (UserModel) authentication.getPrincipal();
        if (!UserModel.class.isInstance(user)) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }

        VideoAulaModel videoAula;
        try {
            videoAula = service.findById(id);
        } catch (RuntimeException e) {
            return ResponseEntity.notFound().build();
        }

        TranscriptionModel transcription = videoAula.getTranscricoes();
        if (transcription == null) {
            return ResponseEntity.badRequest().body(Map.of("erro", "A videoaula não possui transcrição."));
        }

        String status = transcription.getStatus() != null ? transcription.getStatus().getDescricao() : null;
        if (!"Concluído".equals(status)
                || transcription.getPrompt() == null || transcription.getPrompt().isBlank()
                || transcription.getConteudo() == null || transcription.getConteudo().isBlank()) {
            return ResponseEntity.badRequest().body(Map.of(
                    "erro", "A transcrição precisa estar concluída, com prompt e conteúdo."));
        }

        transcription.setStatusAvaliacao("Em Andamento");
        transcription.setAvaliacao(null);
        transcriptionService.update(transcription);

        String tokenFromCookie = "";
        if (request.getCookies() != null) {
            for (jakarta.servlet.http.Cookie cookie : request.getCookies()) {
                if ("token".equals(cookie.getName())) {
                    tokenFromCookie = cookie.getValue();
                    break;
                }
            }
        }

        final Long transcriptionId = transcription.getId();
        final String token = tokenFromCookie;
        final String prompt = transcription.getPrompt();
        final String resultado = transcription.getConteudo();

        executorService.submit(() -> enviarAvaliacaoParaFastAPI(transcriptionId, token, prompt, resultado));

        return ResponseEntity.ok(Map.of("msg", "Avaliação em andamento", "id", id));
    }

    private void enviarAvaliacaoParaFastAPI(Long transcriptionId, String token, String prompt, String resultado) {
        Map<String, Object> corpo = Map.of(
                "aderencia", List.of(Map.of(
                        "prompt", prompt,
                        "resultado", resultado)));

        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
        factory.setConnectTimeout(Duration.ofSeconds(10));
        factory.setReadTimeout(Duration.ofSeconds(30));

        RestTemplate restTemplate = new RestTemplate(factory);
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        headers.setBearerAuth(token);
        HttpEntity<Map<String, Object>> requestEntity = new HttpEntity<>(corpo, headers);

        try {
            restTemplate.postForEntity(
                    FASTAPI_URL.concat("/avaliar/" + transcriptionId), requestEntity, Map.class);
        } catch (Exception e) {
            TranscriptionModel transcription = transcriptionService.findById(transcriptionId);
            if (transcription == null) {
                return;
            }
            transcription.setStatusAvaliacao("Erro");
            transcription.setAvaliacao("Falha ao enviar a avaliação: " + e.getMessage());
            transcriptionService.update(transcription);
        }
    }

    @PutMapping("/transcription/{id}/avaliacao")
    public ResponseEntity<TranscriptionModel> atualizarAvaliacao(
            @PathVariable String id,
            @RequestBody Map<String, Object> payload) {

        TranscriptionModel transcription = transcriptionService.findById(Long.parseLong(id));
        if (transcription == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }

        if (payload.get("erro") != null) {
            transcription.setStatusAvaliacao("Erro");
            transcription.setAvaliacao(String.valueOf(payload.get("erro")));
        } else {
            try {
                transcription.setStatusAvaliacao("Concluído");
                transcription.setAvaliacao(new ObjectMapper().writeValueAsString(payload));
            } catch (JsonProcessingException e) {
                transcription.setStatusAvaliacao("Erro");
                transcription.setAvaliacao("Falha ao gravar a avaliação.");
            }
        }

        transcription = transcriptionService.update(transcription);
        return ResponseEntity.ok(transcription);
    }

    @PutMapping("/transcription/{id}/prompt")
    public ResponseEntity<TranscriptionModel> salvarPrompt(
            @PathVariable String id,
            @RequestBody Map<String, String> payload) {

        TranscriptionModel transcription = transcriptionService.findById(Long.parseLong(id));
        if (transcription == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }

        String prompt = payload.get("prompt");
        if (prompt == null || prompt.isBlank()) {
            return ResponseEntity.badRequest().build();
        }

        transcription.setPrompt(prompt);
        transcription = transcriptionService.update(transcription);
        return ResponseEntity.ok(transcription);
    }

    @DeleteMapping("/video-aula/{id}")
    public ResponseEntity<Void> deletarVideoAula(@PathVariable Long id, Authentication authentication) {
        UserModel user = (UserModel) authentication.getPrincipal();
        if (!UserModel.class.isInstance(user)) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
        
        VideoAulaModel videoAula = service.findById(id);
        if (videoAula == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }
        service.delete(videoAula);
        return ResponseEntity.noContent().build();
    }

    // 👇 O parâmetro Authentication authentication estava faltando aqui
    @PutMapping("video-aula/{id}")
    public ResponseEntity<VideoAulaModel> atualizarVideoAula(@PathVariable String id, @RequestBody VideoAulaModel videoAula, Authentication authentication) {
        UserModel user = (UserModel) authentication.getPrincipal();
        if (!UserModel.class.isInstance(user)) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
        
        VideoAulaModel videoAulaAtualizado = service.update(id, videoAula);
        if (videoAulaAtualizado == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(videoAulaAtualizado);
    }

    @PutMapping("/transcription/{id}")
    public ResponseEntity<TranscriptionModel> atualizarTranscricao(
            @PathVariable String id,
            @RequestBody Map<String, String> payload) {

        String conteudo = payload.get("resumo"); 
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
        transcription.setPrompt(payload.get("prompt"));
        transcription = transcriptionService.update(transcription);

        if (transcription == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }
        return ResponseEntity.ok(transcription);
    }

    private void enviarArquivoParaFastAPI(Long transcriptionId, File file, String token, String prompt) throws IOException {

        System.out.println("Enviando arquivo para FastAPI...");
        WebClient webClient = WebClient.builder().baseUrl(FASTAPI_URL).defaultHeader("Authorization", token)
                .build();

        try {
            MultipartBodyBuilder builder = new MultipartBodyBuilder();
            builder.part("file", new FileSystemResource(file));
            if (prompt != null && !prompt.isBlank()) {
                builder.part("prompt", prompt);
            }
            
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