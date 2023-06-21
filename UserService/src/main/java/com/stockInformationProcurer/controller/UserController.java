package com.stockInformationProcurer.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class UserController {


    @RequestMapping(value = "/get")
    public ResponseEntity welcome() {
        return new ResponseEntity<>("User Controller works", HttpStatus.OK);
    }
}
