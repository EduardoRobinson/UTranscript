package com.example.UTranscriptBack.services;


import org.springframework.stereotype.Service;

import com.example.UTranscriptBack.dto.VideoAulaDTO;
import com.example.UTranscriptBack.models.CursoModel;
import com.example.UTranscriptBack.models.TemaModel;
import com.example.UTranscriptBack.models.UniversidadeModel;
import com.example.UTranscriptBack.models.VideoAulaModel;
import com.example.UTranscriptBack.repositories.VideoAulaRepository;

@Service
public class VideoAulaService {

    private final VideoAulaRepository repo;

    public VideoAulaService(VideoAulaRepository repo) {
        this.repo = repo;
    }

    public VideoAulaModel create(VideoAulaDTO dto) {
        VideoAulaModel v = new VideoAulaModel();
        v.setTitulo(dto.titulo);
        v.setData(dto.data);
        CursoModel curso = new CursoModel();
        curso.setId(dto.cursoId);
        v.setCurso(curso);

        UniversidadeModel universidade = new UniversidadeModel();
        universidade.setId(dto.universidadeId);
        v.setUniversidade(universidade);

        TemaModel tema = new TemaModel();
        tema.setId(dto.temaId);
        v.setTema(tema);

        return repo.save(v);
    }

    public VideoAulaModel findById(Long id) {
        return repo.findById(id).orElseThrow(() -> new RuntimeException("Video Aula not found"));
    }
    

}
