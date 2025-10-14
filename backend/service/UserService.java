// service/UserService.java
package com.studybuddy.service;

import com.studybuddy.model.User;
import com.studybuddy.repository.UserRepository;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepo;

    public User createUser(User user) {
        return userRepo.save(user);
    }

    public Optional<User> getUserByEmail(String email) {
        return userRepo.findByEmail(email);
    }

    public List<User> searchUsersByMajor(String major) {
        return userRepo.findAll().stream()
                .filter(u -> u.getProfile() != null && major.equals(u.getProfile().getMajor()))
                .collect(Collectors.toList());
    }
}
