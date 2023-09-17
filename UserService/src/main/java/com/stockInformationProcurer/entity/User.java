package com.stockInformationProcurer.entity;

import jakarta.persistence.*;
import lombok.Data;
import org.springframework.data.annotation.Id;

@Entity
@Table(name = "users")
@Data
public class User {
    @jakarta.persistence.Id
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String firstname;
    private String lastname;
    private String mail;
    private String password;
    private boolean mail_service;
    public User(String firstname, String lastname, String mail, String password, boolean mail_service) {
        this.firstname = firstname;
        this.lastname = lastname;
        this.mail = mail;
        this.password = password;
        this.mail_service= mail_service;
    }

    public User() {

    }
}
