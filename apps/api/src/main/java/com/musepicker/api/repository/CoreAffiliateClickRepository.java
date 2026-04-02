package com.musepicker.api.repository;

import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;

import com.musepicker.api.domain.core.CoreAffiliateClick;

public interface CoreAffiliateClickRepository extends JpaRepository<CoreAffiliateClick, UUID> {
}
