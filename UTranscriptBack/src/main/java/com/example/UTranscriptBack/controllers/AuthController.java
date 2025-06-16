package com.example.UTranscriptBack.controllers;

import java.util.Map;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.UTranscriptBack.services.AuthService;
import com.example.UTranscriptBack.services.JwtService;

import jakarta.servlet.http.HttpServletRequest;

import com.example.UTranscriptBack.models.UserModel;
import com.example.UTranscriptBack.repositories.UserRepository;
import com.example.UTranscriptBack.dto.RegistroDTO;
import com.example.UTranscriptBack.dto.LoginDTO;

@RestController
@RequestMapping("/auth")

public class AuthController {
       @Autowired
    private AuthService authService;

    @Autowired
    private JwtService jwtService;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private HttpServletRequest request;
   
    @PostMapping("/registrar")
    public ResponseEntity<?> registrar(@RequestBody RegistroDTO dto) {
        authService.registrar(dto);
        return ResponseEntity.ok("Usuário registrado com sucesso");
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginDTO dto) {
        System.out.println(dto);
        UserModel user = authService.autenticar(dto);
        String token = jwtService.gerarToken(user.getEmail());
        return ResponseEntity.ok(Map.of("token", token));
    }

    @GetMapping("/healthcheck")
    public ResponseEntity<String> healthCheck() {
        return ResponseEntity.ok("OK");
    }

    @GetMapping("/user")
    public ResponseEntity<?> getUser() {
        String token = request.getHeader("Authorization");

        if (token == null || !token.startsWith("Bearer ")) {
            return ResponseEntity.status(401).body("Token não fornecido ou inválido");
        }

        String jwt = token.substring(7);
        String email = jwtService.extrairEmail(jwt);

        return userRepository.findByEmail(email)
            .<ResponseEntity<?>>map(user -> ResponseEntity.ok(user))
            .orElseGet(() -> ResponseEntity.status(404).body("Usuário não encontrado"));
    }

}
