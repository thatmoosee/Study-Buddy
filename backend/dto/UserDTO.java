// dto/UserDTO.java
package com.studybuddy.dto;

import java.util.List;

public class UserDTO {
    private String name;
    private String email;
    private String major;
    private List<String> availability;

    // Constructors
    public UserDTO() {}
    public UserDTO(String name, String email, String major, List<String> availability) {
        this.name = name;
        this.email = email;
        this.major = major;
        this.availability = availability;
    }

    // Getters and setters
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public String getMajor() { return major; }
    public void setMajor(String major) { this.major = major; }
    public List<String> getAvailability() { return availability; }
    public void setAvailability(List<String> availability) { this.availability = availability; }
}
