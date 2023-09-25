/**
 * The `UserController` class is responsible for managing user data and user shares in a system.
 * It provides endpoints for various user actions such as adding users,
 * collecting user information and managing user shares.
 *
 * @author
 * @Version 1.0
 * @since 2023-09-18
 */
package com.stockInformationProcurer.controller;

import com.stockInformationProcurer.entity.User;
import com.stockInformationProcurer.entity.UserStock;
import com.stockInformationProcurer.services.UserService;
import com.stockInformationProcurer.services.UserStockService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.security.NoSuchAlgorithmException;
import java.util.List;

@RestController
public class UserController {

    private final UserService userService;
    private final UserStockService userStockService;


    /**
     * Creates a new instance of the `UserController` class.
     *
     * @param userService      The service for managing user data.
     * @param userStockService The service for managing user stocks.
     */
    public UserController(UserService userService, UserStockService userStockService) {
        this.userService = userService;
        this.userStockService = userStockService;
    }


    /**
     * Retrieves a list of all users from the database.
     *
     * @return A list of User objects representing all users in the database.
     */
    public List<User> getAllUsersFromDatabase() {
        return userService.getAllUsers();
    }


    /**
     * Retrieves a list of all users from the database.
     *
     * @return A ResponseEntity containing a list of User objects representing all users in the database
     * with HTTP status OK if successful.
     */
    @RequestMapping(value = "/getAllUsers", method = RequestMethod.GET)
    public ResponseEntity getAllUsers() {
        List<User> users = getAllUsersFromDatabase();
        return new ResponseEntity<>(users, HttpStatus.OK);
    }


    /**
     * Retrieves user information based on the provided last name.
     *
     * @param lastname The last name of the user to retrieve information for.
     * @return A ResponseEntity containing the user information in string format if found, or an error message
     * with HTTP status NOT_FOUND if the user with the provided last name does not exist.
     */
    @RequestMapping(value = "/getUserByLastname", method = RequestMethod.GET)
    public ResponseEntity getUserByLastname(@RequestParam String lastname) {
        User user = userService.getUserByLastname(lastname);
        return new ResponseEntity<>(user, HttpStatus.OK);
    }


    /**
     * Retrieves user information based on the provided mail.
     *
     * @param mail The last name of the user to retrieve information for.
     * @return A ResponseEntity containing the user information in string format if found, or an error message
     * with HTTP status NOT_FOUND if the user with the provided last name does not exist.
     */
    @RequestMapping(value = "/getUserByMail", method = RequestMethod.GET)
    public ResponseEntity getUserByMail(@RequestParam String mail) {
        User user = userService.getUserByMail(mail);
        return new ResponseEntity<>(user, HttpStatus.OK);
    }


    /**
     * Checks the user's credentials by verifying the provided email and password.
     *
     * @param mail     The email address of the user.
     * @param password The password for the user's account.
     * @return A ResponseEntity containing the user object if the credentials are valid with HTTP status OK,
     * or an error message with HTTP status NOT_ACCEPTABLE if the credentials are invalid or the user is not found.
     */
    @RequestMapping(value = "/checkUser", method = RequestMethod.GET)
    public ResponseEntity checkUser(@RequestParam String mail, @RequestParam String password) throws NoSuchAlgorithmException {
        List<User> users = userService.getAllUsers();
        for (User user : users) {
            if (user.getMail().equals(mail) && userService.verifyPassword(password, user.getPassword())) {
                return new ResponseEntity<>(user, HttpStatus.OK);
            }
        }
        return new ResponseEntity<>("User not found", HttpStatus.NOT_ACCEPTABLE);
    }


