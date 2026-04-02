package com.musepicker.api.repository;

import java.util.Optional;
import java.util.UUID;
import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import com.musepicker.api.domain.source.SourceRawOffer;

public interface SourceRawOfferRepository extends JpaRepository<SourceRawOffer, UUID> {
    Optional<SourceRawOffer> findByIdempotencyKey(String idempotencyKey);

    @Query("""
        select r.source as source, count(r) as total
        from SourceRawOffer r
        group by r.source
    """)
    List<SourceCountProjection> countBySource();

    interface SourceCountProjection {
        String getSource();
        long getTotal();
    }
}
