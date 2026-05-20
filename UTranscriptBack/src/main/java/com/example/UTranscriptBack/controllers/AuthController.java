package com.example.UTranscriptBack.controllers;

import java.util.Map;
import java.util.List;

import org.springframework.security.core.Authentication;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseCookie;
import org.springframework.http.HttpStatus;

import com.example.UTranscriptBack.services.AuthService;
import com.example.UTranscriptBack.services.JwtService;
import com.example.UTranscriptBack.services.CursoService;
import com.example.UTranscriptBack.services.UniversidadeService;
import com.example.UTranscriptBack.models.CursoModel;
import com.example.UTranscriptBack.models.UniversidadeModel;

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

    @Autowired
    private CursoService cursoService;

    @Autowired
    private UniversidadeService universidadeService;
   
    @PostMapping("/registrar")
    public ResponseEntity<?> registrar(@RequestBody RegistroDTO dto) {
        UserModel user=authService.registrar(dto);
        return ResponseEntity.ok(Map.of("message", "Usuário registrado com sucesso","user", user));
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginDTO dto) {
        UserModel user = authService.autenticar(dto);
        String token = jwtService.gerarToken(user.getEmail());
        ResponseCookie cookie = ResponseCookie.from("token", token)
            .httpOnly(true)   
            .secure(false)     
            .path("/")         
            .maxAge(86400)     
            .sameSite("Lax")
            .build();

    return ResponseEntity.ok()
            .header(HttpHeaders.SET_COOKIE, cookie.toString())
            .body(Map.of("message", "Autenticação realizada com sucesso."));
        
    }

    @GetMapping("/healthcheck")
    public ResponseEntity<String> healthCheck() {
        return ResponseEntity.ok("OK");
    }

    @GetMapping("/universidades")
    public List<UniversidadeModel> universidades(Authentication authentication) {
        return universidadeService.findAll();
    }

     @GetMapping("/cursos")
    public List<CursoModel> cursos(Authentication authentication) {
        return cursoService.findAll();
    }

    @GetMapping("/user")
    public ResponseEntity<?> getUser(Authentication authentication) {
       if (authentication != null && authentication.getPrincipal() instanceof UserModel) {
            UserModel user = (UserModel) authentication.getPrincipal();
            System.out.println("User email: " + user.getEmail());
            return ResponseEntity.ok(user);
        }
       return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(Map.of("error", "Não autorizado"));
    }

    @PostMapping("/logout")
public ResponseEntity<?> logout() {
    // Cria um cookie com o mesmo nome e caminho, mas vazio e com MaxAge = 0
    ResponseCookie cookie = ResponseCookie.from("token", "")
            .httpOnly(true)
            .secure(false) // Mantenha igual ao do login (false para localhost, true para produção/HTTPS)
            .path("/")
            .maxAge(0)     // Faz o navegador deletar o cookie na mesma hora!
            .sameSite("Lax")
            .build();

    return ResponseEntity.ok()
            .header(HttpHeaders.SET_COOKIE, cookie.toString())
            .body(Map.of("message", "Logout realizado com sucesso."));
}

}
