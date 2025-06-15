package com.example.UTranscriptBack.config;

import java.io.IOException;

import org.springframework.web.filter.OncePerRequestFilter;

import com.example.UTranscriptBack.models.UserModel;
import com.example.UTranscriptBack.repositories.UserRepository;
import com.example.UTranscriptBack.services.JwtService;

import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import java.util.List;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

@Component 
public class JwtFilter extends OncePerRequestFilter{
    private UserRepository usuarioRepo;
    private JwtService jwtService;

   
    public JwtFilter(UserRepository usuarioRepo,JwtService jwtService) {
        this.usuarioRepo = usuarioRepo;
        this.jwtService = jwtService;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain)
            throws ServletException, IOException {

        String token = request.getHeader("Authorization");
        if (token != null && token.startsWith("Bearer ")) {
            String jwt = token.substring(7);
            String email = jwtService.extrairEmail(jwt);
            UserModel usuario = usuarioRepo.findByEmail(email).orElse(null);
            if (usuario != null) {
                UsernamePasswordAuthenticationToken auth =
                        new UsernamePasswordAuthenticationToken(usuario, null, List.of());
                SecurityContextHolder.getContext().setAuthentication(auth);
            }
        }

        filterChain.doFilter(request, response);
    }
}
