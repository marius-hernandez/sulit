package com.marius.sulit.client;

import com.marius.sulit.client.AiServiceDtos.AiChatRequest;
import com.marius.sulit.client.AiServiceDtos.AiChatResponse;
import com.marius.sulit.client.AiServiceDtos.AiMessage;
import com.marius.sulit.exception.AiServiceException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatusCode;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestClientException;

import java.util.List;

@Component
public class AiServiceClient {

    private static final Logger log = LoggerFactory.getLogger(AiServiceClient.class);

    private final RestClient restClient;

    public AiServiceClient(RestClient aiServiceRestClient) {
        this.restClient = aiServiceRestClient;
    }

    public String chat(List<AiMessage> messages) {
        AiChatResponse response;
        try {
            response = restClient.post()
                    .uri("/v1/chat")
                    .body(new AiChatRequest(messages))
                    .retrieve()
                    .onStatus(HttpStatusCode::isError, (request, res) -> {
                        throw new AiServiceException("AI service responded with status " + res.getStatusCode().value());
                    })
                    .body(AiChatResponse.class);
        } catch (RestClientException ex) {
            log.error("Failed to reach AI service", ex);
            throw new AiServiceException("AI service is unavailable.", ex);
        }

        if (response == null || !StringUtils.hasText(response.reply())) {
            throw new AiServiceException("AI service returned an empty reply.");
        }
        return response.reply();
    }
}
