package com.stockInformationProcurer.entity;

import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

@Document("users")
@Data
public class UserEntity {
    @Id
    private String id;
    @Field(name = "firstname")
    private String firstname;
    @Field(name = "lastname")
    private String lastname;
    @Field(name = "mail")
    private String mail;
    @Field(name = "password")
    private String password;

    public UserEntity(String firstname, String lastname, String mail, String password) {
        this.firstname = firstname;
        this.lastname = lastname;
        this.mail = mail;
        this.password = password;
    }
}