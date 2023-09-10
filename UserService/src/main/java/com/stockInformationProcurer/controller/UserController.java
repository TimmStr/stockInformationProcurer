package com.stockInformationProcurer.controller;

import com.stockInformationProcurer.entity.UserEntity;
import com.stockInformationProcurer.services.UserRepositoryService;
import org.apache.catalina.User;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class UserController {
    private final UserRepositoryService userRepositoryService;

    public UserController(UserRepositoryService userRepositoryService) {
        this.userRepositoryService = userRepositoryService;
    }

    @RequestMapping(value = "/get")
    public ResponseEntity welcome() {
        return new ResponseEntity<>("User Controller works", HttpStatus.OK);
    }

    @RequestMapping(value = "/addUser")
    public ResponseEntity addUser(@RequestParam String firstname, @RequestParam String lastname, @RequestParam String mail, @RequestParam String password) {
        System.out.println("firstname: " + firstname+ " lastname: " + lastname+  " mail: " + mail+  " password: " + password);
        UserEntity userEntity = new UserEntity(firstname, lastname, mail, password);
        userRepositoryService.addUserInformation(userEntity);
        return new ResponseEntity<>(lastname +" added.", HttpStatus.OK);
    }



    @RequestMapping(value = "/getUserInformation")
    public ResponseEntity getUserInformation(@RequestParam String lastname) {
        String userinformation = userRepositoryService.getUserInformationForLastname(lastname);
        return new ResponseEntity<>(userinformation, HttpStatus.OK);
    }

    @RequestMapping(value = "/checkUser")
    public ResponseEntity checkUser(@RequestParam String mail, @RequestParam String password) {
        List<UserEntity> users = userRepositoryService.findAll();
        return new ResponseEntity<>(users, HttpStatus.OK);
    }

}

