package com.marius.sulit;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.ConfigurationPropertiesScan;

@SpringBootApplication
@ConfigurationPropertiesScan
public class SulitApplication {

	public static void main(String[] args) {
		SpringApplication.run(SulitApplication.class, args);
	}

}
