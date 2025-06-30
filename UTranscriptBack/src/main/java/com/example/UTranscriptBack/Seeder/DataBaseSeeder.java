package com.example.UTranscriptBack.Seeder;


import java.util.Map;
import java.util.Optional;

import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import com.example.UTranscriptBack.models.CursoModel;
import com.example.UTranscriptBack.models.StatusTranscriptionModel;
import com.example.UTranscriptBack.models.TemaModel;
import com.example.UTranscriptBack.models.UniversidadeModel;
import com.example.UTranscriptBack.repositories.CursoRepository;
import com.example.UTranscriptBack.repositories.StatusTranscriptionRepository;
import com.example.UTranscriptBack.repositories.TemaRepository;
import com.example.UTranscriptBack.repositories.UniversidadeRepository;
import static com.example.UTranscriptBack.Seeder.DataSeed.*;

@Component
public class DataBaseSeeder implements CommandLineRunner {

    private final CursoRepository cursoRepo;
    private final UniversidadeRepository universidadeRepo;
    private final TemaRepository temaRepo;
    private final StatusTranscriptionRepository statusRepo;

    public DataBaseSeeder(
            CursoRepository cursoRepo,
            UniversidadeRepository universidadeRepo,
            TemaRepository temaRepo,
            StatusTranscriptionRepository statusRepo) {
        this.cursoRepo = cursoRepo;
        this.universidadeRepo = universidadeRepo;
        this.temaRepo = temaRepo;
        this.statusRepo = statusRepo;
    }

    @Override
    public void run(String... args) throws Exception {
        seedUniversidades();
        seedCursos();
        seedTemas();
        seedStatus();
    }

    private void seedUniversidades() {
        if (universidadeRepo.count() == 0) {
            for (UniversidadeModel universidade : UNIVERSIDADES) {
                universidadeRepo.save(universidade);
            }
        }

    }

    private void seedCursos() {
        if (cursoRepo.count() == 0) {
            for (CursoModel curso : CURSOS) {
                cursoRepo.save(curso);
            }
        }
    }

    private void seedTemas() {
        if (temaRepo.count() == 0) {
            for (Object temaObj : TEMAS) {
                @SuppressWarnings("unchecked")
                Map<String, String> temaMap = (Map<String, String>) temaObj;

                String nomeCurso = temaMap.get("curso");
                String nomeMateria = temaMap.get("materia");

                // Busca o curso pelo nome
                Optional<CursoModel> cursoOpt = cursoRepo.findByNomeIgnoreCase(nomeCurso);

                if (cursoOpt.isPresent()) {
                    CursoModel curso = cursoOpt.get();

                    TemaModel tema = new TemaModel();
                    tema.setDescricao(nomeMateria);
                    tema.setCurso(curso);

                    temaRepo.save(tema);
                } else {
                    System.out.println("Curso não encontrado: " + nomeCurso);
                }
            }

            System.out.println("Temas seeded com sucesso.");
        }
    }

    private void seedStatus(){
        if(statusRepo.count()==0){
            for(StatusTranscriptionModel status:STATUS){
                statusRepo.save(status);
            }
        }
    }

}
