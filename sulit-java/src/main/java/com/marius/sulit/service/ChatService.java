package com.marius.sulit.service;

import com.marius.sulit.client.AiServiceClient;
import com.marius.sulit.client.AiServiceDtos.AiMessage;
import com.marius.sulit.config.AppProperties;
import com.marius.sulit.dto.ChatResponse;
import com.marius.sulit.dto.MessageDto;
import com.marius.sulit.entity.Conversation;
import com.marius.sulit.entity.Message;
import com.marius.sulit.entity.MessageRole;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;

/**
 * Orchestrates a chat turn. Deliberately not @Transactional so no DB connection
 * is held while waiting on the LLM.
 */
@Service
public class ChatService {

    private final ConversationService conversationService;
    private final AiServiceClient aiServiceClient;
    private final int historyLimit;

    public ChatService(ConversationService conversationService,
                       AiServiceClient aiServiceClient,
                       AppProperties appProperties) {
        this.conversationService = conversationService;
        this.aiServiceClient = aiServiceClient;
        this.historyLimit = appProperties.chat().historyLimit();
    }

    public ChatResponse chat(UUID conversationId, String userMessage) {
        String content = userMessage.strip();

        Conversation conversation = conversationService.getOrCreate(conversationId, content);
        UUID id = conversation.getId();
        conversationService.addMessage(id, MessageRole.USER, content);

        List<AiMessage> history = conversationService.getRecentMessages(id, historyLimit).stream()
                .map(m -> new AiMessage(m.getRole().value(), m.getContent()))
                .toList();

        String reply = aiServiceClient.chat(history);
        Message assistantMessage = conversationService.addMessage(id, MessageRole.ASSISTANT, reply);

        return new ChatResponse(id, MessageDto.from(assistantMessage));
    }

    public List<MessageDto> getMessages(UUID conversationId) {
        return conversationService.getMessages(conversationId).stream()
                .map(MessageDto::from)
                .toList();
    }
}
