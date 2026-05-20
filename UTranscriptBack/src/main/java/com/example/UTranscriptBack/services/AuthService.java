package com.example.UTranscriptBack.services;
import com.example.UTranscriptBack.repositories.UserRepository;
import com.example.UTranscriptBack.repositories.CursoRepository;
import com.example.UTranscriptBack.repositories.UniversidadeRepository;
import com.example.UTranscriptBack.models.UserModel;
import com.example.UTranscriptBack.dto.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class AuthService {
   
    private final UserRepository usuarioRepo;
    private final CursoRepository cursoRepo;
    private final UniversidadeRepository universidadeRepo;

    public AuthService(UserRepository usuarioRepo,
                        CursoRepository cursoRepo,
                        UniversidadeRepository universidadeRepo) 
    {
        this.usuarioRepo = usuarioRepo;
        this.cursoRepo = cursoRepo;
        this.universidadeRepo = universidadeRepo;
    }

    @Autowired
    private PasswordEncoder passwordEncoder;

    public UserModel registrar(RegistroDTO dto) {
        UserModel user = new UserModel();
        user.setNome(dto.nome());
        user.setEmail(dto.email());
        user.setSenha(passwordEncoder.encode(dto.senha()));
        user.setCurso(cursoRepo.findById(dto.curso_id()).orElseThrow(() -> new RuntimeException("Curso não encontrado")));
        user.setUniversidade(universidadeRepo.findById(dto.universidade_id()).orElseThrow(() -> new RuntimeException("Universidade não encontrada")));
        return usuarioRepo.save(user);
    }

    public UserModel autenticar(LoginDTO dto) {
        UserModel user = usuarioRepo.findByEmail(dto.email())
            .orElseThrow(() -> new RuntimeException("Usuario nao encontrado"));
        if (!passwordEncoder.matches(dto.senha(), user.getSenha())) {
            throw new RuntimeException("Senha inválida");
        }
        return user;
    }
}
