package com.marius.sulit.dto;

import com.marius.sulit.entity.Message;

import java.time.Instant;
import java.util.UUID;

public record MessageDto(UUID id, String role, String content, Instant createdAt) {

    public static MessageDto from(Message message) {
        return new MessageDto(
                message.getId(),
                message.getRole().value(),
                message.getContent(),
                message.getCreatedAt()
        );
    }
}
