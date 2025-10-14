// dto/StudyGroupDTO.java
package com.studybuddy.dto;

import java.util.List;

public class StudyGroupDTO {
    private String course;
    private List<String> memberEmails;

    // Constructors
    public StudyGroupDTO() {}
    public StudyGroupDTO(String course, List<String> memberEmails) {
        this.course = course;
        this.memberEmails = memberEmails;
    }

    // Getters and setters
    public String getCourse() { return course; }
    public void setCourse(String course) { this.course = course; }
    public List<String> getMemberEmails() { return memberEmails; }
    public void setMemberEmails(List<String> memberEmails) { this.memberEmails = memberEmails; }
}
