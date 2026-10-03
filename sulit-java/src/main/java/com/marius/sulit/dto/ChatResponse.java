package com.marius.sulit.dto;

import java.util.UUID;

public record ChatResponse(UUID conversationId, MessageDto message) {
}
