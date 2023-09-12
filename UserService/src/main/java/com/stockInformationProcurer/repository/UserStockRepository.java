package com.stockInformationProcurer.repository;

import com.stockInformationProcurer.entity.UserStock;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserStockRepository extends JpaRepository<UserStock, Long> {
    UserStock findByMail(String mail);
    UserStock deleteByMailAndStockSymbol(String mail, String stock_symbol);
    UserStock findByStockSymbol(String stock_symbol);
    UserStock findByMailAndStockSymbol(String mail, String stock_symbol);
}
