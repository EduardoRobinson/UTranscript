package com.example.UTranscriptBack.controllers;

import org.springframework.http.HttpHeaders;

import org.springframework.http.MediaType;

import java.util.List;

import org.apache.tomcat.util.net.openssl.ciphers.Authentication;
import org.springframework.http.ContentDisposition;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import com.example.UTranscriptBack.dto.VideoAulaDTO;
import com.example.UTranscriptBack.dto.YoutubeRequestDTO;
import com.example.UTranscriptBack.models.CursoModel;
import com.example.UTranscriptBack.models.TemaModel;
import com.example.UTranscriptBack.models.UniversidadeModel;
import com.example.UTranscriptBack.models.VideoAulaModel;
import com.example.UTranscriptBack.services.CursoService;
import com.example.UTranscriptBack.services.TemaService;
import com.example.UTranscriptBack.services.UniversidadeService;
import com.example.UTranscriptBack.services.VideoAulaService;


@RestController
public class UTranscriptController {

    private final String FASTAPI_URL = "http://127.0.0.1:8000/youtube_download";

    private final VideoAulaService service;

    private TemaService temaService;

    private CursoService cursoService;

    private UniversidadeService universidadeService;


    public UTranscriptController(VideoAulaService service, TemaService temaService, CursoService cursoService,
            UniversidadeService universidadeService) {
        this.service = service;
        this.temaService = temaService;
        this.cursoService = cursoService;
        this.universidadeService = universidadeService;
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

    @PostMapping("/videoAula")
    public ResponseEntity<?> criar(@RequestBody VideoAulaDTO dto,Authentication authentication) {
        VideoAulaModel v = service.create(dto);
        return ResponseEntity.ok(v);
    }

    @GetMapping("/cursos")
    public List<CursoModel> cursos(Authentication authentication) {
        return cursoService.findAll();
    }

    @GetMapping("/temas/{id}")
    public List<TemaModel> getTemasPorCurso(@PathVariable Long id,Authentication authentication) {
        return temaService.findByCursoId(id);
    }

    @GetMapping("/universidades")
    public List<UniversidadeModel> universidades(Authentication authentication) {
        return universidadeService.findAll();
    }

}
