package com.stockInformationProcurer.services;

import com.stockInformationProcurer.entity.UserEntity;
import com.stockInformationProcurer.repository.UserInformationRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class UserRepositoryService {

    UserInformationRepository userInformationRepository;

    @Autowired
    public UserRepositoryService(UserInformationRepository userInformationRepository) {
        this.userInformationRepository = userInformationRepository;
    }

    public String getUserInformationForLastname(String lastname) {
        return userInformationRepository.findByLastname(lastname).toString();
    }

    public void addUserInformation(UserEntity userEntity) {
        if (this.userInformationRepository.findByLastname(userEntity.getLastname()) == null)
            this.userInformationRepository.save(userEntity);
    }
}
