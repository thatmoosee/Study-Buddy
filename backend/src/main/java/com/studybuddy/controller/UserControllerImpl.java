// controller/UserControllerImpl.java
package com.studybuddy.controller;

import com.studybuddy.dto.UserDTO;
import com.studybuddy.model.Profile;
import com.studybuddy.model.User;
import com.studybuddy.service.UserService;
import com.studybuddy.exception.UserNotFoundException;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/users")
public class UserControllerImpl implements UserController {

    @Autowired
    private UserService userService;

    @PostMapping("/create")
    public User createUser(@RequestBody UserDTO dto) {
        Profile profile = new Profile(dto.getMajor(), dto.getAvailability());
        User user = new User(UUID.randomUUID().toString(), dto.getName(), dto.getEmail());
        user.setProfile(profile);
        return userService.createUser(user);
    }

    @GetMapping("/{email}")
    public User getUser(@PathVariable String email) {
        return userService.getUserByEmail(email)
                .orElseThrow(() -> new UserNotFoundException("User not found: " + email));
    }

    @GetMapping("/search")
    public List<User> searchUsers(@RequestParam String major) {
        return userService.searchUsersByMajor(major);
    }
}
