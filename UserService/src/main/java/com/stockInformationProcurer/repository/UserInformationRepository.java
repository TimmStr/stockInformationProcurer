package com.stockInformationProcurer.repository;

import com.stockInformationProcurer.entity.UserEntity;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface UserInformationRepository extends MongoRepository<UserEntity, String> {
    UserEntity findByLastname(String lastname);
}
