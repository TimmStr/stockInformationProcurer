/**
 * The `MailController` class is responsible for managing email-related endpoints.
 * It provides RESTful web services for sending emails and scheduling email notifications.
 * It is able to send an email with an attachment, and it is able to send an email to all users with all their
 * subscribed stocks.
 */

package com.stockInformationProcurer.controller;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.stockInformationProcurer.services.UserServiceConnection;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;


@RestController
@RequestMapping("/mail")
public class MailController {

    private final MailService mailService;

    @Autowired
    public MailController(MailService mailService) {
        this.mailService = mailService;
    }

    /**
     * Handles the HTTP POST request for sending an email.
     *
     * @param to       The recipient's email address.
     * @param subject  The subject of the email.
     * @param text     The content of the email.
     * @param file     The attached file.
     * @param filename The name of the attached file.
     * @return A success message indicating that the email was sent.
     * @throws IOException If there is an issue with file handling.
     */
    @PostMapping("/sendMail")
    public String sendMail(
            @RequestParam String to,
            @RequestParam String subject,
            @RequestParam String text,
            @RequestParam MultipartFile file,
            @RequestParam String filename) throws IOException {

        mailService.sendEmail(to, subject, text, file.getBytes(), filename);
        return "Email sent successfully!";
    }


    /**
     * Scheduled method to send emails to all users subscribed to stock updates.
     * This method is triggered every Monday at 20:00.
     *
     * @return A ResponseEntity with the result of sending emails to users.
     * @throws JsonProcessingException If there is an issue with JSON processing.
     */
    @Scheduled(cron = "0 0 20 * * 1") // every monday at 20:00
    @RequestMapping(value = "/sendMailToAllStocksForAllUsers", method = RequestMethod.GET)
    public ResponseEntity sendMailToAllStocksForAllUsers() throws JsonProcessingException {
        UserServiceConnection userServiceConnection = new UserServiceConnection(this.mailService);
        return userServiceConnection.sendMailtoAllUserSubscribers();
    }
}

