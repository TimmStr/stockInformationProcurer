package com.stockInformationProcurer.controller;

import com.stockInformationProcurer.entity.User;
import com.stockInformationProcurer.entity.UserStock;
import com.stockInformationProcurer.services.UserService;
import com.stockInformationProcurer.services.UserStockService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class UserController {

    private final UserService userService;
    private final UserStockService userStockService;

    public UserController(UserService userService, UserStockService userStockService) {
        this.userService = userService;
        this.userStockService = userStockService;
    }

    @RequestMapping(value = "/get")
    public ResponseEntity welcome() {
        return new ResponseEntity<>("User Controller works", HttpStatus.OK);
    }


    //
//    User Requests
//
    public List<User> getAllUsersFromDatabase() {
        return userService.getAllUsers();
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
        User newUser = new User(firstname, lastname, mail, password, mail_service);
        userService.createUser(newUser);
        return new ResponseEntity<>(lastname + " added.", HttpStatus.OK);
    }


    @RequestMapping(value = "/getUserInformation")
    public ResponseEntity getUserInformation(@RequestParam String lastname) {
        User user = userService.getUserByLastname(lastname);
        return new ResponseEntity<>(user.toString(), HttpStatus.OK);
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

    //
//    UserStock Requests
//
    @RequestMapping(value = "/addUserStock")
    public ResponseEntity addUserStock(@RequestParam String mail,
                                       @RequestParam String password,
                                       @RequestParam String stockSymbol) {
        if (checkUser(mail, password).getStatusCode().equals(HttpStatus.OK)) {
            List<UserStock> userStocks = userStockService.getAllUserStocks();
            for (UserStock userStock : userStocks) {
                if (userStock.getMail().equals(mail) && userStock.getStockSymbol().equals(stockSymbol)) {
                    return new ResponseEntity<>(mail + " already subscribed to " + stockSymbol, HttpStatus.NOT_ACCEPTABLE);
                }
            }
            UserStock newUserStock = new UserStock(mail, stockSymbol);
            userStockService.createUserStock(newUserStock);
        }
        else{
            return new ResponseEntity<>("User does not exist", HttpStatus.OK)
        }
        return new ResponseEntity<>("Added " + stockSymbol + " subscription to " + mail, HttpStatus.OK);
    }

    @RequestMapping(value = "/getStocksForUser")
    public ResponseEntity getStockForUser(@RequestParam String mail,
                                          @RequestParam String password) {
        if (checkUser(mail, password).getStatusCode().equals(HttpStatus.OK)) {
            List<UserStock> userStocks = userStockService.getAllUserStocks();
            List<UserStock> userStocksForUser = null;
            for (UserStock userStock : userStocks) {
                if (userStock.getMail().equals(mail)) {
                    userStocksForUser.add(userStock);
                }
            }
            return new ResponseEntity<>(userStocksForUser, HttpStatus.OK);
        }
        return new ResponseEntity<>("User not found", HttpStatus.NOT_ACCEPTABLE);
    }

    @RequestMapping(value = "/deleteUserStock")
    public ResponseEntity deleteUserStock(@RequestParam String mail,
                                          @RequestParam String password,
                                          @RequestParam String stockSymbol) {
        if (checkUser(mail, password).getStatusCode().equals(HttpStatus.OK)) {
            List<UserStock> userStocks = userStockService.getAllUserStocks();
            for (UserStock userStock : userStocks) {
                if (userStock.getMail().equals(mail) && userStock.getStockSymbol().equals(stockSymbol)) {

                    return new ResponseEntity<>(userStockService.deleteUserStock(mail, stockSymbol), HttpStatus.OK);
                }
            }
            return new ResponseEntity<>(mail + " not subscribed to " + stockSymbol, HttpStatus.NOT_ACCEPTABLE);
        }
        return new ResponseEntity<>("User not found", HttpStatus.NOT_ACCEPTABLE);
    }

    @RequestMapping(value = "/getAllUserStocks")
    public ResponseEntity getAllUserStocks() {
        List<UserStock> userStocks = userStockService.getAllUserStocks();
        return new ResponseEntity<>(userStocks, HttpStatus.OK);
    }
}