    /**
     * Adds a new user to the system with the provided information.
     *
     * @param firstname    The first name of the user.
     * @param lastname     The last name of the user.
     * @param mail         The email address of the user.
     * @param password     The password for the user's account.
     * @param mail_service A boolean flag indicating whether the user wants to receive email notifications.
     * @return A ResponseEntity containing a success message if the user was added successfully,
     * or an error message with HTTP status NOT_ACCEPTABLE if the user already exists.
     */
    @RequestMapping(value = "/addUser", method = RequestMethod.PUT)
    public ResponseEntity addUser(@RequestParam String firstname,
                                  @RequestParam String lastname,
                                  @RequestParam String mail,
                                  @RequestParam String password,
                                  @RequestParam boolean mail_service) throws NoSuchAlgorithmException {
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


    /**
     * Updates the password for a user with the provided email address.
     *
     * @param mail         The email address of the user.
     * @param old_password The old password for the user's account.
     * @param new_password The new password to set for the user's account.
     * @return A ResponseEntity containing the updated user object if the password is successfully updated with HTTP status OK,
     * or an error message with HTTP status NOT_ACCEPTABLE if the user is not found or the old password is incorrect.
     */
    @RequestMapping(value = "/updateUserPassword", method = RequestMethod.PUT)
    public ResponseEntity updateUserPassword(@RequestParam String mail, @RequestParam String old_password, @RequestParam String new_password) throws NoSuchAlgorithmException {
        User user = userService.updateUserPassword(mail, old_password, new_password);
        if (user != null) {
            return new ResponseEntity<>(user, HttpStatus.OK);
        }
        return new ResponseEntity<>("User not found", HttpStatus.NOT_ACCEPTABLE);
    }

    /**
     * Deletes all users.
     *
     * @return A ResponseEntity containing a success message if all users have been successfully deleted with HTTP status OK,
     * or an error message with HTTP status NOT_ACCEPTABLE if the users were not found.
     */
    @RequestMapping(value = "/deleteAllUsers", method = RequestMethod.GET)
    public ResponseEntity deleteUsers() {
        userService.deleteAllUsers();
        return new ResponseEntity<>("Users have been deleted", HttpStatus.OK);
    }


    /**
     * Deletes a user with the provided email address.
     *
     * @param mail     The email address of the user and the password.
     * @param password The password to confirm the deletion.
     * @return A ResponseEntity containing a success message if the user has been successfully deleted with HTTP status OK,
     * or an error message with HTTP status NOT_ACCEPTABLE if the user was not found.
     */
    @RequestMapping(value = "/deleteUserByMail", method = RequestMethod.GET)
    public ResponseEntity deleteUserByMail(@RequestParam String mail, @RequestParam String password) throws NoSuchAlgorithmException {
        if (checkUser(mail, password).getStatusCode().equals(HttpStatus.OK)) {
            userStockService.deleteUserStocksByMail(mail);
            userService.deleteUserByMail(mail);
            return new ResponseEntity<>("User deleted", HttpStatus.OK);
        }
        return new ResponseEntity<>("User not found", HttpStatus.NOT_ACCEPTABLE);
    }


    /**
     * Retrieves a list of all user stocks from the database.
     *
     * @return A ResponseEntity containing a list of UserStock objects representing all user stocks in the database
     * with HTTP status OK if successful.
     */
    @RequestMapping(value = "/getAllUserStocks", method = RequestMethod.GET)
    public ResponseEntity getAllUserStocks() {
        List<UserStock> userStocks = userStockService.getAllUserStocks();
        return new ResponseEntity<>(userStocks, HttpStatus.OK);
    }


    /**
     * Retrieves a list of all user stocks for the user with the provided email address.
     *
     * @param mail     The email address of the user.
     * @param password The password for the user's account.
     * @return A ResponseEntity containing a list of UserStock objects representing all user stocks for the user
     * with HTTP status OK if successful, or an error message with HTTP status NOT_ACCEPTABLE if the user does not exist.
     */
    @RequestMapping(value = "/getStocksForUser", method = RequestMethod.GET)
    public ResponseEntity getStocksForUser(@RequestParam String mail,
                                           @RequestParam String password) throws NoSuchAlgorithmException {
        if (checkUser(mail, password).getStatusCode().equals(HttpStatus.OK)) {
            List<UserStock> userStocks = userStockService.getUserStocksByMail(mail);
            return new ResponseEntity<>(userStocks, HttpStatus.OK);
        }
        return new ResponseEntity<>("User not found", HttpStatus.NOT_ACCEPTABLE);
    }


    /**
     * Adds a new user stock subscription with the provided user credentials and stock symbol.
     *
     * @param mail        The email address of the user.
     * @param password    The password for the user's account.
     * @param stockSymbol The symbol of the stock to subscribe to.
     * @return A ResponseEntity with a success message if the subscription is added successfully with HTTP status OK,
     * or an error message with HTTP status NOT_ACCEPTABLE if the user does not exist or is already subscribed.
     */
    @RequestMapping(value = "/addUserStock", method = RequestMethod.PUT)
    public ResponseEntity addUserStock(@RequestParam String mail,
                                       @RequestParam String password,
                                       @RequestParam String stockSymbol) throws NoSuchAlgorithmException {
        if (checkUser(mail, password).getStatusCode().equals(HttpStatus.OK)) {
            List<UserStock> userStocks = userStockService.getAllUserStocks();
            for (UserStock userStock : userStocks) {
                if (userStock.getMail().equals(mail) && userStock.getStockSymbol().equals(stockSymbol)) {
                    return new ResponseEntity<>(mail + " already subscribed to " + stockSymbol, HttpStatus.NOT_ACCEPTABLE);
                }
            }
            UserStock newUserStock = new UserStock(mail, stockSymbol);
            userStockService.createUserStock(newUserStock);
        } else {
            return new ResponseEntity<>("User does not exist", HttpStatus.OK);
        }
        return new ResponseEntity<>("Added " + stockSymbol + " subscription to " + mail, HttpStatus.OK);
    }


    /**
     * Deletes a user stock subscription with the provided user credentials and stock symbol.
     *
     * @param mail        The email address of the user.
     * @param password    The password for the user's account.
     * @param stockSymbol The symbol of the stock to unsubscribe from.
     * @return A ResponseEntity with a success message if the subscription is deleted successfully with HTTP status OK,
     * or an error message with HTTP status NOT_ACCEPTABLE if the user does not exist or is not subscribed.
     */
    @RequestMapping(value = "/deleteUserStock", method = RequestMethod.GET)
    public ResponseEntity deleteUserStock(@RequestParam String mail,
                                          @RequestParam String password,
                                          @RequestParam String stockSymbol) throws NoSuchAlgorithmException {
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


    /**
     * Deletes all user stock subscriptions with the provided user credentials.
     *
     * @param mail     The email address of the user.
     * @param password The password for the user's account.
     * @return A ResponseEntity with a success message if the subscription is deleted successfully with HTTP status OK,
     * or an error message with HTTP status NOT_ACCEPTABLE if the user does not exist or is not subscribed.
     */
    @RequestMapping(value = "/deleteUserStocksByMail", method = RequestMethod.GET)
    public ResponseEntity deleteUserStocksByMail(@RequestParam String mail,
                                                 @RequestParam String password) throws NoSuchAlgorithmException {
        if (checkUser(mail, password).getStatusCode().equals(HttpStatus.OK)) {
            userStockService.deleteUserStocksByMail(mail);
            return new ResponseEntity<>("The shares for the customer have been deleted", HttpStatus.OK);
        }
        return new ResponseEntity<>("User not found", HttpStatus.NOT_ACCEPTABLE);
    }
}

