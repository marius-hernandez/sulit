package com.marius.sulit.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

import java.util.UUID;

/**
 * @param conversationId null to start a new conversation
 */
public record ChatRequest(
        UUID conversationId,
        @NotBlank(message = "Message is required.")
        @Size(max = 4000, message = "Message must be at most 4000 characters.")
        String message
) {
}
