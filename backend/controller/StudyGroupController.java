// StudyGroupController.java
package com.studybuddy.controller;

import com.studybuddy.model.StudyGroup;
import com.studybuddy.model.User;

import java.util.List;

public interface StudyGroupController {
    StudyGroup createGroup(String course, List<User> members);
    void addMember(StudyGroup group, User user);
    void removeMember(StudyGroup group, User user);
    List<StudyGroup> getGroupsByUser(User user);
}
