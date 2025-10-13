// repository/UserRepository.java
package com.studybuddy.repository;

import com.studybuddy.model.User;
import java.util.*;

import org.springframework.stereotype.Repository;

@Repository
public class UserRepository {
    private final Map<String, User> users = new HashMap<>();

    public User save(User user) {
        users.put(user.getEmail(), user);
        return user;
    }

    public Optional<User> findByEmail(String email) {
        return Optional.ofNullable(users.get(email));
    }

    public List<User> findAll() {
        return new ArrayList<>(users.values());
    }
}
