package com.example.UTranscriptBack.controllers;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class UTranscriptController {

    @GetMapping("/health")
    public String health() {
        return "OK";
    }
}
