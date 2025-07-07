package com.example.UTranscriptBack.services;

import org.springframework.stereotype.Service;

import com.example.UTranscriptBack.models.TranscriptionModel;
import com.example.UTranscriptBack.repositories.TranscriptionRepository;

@Service
public class TranscriptionService {

    private final TranscriptionRepository repo;

    public TranscriptionService(TranscriptionRepository repo) {
        this.repo = repo;
    }

    public TranscriptionModel create(TranscriptionModel transcription) {
        return this.repo.save(transcription);
    }

    public TranscriptionModel findByVideoAulaId(Long videoAulaId) {
        return this.repo.findByVideoAulaId(videoAulaId).orElse(null);
    }

    public void deleteByVideoAula(Long videoAulaId) {
        TranscriptionModel transcription = this.repo.findByVideoAulaId(videoAulaId).orElse(null);
        if (transcription != null) {
           this.repo.delete(transcription);
        }   
        return;
    }
}
