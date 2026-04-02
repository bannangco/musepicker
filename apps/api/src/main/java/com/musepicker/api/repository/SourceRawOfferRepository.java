package com.musepicker.api.repository;

import java.util.Optional;
import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;

import com.musepicker.api.domain.source.SourceRawOffer;

public interface SourceRawOfferRepository extends JpaRepository<SourceRawOffer, UUID> {
    Optional<SourceRawOffer> findByIdempotencyKey(String idempotencyKey);
}
