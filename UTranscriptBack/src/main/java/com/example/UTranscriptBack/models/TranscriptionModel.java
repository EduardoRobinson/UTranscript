package com.example.UTranscriptBack.models;
import com.fasterxml.jackson.annotation.JsonIgnore;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToOne;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@Entity
@Data
@ToString(exclude = "videoAula")
@NoArgsConstructor
@AllArgsConstructor
public class TranscriptionModel {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(columnDefinition = "TEXT")
    private String conteudo;
    
    @OneToOne
    @JoinColumn (name = "video_aula_id")
    @JsonIgnore
    private VideoAulaModel videoAula;

    @ManyToOne
    @JoinColumn(name = "status_id")
    private StatusTranscriptionModel status;

    @Column(name = "tipo_extracao", nullable = false, length = 20)
    private String tipoExtracao = "COMUM";

    @Column(columnDefinition = "TEXT")
    private String prompt;

    @Column(name = "prompt_personalizado", columnDefinition = "TEXT")
    private String promptPersonalizado;

    @Column(name = "status_avaliacao", length = 30)
    private String statusAvaliacao;

    @Column(columnDefinition = "TEXT")
    private String avaliacao;

}
