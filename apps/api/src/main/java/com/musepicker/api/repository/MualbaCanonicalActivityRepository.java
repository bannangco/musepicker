package com.musepicker.api.repository;

import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;

import com.musepicker.api.domain.mualba.MualbaCanonicalActivity;

public interface MualbaCanonicalActivityRepository extends JpaRepository<MualbaCanonicalActivity, UUID> {
}
