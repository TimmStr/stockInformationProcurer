/**
 * The `UserService` class provides service methods for managing user-related operations.
 * It interacts with the database through the `UserRepository` to perform operations such as
 * creating users, retrieving users, updating user passwords, and deleting users.
 * <p>
 * This service class is annotated with `@Service`, indicating that it is a Spring-managed service component.
 * It is responsible for handling business logic related to users.
 */
package com.stockInformationProcurer.services;

import com.stockInformationProcurer.entity.User;
import com.stockInformationProcurer.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.List;
import java.util.Optional;

@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;

    /**
     * Creates a new user and saves it to the database.
     *
     * @param user The User object representing the user to be created.
     * @return The created User object.
     */
    public User createUser(User user) throws NoSuchAlgorithmException {
        user.setPassword(getMD5Hash(user.getPassword()));
        return userRepository.save(user);
    }

    /**
     * Retrieves a list of all users from the database.
     *
     * @return A list of User objects representing all users.
     */
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }

    /**
     * Retrieves a user by their last name.
     *
     * @param lastname The last name of the user to be retrieved.
     * @return The user entity with the specified last name, or null if not found.
     */
    public User getUserByLastname(String lastname) {
        return userRepository.findByLastname(lastname);
    }

    /**
     * Retrieves a user by their email address.
     *
     * @param mail The email address of the user to be retrieved.
     * @return The user entity with the specified email address, or null if not found.
     */
    public User getUserByMail(String mail) {
        return userRepository.findByMail(mail);
    }

    /**
     * Updates a user's password based on their email address, old password, and new password.
     *
     * @param mail         The email address of the user.
     * @param old_password The old password for the user's account to confirm the authenticity.
     * @param new_password The new password to set for the user's account.
     * @return The updated user entity if the password is successfully updated, or null if not found
     *         or the old password is incorrect.
     */
    public User updateUserPassword(String mail, String old_password, String new_password) throws NoSuchAlgorithmException {
        Optional<User> user = Optional.ofNullable(userRepository.findByMail(mail));
        if (user.isPresent()) {
            User existingUser = user.get();
            if (verifyPassword(old_password, existingUser.getPassword())) {
                existingUser.setPassword(getMD5Hash(new_password));
                return userRepository.save(existingUser);
            }
        }
        return null;
    }

    /**
     * Deletes all users from the database.
     */
    public void deleteAllUsers() {
        userRepository.deleteAll();
    }

    /**
     * Deletes a user by their email address.
     *
     * @param mail The email address of the user to be deleted.
     */
    public void deleteUserByMail(String mail) {
        userRepository.deleteByMail(mail);
    }


    public String getMD5Hash(String input) throws NoSuchAlgorithmException {
        MessageDigest md = MessageDigest.getInstance("MD5");
        md.update(input.getBytes());
        byte[] digest = md.digest();
        StringBuilder hashString = new StringBuilder();

        for (byte b : digest) {
            hashString.append(String.format("%02x", b));
        }

        return hashString.toString();
    }

    public boolean verifyPassword(String inputPassword, String storedHash) throws NoSuchAlgorithmException {
        String hashedInput = getMD5Hash(inputPassword);
        return hashedInput.equals(storedHash);
    }
}
