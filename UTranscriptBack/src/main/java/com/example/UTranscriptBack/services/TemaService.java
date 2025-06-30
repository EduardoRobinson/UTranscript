package com.example.UTranscriptBack.services;

import java.util.List;

import org.springframework.stereotype.Service;

import com.example.UTranscriptBack.models.TemaModel;
import com.example.UTranscriptBack.repositories.TemaRepository;

@Service
public class TemaService {
    private final TemaRepository repo;
    public TemaService(TemaRepository repo) {
        this.repo = repo;
    }

    public List<TemaModel> findAll() {
        return repo.findAll();
    }

    public List<TemaModel> findByCursoId(Long cursoId) {
        return repo.findAll().stream()
                   .filter(tema -> tema.getCurso().getId().equals(cursoId))
                   .toList();
    }      
    
    public TemaModel findById(Long id) {
        return repo.findById(id).orElseThrow(() -> new RuntimeException("Tema not found"));
    }
}
