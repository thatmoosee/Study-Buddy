// User.java
package com.studybuddy.model;

import java.util.List;

public class User {
    private String id;
    private String name;
    private String email;
    private Profile profile;
    private List<StudyGroup> groups;

    // Constructor
    public User(String id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }

    // Getters and setters
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public Profile getProfile() { return profile; }
    public void setProfile(Profile profile) { this.profile = profile; }

    public List<StudyGroup> getGroups() { return groups; }
    public void setGroups(List<StudyGroup> groups) { this.groups = groups; }
}
