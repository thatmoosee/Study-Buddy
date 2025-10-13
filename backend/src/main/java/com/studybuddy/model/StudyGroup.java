// StudyGroup.java
package com.studybuddy.model;

import java.util.List;

public class StudyGroup {
    private String groupId;
    private String course;
    private List<User> members;

    public StudyGroup(String groupId, String course) {
        this.groupId = groupId;
        this.course = course;
    }

    // Getters and setters
    public String getGroupId() { return groupId; }
    public void setGroupId(String groupId) { this.groupId = groupId; }

    public String getCourse() { return course; }
    public void setCourse(String course) { this.course = course; }

    public List<User> getMembers() { return members; }
    public void setMembers(List<User> members) { this.members = members; }
}
