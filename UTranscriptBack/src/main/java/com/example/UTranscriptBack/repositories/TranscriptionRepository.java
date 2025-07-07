package com.example.UTranscriptBack.repositories;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.UTranscriptBack.models.TranscriptionModel;

public interface TranscriptionRepository extends JpaRepository<TranscriptionModel, Long> {
    Optional<TranscriptionModel> findByVideoAulaId(Long videoAulaId);
    // Define any custom query methods if needed
    // For example:
    // List<TranscriptionModel> findByVideoAulaId(Long videoAulaId);
    
}
