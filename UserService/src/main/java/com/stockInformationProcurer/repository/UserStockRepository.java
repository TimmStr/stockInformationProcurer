/**
 * The `UserStockRepository` interface defines the contract for interacting with the database
 * to perform CRUD (Create, Read, Update, Delete) operations related to the `UserStock` entity.
 * It extends the JpaRepository interface provided by Spring Data JPA, which provides
 * common database operations out of the box.
 * <p>
 * This interface allows developers to perform database operations on the `UserStock` entity,
 * such as finding user stocks by email or stock symbol, deleting user stocks by email and stock symbol,
 * and finding user stocks by stock symbol and email.
 *
 * @param <UserStock> The type of entity, which in this case is the `UserStock` entity.
 * @param <Long>      The type of the primary key for the `UserStock` entity, which is a Long.
 */
package com.stockInformationProcurer.repository;

import com.stockInformationProcurer.entity.UserStock;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

public interface UserStockRepository extends JpaRepository<UserStock, Long> {
    /**
     * Finds user stocks by their email address.
     *
     * @param mail The email address of the user for which user stocks are to be retrieved.
     * @return The user stocks associated with the specified email address, or null if not found.
     */
    List<UserStock> findByMail(String mail);

    /**
     * Finds user stocks by their stock symbol.
     *
     * @param stock_symbol The stock symbol for which user stocks are to be retrieved.
     * @return The user stocks associated with the specified stock symbol, or null if not found.
     */
    UserStock findByStockSymbol(String stock_symbol);

    /**
     * Finds user stocks by both their email address and stock symbol.
     *
     * @param mail         The email address of the user for which user stocks are to be retrieved.
     * @param stock_symbol The stock symbol for which user stocks are to be retrieved.
     * @return The user stock entity associated with the specified email address and stock symbol, or null if not found.
     */
    UserStock findByMailAndStockSymbol(String mail, String stock_symbol);

    @Transactional
    void deleteByMail(String mail);

}
