package com.stockInformationProcurer.controller;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.stockInformationProcurer.services.UserServiceConnection;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
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

    @RequestMapping(value = "/get")
    public ResponseEntity welcome() {
        return new ResponseEntity<>("Mail Controller works", HttpStatus.OK);
    }

    @PostMapping("/send")
    public String sendEmail(
            @RequestParam String to,
            @RequestParam String subject,
            @RequestParam String text,
            @RequestParam MultipartFile file,
            @RequestParam String filename) throws IOException {

        mailService.sendEmail(to, subject, text, file.getBytes(), filename);
        return "Email sent successfully!";
    }

    @RequestMapping(value = "/getAllStocksForUser", method = RequestMethod.GET)
    public ResponseEntity getAllStocksForUser(
            @RequestParam String mail,
            @RequestParam String password) {

        UserServiceConnection userServiceConnection = new UserServiceConnection(this.mailService);
        return userServiceConnection.getAllStocksForUserFromUserService(mail, password);
    }

    @RequestMapping(value = "/sendMailToAllStocksForAllUsers", method = RequestMethod.GET)
    public ResponseEntity sendMailToAllStocksForAllUsers() throws JsonProcessingException {
        UserServiceConnection userServiceConnection = new UserServiceConnection(this.mailService);
        return userServiceConnection.sendMailtoAllUserSubscribers();


    }
}

