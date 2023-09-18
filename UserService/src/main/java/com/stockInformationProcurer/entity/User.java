/**
 * The `User` class represents a user entity in the application.
 * It is annotated as an entity to be mapped to a postgres database table named "users."
 * This class defines the structure and properties of a user, including their first name, last name,
 * email, password, and a flag indicating whether they wish to receive email notifications.
 * <p>
 * The class uses Lombok annotations such as @Data to automatically generate getters, setters, equals, hashCode,
 * and toString methods for its fields, reducing boilerplate code.
 *
 * @Entity indicates that instances of this class are JPA entities, making them eligible for database persistence.
 * @Table(name = "users") specifies the name of the postgres database table where user records are stored.
 * @Data is a Lombok annotation that generates getter and setter methods for class fields.
 */
package com.stockInformationProcurer.entity;

import jakarta.persistence.*;
import lombok.Data;
import org.springframework.data.annotation.Id;

@Entity
@Table(name = "users")
@Data
public class User {

    /**
     * The unique identifier for the user.
     */
    @jakarta.persistence.Id
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * The first name of the user.
     */
    private String firstname;

    /**
     * The last name of the user.
     */
    private String lastname;

    /**
     * The email address of the user.
     */
    private String mail;

    /**
     * The password associated with the user's account.
     */
    private String password;

    /**
     * A flag indicating whether the user wishes to receive email notifications.
     */
    private boolean mail_service;

    /**
     * Constructs a new User object with the specified attributes.
     *
     * @param firstname    The first name of the user.
     * @param lastname     The last name of the user.
     * @param mail         The email address of the user.
     * @param password     The password for the user's account.
     * @param mail_service A boolean flag indicating whether the user wishes to receive email notifications.
     */
    public User(String firstname, String lastname, String mail, String password, boolean mail_service) {
        this.firstname = firstname;
        this.lastname = lastname;
        this.mail = mail;
        this.password = password;
        this.mail_service = mail_service;
    }

    /**
     * Default constructor for the User class.
     * It is required for JPA entity mapping and should not be used directly.
     */
    public User() {
    }
}
