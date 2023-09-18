/**
 * The `UserRepository` interface defines the contract for interacting with the database
 * to perform CRUD (Create, Read, Update, Delete) operations related to the `User` entity.
 * It extends the JpaRepository interface provided by Spring Data JPA, which provides
 * common database operations out of the box.
 * <p>
 * This interface allows developers to perform database operations on the `User` entity,
 * such as finding users by email or last name and deleting users by email.
 *
 * @param <User> The type of entity, which in this case is the `User` entity.
 * @param <Long> The type of the primary key for the `User` entity, which is a Long.
 */
package com.stockInformationProcurer.repository;

import com.stockInformationProcurer.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.transaction.annotation.Transactional;

public interface UserRepository extends JpaRepository<User, Long> {

    /**
     * Finds a user by their email address.
     *
     * @param mail The email address of the user to be retrieved.
     * @return The user entity with the specified email address, or null if not found.
     */
    User findByMail(String mail);


    /**
     * Deletes a user by their email address.
     *
     * @param mail The email address of the user to be deleted.
     */
    @Transactional
    void deleteByMail(String mail);


    /**
     * Finds a user by their last name.
     *
     * @param lastname The last name of the user to be retrieved.
     * @return The user entity with the specified last name, or null if not found.
     */
    User findByLastname(String lastname);
}
