// exception/UserNotFoundException.java
package com.studybuddy.exception;

public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(String message) {
        super(message);
    }
}
