package com.stockInformationProcurer.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
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

        mailService.sendEmail(to, subject, text,file.getBytes(),filename);
            return "Email sent successfully!";
        }
}

