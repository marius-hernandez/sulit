package com.marius.sulit.entity;

public enum MessageRole {
    USER,
    ASSISTANT;

    public String value() {
        return name().toLowerCase();
    }
}
