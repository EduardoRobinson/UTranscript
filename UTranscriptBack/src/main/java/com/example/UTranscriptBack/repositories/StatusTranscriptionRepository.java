package com.example.UTranscriptBack.repositories;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.UTranscriptBack.models.StatusTranscriptionModel;

public interface StatusTranscriptionRepository extends JpaRepository<StatusTranscriptionModel, Long> {
}
