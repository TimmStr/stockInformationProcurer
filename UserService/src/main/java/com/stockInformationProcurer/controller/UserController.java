package com.stockInformationProcurer.controller;

import com.stockInformationProcurer.entity.User;
import com.stockInformationProcurer.services.UserService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @RequestMapping(value = "/get")
    public ResponseEntity welcome() {
        return new ResponseEntity<>("User Controller works", HttpStatus.OK);
    }

    @RequestMapping(value = "/addUser")
    public ResponseEntity addUser(@RequestParam String firstname,
                                  @RequestParam String lastname,
                                  @RequestParam String mail,
                                  @RequestParam String password,
                                  @RequestParam boolean mail_service) {
        List<User> users = getAllUsersFromDatabase();
        for (User user : users) {
            if (user.getMail().equals(mail)) {
                return new ResponseEntity<>("Userprofile already exists.", HttpStatus.NOT_ACCEPTABLE);
            }
        }
        User new_user = new User(firstname, lastname, mail, password, mail_service);
        userService.createUser(new_user);
        return new ResponseEntity<>(lastname + " added.", HttpStatus.OK);
    }


    @RequestMapping(value = "/getUserInformation")
    public ResponseEntity getUserInformation(@RequestParam String lastname) {
        User user = userService.getUserByLastname(lastname);
        return new ResponseEntity<>(user.toString(), HttpStatus.OK);
    }

    public List<User> getAllUsersFromDatabase() {
        return userService.getAllUsers();
    }

    @RequestMapping(value = "/getAllUsers")
    public ResponseEntity getAllUsers() {
        List<User> users = getAllUsersFromDatabase();
        return new ResponseEntity<>(users, HttpStatus.OK);
    }

    @RequestMapping(value = "/checkUser")
    public ResponseEntity checkUser(@RequestParam String mail, @RequestParam String password) {
        List<User> users = userService.getAllUsers();
        for (User user : users) {
            if (user.getMail().equals(mail) && user.getPassword().equals(password)) {
                System.out.println(user.getMail() + " " + mail);
                System.out.println(user.getPassword() + " " + password);
                return new ResponseEntity<>(user, HttpStatus.OK);
            }
        }
        return new ResponseEntity<>("User not found", HttpStatus.NOT_ACCEPTABLE);
    }

    @RequestMapping(value = "/updateUserPassword")
    public ResponseEntity updateUserPassword(@RequestParam String mail, @RequestParam String old_password, @RequestParam String new_password) {
        User user = userService.updateUserPassword(mail, old_password, new_password);
        if (user != null) {
            return new ResponseEntity<>(user, HttpStatus.OK);
        }
        return new ResponseEntity<>("User not found", HttpStatus.NOT_ACCEPTABLE);
    }

}

