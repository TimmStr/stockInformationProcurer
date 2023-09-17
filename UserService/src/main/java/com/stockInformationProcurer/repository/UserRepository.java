package com.stockInformationProcurer.repository;

import com.stockInformationProcurer.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepository extends JpaRepository<User, Long>{
    User findByMail(String mail);
    User deleteByMail(String mail);
    User findByLastname(String lastname);
}
