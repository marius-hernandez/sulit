package com.marius.sulit.service;

import com.marius.sulit.entity.Conversation;
import com.marius.sulit.entity.Message;
import com.marius.sulit.entity.MessageRole;
import com.marius.sulit.exception.ConversationNotFoundException;
import com.marius.sulit.repository.ConversationRepository;
import com.marius.sulit.repository.MessageRepository;
import org.springframework.data.domain.Limit;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.UUID;

@Service
public class ConversationService {

    private static final int TITLE_MAX_LENGTH = 60;

    private final ConversationRepository conversationRepository;
    private final MessageRepository messageRepository;

    public ConversationService(ConversationRepository conversationRepository, MessageRepository messageRepository) {
        this.conversationRepository = conversationRepository;
        this.messageRepository = messageRepository;
    }

    @Transactional
    public Conversation getOrCreate(UUID conversationId, String firstMessage) {
        if (conversationId != null) {
            return conversationRepository.findById(conversationId)
                    .orElseThrow(() -> new ConversationNotFoundException(conversationId));
        }
        return conversationRepository.save(new Conversation(toTitle(firstMessage)));
    }

    @Transactional
    public Message addMessage(UUID conversationId, MessageRole role, String content) {
        Conversation conversation = conversationRepository.getReferenceById(conversationId);
        return messageRepository.save(new Message(conversation, role, content));
    }

    /** Returns the most recent messages in chronological order. */
    @Transactional(readOnly = true)
    public List<Message> getRecentMessages(UUID conversationId, int limit) {
        List<Message> messages = new ArrayList<>(
                messageRepository.findByConversationIdOrderByCreatedAtDesc(conversationId, Limit.of(limit)));
        Collections.reverse(messages);
        return messages;
    }

    @Transactional(readOnly = true)
    public List<Message> getMessages(UUID conversationId) {
        if (!conversationRepository.existsById(conversationId)) {
            throw new ConversationNotFoundException(conversationId);
        }
        return messageRepository.findByConversationIdOrderByCreatedAtAsc(conversationId);
    }

    private static String toTitle(String message) {
        String normalized = message.strip().replaceAll("\\s+", " ");
        return normalized.length() <= TITLE_MAX_LENGTH ? normalized : normalized.substring(0, TITLE_MAX_LENGTH);
    }
}
