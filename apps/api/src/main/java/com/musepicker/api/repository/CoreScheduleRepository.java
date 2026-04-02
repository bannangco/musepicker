package com.musepicker.api.repository;

import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;

import com.musepicker.api.domain.core.CoreSchedule;

public interface CoreScheduleRepository extends JpaRepository<CoreSchedule, UUID> {
}
