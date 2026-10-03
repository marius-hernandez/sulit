package com.marius.sulit.client;

import java.util.List;

/** Wire contract shared with the FastAPI service (sulit-ai). */
public final class AiServiceDtos {

    private AiServiceDtos() {
    }

    public record AiMessage(String role, String content) {
    }

    public record AiChatRequest(List<AiMessage> messages) {
    }

    public record AiChatResponse(String reply, String model) {
    }
}
