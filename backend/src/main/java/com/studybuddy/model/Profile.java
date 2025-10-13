// Profile.java
package com.studybuddy.model;

import java.util.List;

public class Profile {
    private String major;
    private List<String> availability;

    public Profile(String major, List<String> availability) {
        this.major = major;
        this.availability = availability;
    }

    public String getMajor() { return major; }
    public void setMajor(String major) { this.major = major; }

    public List<String> getAvailability() { return availability; }
    public void setAvailability(List<String> availability) { this.availability = availability; }
}
