package com.example.UTranscriptBack.repositories;


import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.UTranscriptBack.models.StatusTranscriptionModel;

public interface StatusTranscriptionRepository extends JpaRepository<StatusTranscriptionModel, Long> {
    Optional<StatusTranscriptionModel> findByDescricao(String descricao);
}
