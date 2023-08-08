package com.stockInformationProcurer.repository;


import com.stockInformationProcurer.entity.StockEntity;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface StockInformationRepository extends MongoRepository<StockEntity, String> {
    StockEntity findBySymbol(String symbol);
}
