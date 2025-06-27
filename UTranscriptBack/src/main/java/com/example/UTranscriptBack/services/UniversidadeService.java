package com.example.UTranscriptBack.services;

import java.util.List;

import org.springframework.stereotype.Service;

import com.example.UTranscriptBack.models.UniversidadeModel;
import com.example.UTranscriptBack.repositories.UniversidadeRepository;

@Service
public class UniversidadeService {
    private final UniversidadeRepository repo;
    public UniversidadeService(UniversidadeRepository repo) {
        this.repo = repo;
    }

    public List<UniversidadeModel> findAll() {
        return repo.findAll();
    }
}
