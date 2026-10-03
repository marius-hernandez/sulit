package com.marius.sulit.controller;

import com.marius.sulit.dto.ChatRequest;
import com.marius.sulit.dto.ChatResponse;
import com.marius.sulit.dto.MessageDto;
import com.marius.sulit.service.ChatService;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api")
public class ChatController {

    private final ChatService chatService;

    public ChatController(ChatService chatService) {
        this.chatService = chatService;
    }

    @PostMapping("/chat")
    public ChatResponse chat(@Valid @RequestBody ChatRequest request) {
        return chatService.chat(request.conversationId(), request.message());
    }

    @GetMapping("/conversations/{conversationId}/messages")
    public List<MessageDto> getMessages(@PathVariable UUID conversationId) {
        return chatService.getMessages(conversationId);
    }
}
