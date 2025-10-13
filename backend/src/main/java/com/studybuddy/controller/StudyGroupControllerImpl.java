// controller/StudyGroupControllerImpl.java
package com.studybuddy.controller;

import com.studybuddy.dto.StudyGroupDTO;
import com.studybuddy.model.StudyGroup;
import com.studybuddy.model.User;
import com.studybuddy.service.StudyGroupService;
import com.studybuddy.service.UserService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/groups")
public class StudyGroupControllerImpl implements StudyGroupController {

    @Autowired
    private StudyGroupService groupService;

    @Autowired
    private UserService userService;

    @PostMapping("/create")
    public StudyGroup createGroup(@RequestBody StudyGroupDTO dto) {
        List<User> members = dto.getMemberEmails().stream()
                .map(email -> userService.getUserByEmail(email).orElse(null))
                .filter(u -> u != null)
                .collect(Collectors.toList());
        return groupService.createGroup(dto.getCourse(), members);
    }

    @PostMapping("/{groupId}/add/{email}")
    public void addMember(@PathVariable String groupId, @PathVariable String email) {
        User user = userService.getUserByEmail(email).orElse(null);
        if (user != null) {
            groupService.addMember(groupService.getGroupById(groupId), user);
        }
    }

    @PostMapping("/{groupId}/remove/{email}")
    public void removeMember(@PathVariable String groupId, @PathVariable String email) {
        User user = userService.getUserByEmail(email).orElse(null);
        if (user != null) {
            groupService.removeMember(groupService.getGroupById(groupId), user);
        }
    }
}
