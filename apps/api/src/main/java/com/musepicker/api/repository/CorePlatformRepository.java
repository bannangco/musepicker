package com.musepicker.api.repository;

import java.util.List;
import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;

import com.musepicker.api.domain.core.CorePlatform;

public interface CorePlatformRepository extends JpaRepository<CorePlatform, UUID> {
    List<CorePlatform> findByEnabledTrueOrderByNameAsc();
}
