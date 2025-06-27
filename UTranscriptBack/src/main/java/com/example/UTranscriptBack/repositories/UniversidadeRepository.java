package com.example.UTranscriptBack.repositories;

import org.springframework.data.jpa.repository.JpaRepository;


import com.example.UTranscriptBack.models.UniversidadeModel;

public interface UniversidadeRepository extends JpaRepository<UniversidadeModel, Long> {
	
}
