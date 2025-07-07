package com.example.UTranscriptBack.models;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDate;


@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Entity
@ToString
public class VideoAulaModel {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String titulo;
    private LocalDate data;
    private String professor;

    @ManyToOne
    @JoinColumn(name = "curso_id")
    private CursoModel curso;

    @ManyToOne
    @JoinColumn(name = "universidade_id")
    private UniversidadeModel universidade;

    @ManyToOne
    @JoinColumn(name = "tema_id")
    private TemaModel tema;

    @ManyToOne
    @JoinColumn(name = "usuario_id")
    private UserModel usuario;

    @OneToOne(mappedBy = "videoAula",cascade = CascadeType.ALL, orphanRemoval = true)
    private TranscriptionModel transcricoes;

}
