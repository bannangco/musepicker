package com.musepicker.api.repository;

import java.util.List;
import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import com.musepicker.api.domain.core.CoreActivity;

public interface CoreActivityRepository extends JpaRepository<CoreActivity, UUID> {

    @Query("""
        select a from CoreActivity a
        join fetch a.region
    """)
    List<CoreActivity> findAllWithRegion();

    @Query("""
        select a from CoreActivity a
        join fetch a.region r
        where (:city is null or lower(r.city) = lower(:city))
          and (:query is null or lower(a.name) like lower(concat('%', :query, '%')) or lower(a.description) like lower(concat('%', :query, '%')))
          and (:category is null or lower(a.categoriesCsv) like lower(concat('%', :category, '%')))
    """)
    List<CoreActivity> search(@Param("city") String city, @Param("category") String category, @Param("query") String query);
}
