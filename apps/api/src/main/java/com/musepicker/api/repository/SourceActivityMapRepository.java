package com.musepicker.api.repository;

import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;

import com.musepicker.api.domain.source.SourceActivityMap;

public interface SourceActivityMapRepository extends JpaRepository<SourceActivityMap, UUID> {
}
