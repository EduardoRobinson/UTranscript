package com.example.UTranscriptBack.repositories;


import org.springframework.data.jpa.repository.JpaRepository;


import com.example.UTranscriptBack.models.TemaModel;
public interface TemaRepository extends JpaRepository<TemaModel, Long> {
   
}

