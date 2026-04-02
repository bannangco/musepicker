package com.musepicker.api.repository;

import java.util.UUID;
import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import com.musepicker.api.domain.source.SourceActivityMap;

public interface SourceActivityMapRepository extends JpaRepository<SourceActivityMap, UUID> {
    @Query("""
        select m.source as source, count(m) as total
        from SourceActivityMap m
        group by m.source
    """)
    List<SourceCountProjection> countBySource();

    @Query("""
        select m from SourceActivityMap m
        where (m.coreActivity is null or m.mualbaActivity is null)
          and (m.manualOverride is null or m.manualOverride = false)
        order by m.source asc, m.sourceActivityId asc
    """)
    List<SourceActivityMap> findReviewQueue();

    Optional<SourceActivityMap> findBySourceAndSourceActivityId(String source, String sourceActivityId);

    interface SourceCountProjection {
        String getSource();
        long getTotal();
    }
}
