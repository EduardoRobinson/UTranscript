package com.example.UTranscriptBack.services;

import java.util.List;

import org.springframework.stereotype.Service;

import com.example.UTranscriptBack.models.CursoModel;
import com.example.UTranscriptBack.repositories.CursoRepository;

@Service
public class CursoService {
    private final CursoRepository repo;
    public CursoService(CursoRepository repo) {
        this.repo = repo;
    }

    public List<CursoModel> findAll() {
        return repo.findAll();
    }
}
