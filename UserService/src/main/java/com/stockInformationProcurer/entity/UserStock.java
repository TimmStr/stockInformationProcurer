/**
 * The `UserStock` class represents a user-stock entity in the application.
 * It is annotated as an entity to be mapped to a postgres database table named "user-stocks."
 * This class defines the structure and properties of a user-stock, including their mail and stock symbol.
 * <p>
 * The class uses Lombok annotations such as @Data to automatically generate getters, setters, equals, hashCode,
 * and toString methods for its fields, reducing boilerplate code.
 *
 * @Entity indicates that instances of this class are JPA entities, making them eligible for database persistence.
 * @Table(name = "user-stocks") specifies the name of the postgres database table where user-stock records are stored.
 * @Data is a Lombok annotation that generates getter and setter methods for class fields.
 */
package com.stockInformationProcurer.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Table;
import lombok.Data;
import org.springframework.data.annotation.Id;

@Entity
@Table(name = "user-stocks")
@Data
public class UserStock {

    /**
     * The unique identifier for the user-stock.
     */
    @jakarta.persistence.Id
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * The email address of the user.
     */
    private String mail;
    /**
     * The stock symbol that creates a connection between the stock and the user
     */
    private String stockSymbol;

    /**
     * Constructs a new UserStock object with the specified attributes.
     *
     * @param mail         The email address of the user.
     * @param stock_symbol The stock symbol that creates a connection between the stock and the user
     */
    public UserStock(String mail, String stock_symbol) {
        this.mail = mail;
        this.stockSymbol = stock_symbol;
    }

    /**
     * Constructs a new UserStock object with no attributes.
     */
    public UserStock() {

    }
}
