// service/StudyGroupService.java
package com.studybuddy.service;

import com.studybuddy.model.StudyGroup;
import com.studybuddy.model.User;
import com.studybuddy.repository.StudyGroupRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;

@Service
public class StudyGroupService {

    @Autowired
    private StudyGroupRepository groupRepo;

    public StudyGroup createGroup(String course, List<User> members) {
        StudyGroup group = new StudyGroup(UUID.randomUUID().toString(), course);
        group.setMembers(members);
        return groupRepo.save(group);
    }

    public void addMember(StudyGroup group, User user) {
        group.getMembers().add(user);
    }

    public void removeMember(StudyGroup group, User user) {
        group.getMembers().remove(user);
    }

    public StudyGroup getGroupById(String id) {
        return groupRepo.findById(id).orElse(null);
    }
}
