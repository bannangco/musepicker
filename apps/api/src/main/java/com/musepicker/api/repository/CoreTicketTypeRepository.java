package com.musepicker.api.repository;

import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;

import com.musepicker.api.domain.core.CoreTicketType;

public interface CoreTicketTypeRepository extends JpaRepository<CoreTicketType, UUID> {
}
