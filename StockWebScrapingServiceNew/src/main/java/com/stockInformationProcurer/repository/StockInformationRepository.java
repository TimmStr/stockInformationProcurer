package com.stockInformationProcurer.repository;


import com.stockInformationProcurer.entity.StockEntity;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.data.mongodb.repository.ReactiveMongoRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Mono;

@Repository
public interface StockInformationRepository extends ReactiveMongoRepository<StockEntity, String> {
    @Query("{'symbol': ?0}")
    Mono<StockEntity> findBySymbol(String symbol);
}
