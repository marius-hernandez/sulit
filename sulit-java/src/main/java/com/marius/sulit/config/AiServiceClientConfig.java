package com.marius.sulit.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.client.JdkClientHttpRequestFactory;
import org.springframework.util.StringUtils;
import org.springframework.web.client.RestClient;

import java.net.http.HttpClient;

@Configuration
public class AiServiceClientConfig {

    public static final String INTERNAL_API_KEY_HEADER = "X-Internal-Api-Key";

    @Bean
    public RestClient aiServiceRestClient(AppProperties appProperties) {
        AppProperties.AiService props = appProperties.aiService();

        // Force HTTP/1.1: the JDK client otherwise attempts an h2c upgrade that uvicorn doesn't support.
        HttpClient httpClient = HttpClient.newBuilder()
                .version(HttpClient.Version.HTTP_1_1)
                .connectTimeout(props.connectTimeout())
                .build();

        JdkClientHttpRequestFactory requestFactory = new JdkClientHttpRequestFactory(httpClient);
        requestFactory.setReadTimeout(props.readTimeout());

        RestClient.Builder builder = RestClient.builder()
                .baseUrl(props.baseUrl().toString())
                .requestFactory(requestFactory)
                .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
                .defaultHeader(HttpHeaders.ACCEPT, MediaType.APPLICATION_JSON_VALUE);

        if (StringUtils.hasText(props.apiKey())) {
            builder.defaultHeader(INTERNAL_API_KEY_HEADER, props.apiKey());
        }

        return builder.build();
    }
}
