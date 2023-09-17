package com.stockInformationProcurer.services;

import com.stockInformationProcurer.entity.UserStock;
import com.stockInformationProcurer.repository.UserStockRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class UserStockService {
    @Autowired
    private UserStockRepository userStocksRepository;

    public UserStock createUserStock(UserStock userstock) {
        return userStocksRepository.save(userstock);
    }


    public List<UserStock> getAllUserStocks() {
        return userStocksRepository.findAll();
    }


    public Optional<UserStock> getUserStockById(Long id) {
        return userStocksRepository.findById(id);
    }

    public UserStock getUserStocksByMail(String mail) {
        return userStocksRepository.findByMail(mail);
    }

    public UserStock getUserStockByStockSymbol(String stockSymbol) {
        return userStocksRepository.findByStockSymbol(stockSymbol);
    }

    public String deleteUserStock(String mail, String stockSymbol) {
        UserStock userStock = userStocksRepository.findByMailAndStockSymbol(mail, stockSymbol);
        userStocksRepository.delete(userStock);
        return "Deleted "+stockSymbol+ "for "+mail;
    }
}
