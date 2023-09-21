/**
 * The `Main` class serves as the entry point for the Stock Information Procurer application.
 * It is annotated with `@SpringBootApplication`, indicating that it is the main application class
 * and enabling Spring Boot auto-configuration.
 * <p>
 * This class contains the `main` method, which is the starting point for running the application.
 * When executed, the `main` method invokes the `SpringApplication.run` method to bootstrap and start
 * the Spring Boot application.
 */
package com.stockInformationProcurer;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Main {
    /**
     * The main method is the entry point for the application.
     *
     * @param args Command-line arguments passed to the application (not used in this case).
     */
    public static void main(String[] args) {
        SpringApplication.run(Main.class, args);
    }
}
