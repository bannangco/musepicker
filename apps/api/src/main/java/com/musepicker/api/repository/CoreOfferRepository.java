package com.musepicker.api.repository;

import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import com.musepicker.api.domain.core.CoreOffer;

public interface CoreOfferRepository extends JpaRepository<CoreOffer, UUID> {

    @Query("""
        select o from CoreOffer o
        join fetch o.activity a
        join fetch a.region r
        join fetch o.platform p
        left join fetch o.ticketType tt
        left join fetch o.schedule s
        where (:city is null or lower(r.city) = lower(:city))
          and (:category is null or lower(a.categoriesCsv) like lower(concat('%', :category, '%')))
          and (:query is null or lower(a.name) like lower(concat('%', :query, '%')) or lower(a.description) like lower(concat('%', :query, '%')))
          and (:date is null or s.startDate = :date)
    """)
    List<CoreOffer> searchOffers(
        @Param("city") String city,
        @Param("category") String category,
        @Param("query") String query,
        @Param("date") LocalDate date
    );

    @Query("""
        select o from CoreOffer o
        join fetch o.activity a
        join fetch o.platform p
        left join fetch o.ticketType tt
        left join fetch o.schedule s
        where a.id = :activityId
          and (:date is null or s.startDate = :date)
    """)
    List<CoreOffer> findByActivityAndDate(@Param("activityId") UUID activityId, @Param("date") LocalDate date);

    @Query("""
        select o from CoreOffer o
        join fetch o.activity a
        join fetch o.platform p
        left join fetch o.ticketType tt
        left join fetch o.schedule s
    """)
    List<CoreOffer> findAllForTrending();
}
