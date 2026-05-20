package com.example.UTranscriptBack.config;

import java.io.IOException;
import java.util.List;

import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import com.example.UTranscriptBack.models.UserModel;
import com.example.UTranscriptBack.repositories.UserRepository;
import com.example.UTranscriptBack.services.JwtService;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

@Component
public class JwtFilter extends OncePerRequestFilter {
    
    private UserRepository usuarioRepo;
    private JwtService jwtService;

    public JwtFilter(UserRepository usuarioRepo, JwtService jwtService) {
        this.usuarioRepo = usuarioRepo;
        this.jwtService = jwtService;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request,
            HttpServletResponse response,
            FilterChain filterChain)
            throws ServletException, IOException {

        // Chama o método auxiliar para extrair o token (seja do cookie ou do header)
        String jwt = extrairToken(request);

        if (jwt != null) {
            try {
                String email = jwtService.extrairEmail(jwt);
                UserModel usuario = usuarioRepo.findByEmail(email).orElse(null);

                if (usuario != null) {
                    UsernamePasswordAuthenticationToken auth = new UsernamePasswordAuthenticationToken(
                            usuario, null, List.of());
                    SecurityContextHolder.getContext().setAuthentication(auth);
                }

            } catch (Exception e) {
                response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
                response.setContentType("application/json");
                response.getWriter().write("{\"error\": \"Token inválido ou expirado.\"}");
                return;
            }
        }

        filterChain.doFilter(request, response);
    }

    /**
     * Método auxiliar para buscar o JWT.
     * Prioriza os Cookies (usado pelo Angular). Faz fallback para o Header (Postman/Insomnia).
     */
    private String extrairToken(HttpServletRequest request) {
        // 1. Tenta buscar nos Cookies
        if (request.getCookies() != null) {
            for (Cookie cookie : request.getCookies()) {
                if ("token".equals(cookie.getName())) {
                    return cookie.getValue();
                }
            }
        }

        // 2. Se não encontrar no Cookie, tenta buscar no Header Authorization
        String tokenHeader = request.getHeader("Authorization");
        if (tokenHeader != null && tokenHeader.startsWith("Bearer ")) {
            return tokenHeader.substring(7);
        }

        return null;
    }
}