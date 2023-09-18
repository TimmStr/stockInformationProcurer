/**
 * The `UserStockService` class provides service methods for managing user stock subscriptions.
 * It interacts with the postgres database through the `UserStockRepository` to perform operations such as
 * creating user stock subscriptions, retrieving all user stock subscriptions, and deleting user stock subscriptions.
 * <p>
 * This service class is annotated with `@Service`, indicating that it is a Spring-managed service component.
 * It is responsible for handling business logic related to user stock subscriptions.
 */
package com.stockInformationProcurer.services;

import com.stockInformationProcurer.entity.UserStock;
import com.stockInformationProcurer.repository.UserStockRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class UserStockService {
    @Autowired
    private UserStockRepository userStocksRepository;

    /**
     * Creates a new user stock subscription in the database.
     *
     * @param userstock The UserStock object representing the user stock subscription to be created.
     * @return The created UserStock object.
     */
    public UserStock createUserStock(UserStock userstock) {
        return userStocksRepository.save(userstock);
    }

    /**
     * Retrieves a list of all user stock subscriptions from the database.
     *
     * @return A list of UserStock objects representing all user stock subscriptions.
     */
    public List<UserStock> getAllUserStocks() {
        return userStocksRepository.findAll();
    }

    /**
     * Deletes a user stock subscription based on the user's email address and stock symbol.
     *
     * @param mail        The email address of the user.
     * @param stockSymbol The stock symbol of the user stock subscription to be deleted.
     * @return A message indicating the deletion status, including the deleted stock symbol and user email.
     */
    public String deleteUserStock(String mail, String stockSymbol) {
        UserStock userStock = userStocksRepository.findByMailAndStockSymbol(mail, stockSymbol);
        userStocksRepository.delete(userStock);
        return "Deleted " + stockSymbol + " for " + mail;
    }


    /**
     * Retrieves a list of user stock subscriptions based on the user's email address.
     *
     * @param mail The email address of the user.
     * @return A list of UserStock objects representing the user's stock subscriptions.
     */
    public List<UserStock> getUserStocksByMail(String mail) {
        return userStocksRepository.findByMail(mail);
    }

    /**
     * Deletes all user stock subscriptions based on the user's email address.
     *
     * @param mail The email address of the user.
     */
    public void deleteUserStocksByMail(String mail) {
        userStocksRepository.deleteByMail(mail);
    }
}
