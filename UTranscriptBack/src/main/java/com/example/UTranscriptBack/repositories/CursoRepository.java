package com.example.UTranscriptBack.repositories;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.UTranscriptBack.models.CursoModel;


public interface CursoRepository extends JpaRepository<CursoModel, Long>{
    Optional<CursoModel> findByNomeIgnoreCase(String nome);
}
