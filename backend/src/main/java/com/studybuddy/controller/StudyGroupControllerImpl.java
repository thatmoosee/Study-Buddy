// controller/StudyGroupControllerImpl.java
package com.studybuddy.controller;

import com.studybuddy.dto.StudyGroupDTO;
import com.studybuddy.model.StudyGroup;
import com.studybuddy.model.User;
import com.studybuddy.service.StudyGroupService;
import com.studybuddy.service.UserService;

import java.util.List;
import java.util.stream.Collectors;

public class StudyGroupControllerImpl implements StudyGroupController {

    private StudyGroupService groupService;

    private UserService userService;

    public StudyGroup createGroup(@RequestBody StudyGroupDTO dto) {
        List<User> members = dto.getMemberEmails().stream()
                .map(email -> userService.getUserByEmail(email).orElse(null))
                .filter(u -> u != null)
                .collect(Collectors.toList());
        return groupService.createGroup(dto.getCourse(), members);
    }

    public void addMember(@PathVariable String groupId, @PathVariable String email) {
        User user = userService.getUserByEmail(email).orElse(null);
        if (user != null) {
            groupService.addMember(groupService.getGroupById(groupId), user);
        }
    }

    public void removeMember(@PathVariable String groupId, @PathVariable String email) {
        User user = userService.getUserByEmail(email).orElse(null);
        if (user != null) {
            groupService.removeMember(groupService.getGroupById(groupId), user);
        }
    }
}
