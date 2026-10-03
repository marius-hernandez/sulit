package com.marius.sulit.exception;

import java.util.UUID;

public class ConversationNotFoundException extends RuntimeException {

    public ConversationNotFoundException(UUID conversationId) {
        super("Conversation " + conversationId + " was not found.");
    }
}
