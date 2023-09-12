package com.stockInformationProcurer.services;

import com.stockInformationProcurer.entity.User;
import com.stockInformationProcurer.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;

    public User createUser(User user) {
        return userRepository.save(user);
    }


    public List<User> getAllUsers() {
        return userRepository.findAll();
    }


    public Optional<User> getUserById(Long id) {
        return userRepository.findById(id);
    }

    public User getUserByLastname(String lastname) {
        return userRepository.findByLastname(lastname);
    }

    public User getUserByMail(String mail) {
        return userRepository.findByMail(mail);
    }


    public User updateUserPassword(String mail, String old_password, String new_password) {
        Optional<User> user = Optional.ofNullable(userRepository.findByMail(mail));
        if (user.isPresent()) {
            User existingUser = user.get();
            if (existingUser.getPassword().equals(old_password)) {
                existingUser.setPassword(new_password);
                return userRepository.save(existingUser);
            }
        }
        return null;
    }


    public void deleteAllUsers() {
        userRepository.deleteAll();
    }


    public void deleteUser(String mail) {
        userRepository.deleteByMail(mail);
    }


}
