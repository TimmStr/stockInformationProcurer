package com.stockInformationProcurer.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class DocumentController {


    @RequestMapping(value = "/get")
    public ResponseEntity welcome() {
        return new ResponseEntity<>("Document Controller works", HttpStatus.OK);
    }


    @RequestMapping
    public ResponseEntity hello() {
        return new ResponseEntity<>("Hello from Spring boot & Keycloak", HttpStatus.OK);
    }

    @RequestMapping(value="/hello2")
    public ResponseEntity hello2() {
        return new ResponseEntity<>("Hello from Spring boot & Keycloak 2", HttpStatus.OK);
    }
}
