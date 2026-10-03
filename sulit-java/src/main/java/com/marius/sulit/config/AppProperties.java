package com.marius.sulit.config;

import jakarta.validation.Valid;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.validation.annotation.Validated;

import java.net.URI;
import java.time.Duration;
import java.util.List;

@Validated
@ConfigurationProperties(prefix = "app")
public record AppProperties(
        @Valid @NotNull Cors cors,
        @Valid @NotNull Chat chat,
        @Valid @NotNull AiService aiService
) {

    public record Cors(@NotEmpty List<String> allowedOrigins) {
    }

    public record Chat(@Min(1) int historyLimit) {
    }

    public record AiService(
            @NotNull URI baseUrl,
            String apiKey,
            @NotNull Duration connectTimeout,
            @NotNull Duration readTimeout
    ) {
    }
}
