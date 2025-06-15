package com.example.UTranscriptBack.services;
import com.example.UTranscriptBack.repositories.UserRepository;
import com.example.UTranscriptBack.models.UserModel;
import com.example.UTranscriptBack.dto.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class AuthService {
     @Autowired
    private UserRepository usuarioRepo;

    @Autowired
    private PasswordEncoder passwordEncoder;

    public void registrar(RegistroDTO dto) {
        UserModel user = new UserModel();
        user.setNome(dto.nome());
        user.setEmail(dto.email());
        user.setSenha(passwordEncoder.encode(dto.senha()));
        usuarioRepo.save(user);
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
