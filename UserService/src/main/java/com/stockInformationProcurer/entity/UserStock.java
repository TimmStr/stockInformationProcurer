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
    @jakarta.persistence.Id
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String mail;
    private String stockSymbol;
    public UserStock(String mail, String stock_symbol) {
        this.mail = mail;
        this.stockSymbol = stock_symbol;
    }

    public UserStock() {

    }
}
