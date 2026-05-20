package com.example.UTranscriptBack.models;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Column;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.JoinColumn;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;


@Getter
@Setter
@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor

public class UserModel {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String nome;

    @Column(unique = true)
    private String email;

    private String senha;

    @ManyToOne
    @JoinColumn(name="curso_id")
    private CursoModel curso;

    @ManyToOne
    @JoinColumn(name="universidade_id")
    private UniversidadeModel universidade;

}
