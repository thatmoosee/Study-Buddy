// repository/StudyGroupRepository.java
package com.studybuddy.repository;

import com.studybuddy.model.StudyGroup;
import java.util.*;

import org.springframework.stereotype.Repository;

@Repository
public class StudyGroupRepository {
    private final Map<String, StudyGroup> groups = new HashMap<>();

    public StudyGroup save(StudyGroup group) {
        groups.put(group.getGroupId(), group);
        return group;
    }

    public Optional<StudyGroup> findById(String id) {
        return Optional.ofNullable(groups.get(id));
    }

    public List<StudyGroup> findAll() {
        return new ArrayList<>(groups.values());
    }
}
