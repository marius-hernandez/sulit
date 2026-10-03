package com.marius.sulit.controller;

import com.marius.sulit.dto.ChatRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = {"http://localhost:3000", "http://127.0.0.1:3000"})
public class ChatController {

    @PostMapping("/chat")
    public ResponseEntity<Map<String, Object>> chat(@RequestBody ChatRequest request) {
        String message = request.message() == null ? "" : request.message().trim();

        if (message.isBlank()) {
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("success", false);
            errorResponse.put("message", "Message is required.");
            return ResponseEntity.badRequest().body(errorResponse);
        }

        Map<String, Object> response = new HashMap<>();
        response.put("success", true);
        response.put("reply", "Dummy backend response: " + message);
        response.put("message", "Dummy backend response: " + message);

        return ResponseEntity.ok(response);
    }
}
