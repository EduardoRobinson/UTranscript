package com.example.UTranscriptBack.services;

import java.util.List;

import org.springframework.stereotype.Service;

import com.example.UTranscriptBack.dto.VideoAulaDTO;
import com.example.UTranscriptBack.models.CursoModel;
import com.example.UTranscriptBack.models.TemaModel;
import com.example.UTranscriptBack.models.UniversidadeModel;
import com.example.UTranscriptBack.models.UserModel;
import com.example.UTranscriptBack.models.VideoAulaModel;
import com.example.UTranscriptBack.repositories.VideoAulaRepository;

@Service
public class VideoAulaService {

    private final VideoAulaRepository repo;

    private final CursoService cursoRepo;
    private final UniversidadeService universidadeRepo;
    private final TemaService temaRepo;
    private final TranscriptionService transcriptionRepo;


    public VideoAulaService(VideoAulaRepository repo,
                            CursoService cursoRepo,
                            UniversidadeService universidadeRepo,
                            TemaService temaRepo,
                            TranscriptionService transcriptionRepo) {
        this.repo = repo;
        this.cursoRepo = cursoRepo;
        this.universidadeRepo = universidadeRepo;
        this.temaRepo = temaRepo;   
        this.transcriptionRepo = transcriptionRepo;
    }

    public VideoAulaModel create(VideoAulaDTO dto, UserModel user) {
        VideoAulaModel v = new VideoAulaModel();
        v.setTitulo(dto.titulo);
        v.setData(dto.data);
        v.setProfessor(dto.professor);

        CursoModel curso = cursoRepo.findById(dto.cursoId);
        if (curso == null) {
            throw new RuntimeException("Curso não encontrado");
        }
        v.setCurso(curso);

        UniversidadeModel universidade = universidadeRepo.findById(dto.universidadeId);
        if (universidade == null) {
            throw new RuntimeException("Universidade não encontrada");
        }
        v.setUniversidade(universidade);

        TemaModel tema = temaRepo.findById(dto.temaId);
        if (tema == null) {
            throw new RuntimeException("Tema não encontrado");
        }
        v.setTema(tema);

        v.setUsuario(user);

        return repo.save(v);
    }

    public VideoAulaModel findById(Long id) {
        return repo.findById(id).orElseThrow(() -> new RuntimeException("Video Aula not found"));
    }

    public List<VideoAulaModel> findAll() {
        return repo.findAll();
    }

    public void delete(VideoAulaModel videoAula) {
        transcriptionRepo.deleteByVideoAula(videoAula.getId());
        repo.delete(videoAula);
    }

    public VideoAulaModel update(String id, VideoAulaModel videoAula) {
        VideoAulaModel existingVideoAula = repo.findById(Long.parseLong(id))
                .orElseThrow(() -> new RuntimeException("Video Aula not found"));

        existingVideoAula.setTitulo(videoAula.getTitulo());
        existingVideoAula.setData(videoAula.getData());
        existingVideoAula.setProfessor(videoAula.getProfessor());
        existingVideoAula.setCurso(videoAula.getCurso());
        existingVideoAula.setUniversidade(videoAula.getUniversidade());
        existingVideoAula.setTema(videoAula.getTema());

        return repo.save(existingVideoAula);
    }

}
