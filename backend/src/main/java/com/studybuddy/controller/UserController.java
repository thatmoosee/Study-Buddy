// UserController.java
package com.studybuddy.controller;

import com.studybuddy.model.User;

import java.util.List;

public interface UserController {
    User createUser(User user);
    User getUserById(String id);
    List<User> searchUsersByClass(String className);
}
