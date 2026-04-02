package com.musepicker.api.domain.core;

import java.time.Instant;
import java.time.LocalDate;
import java.util.UUID;

import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

@Entity
@Table(name = "core_schedule")
public class CoreSchedule {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column(columnDefinition = "char(36)")
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "activity_id")
    private CoreActivity activity;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "venue_id")
    private CoreVenue venue;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "ticket_type_id")
    private CoreTicketType ticketType;

    @Column(name = "start_date", nullable = false)
    private LocalDate startDate;

    @Column(name = "selling_start")
    private Instant sellingStart;

    @Column(name = "selling_end")
    private Instant sellingEnd;

    @Column(name = "max_pax")
    private Integer maxPax;

    public UUID getId() {
        return id;
    }

    public CoreActivity getActivity() {
        return activity;
    }

    public void setActivity(CoreActivity activity) {
        this.activity = activity;
    }

    public CoreVenue getVenue() {
        return venue;
    }

    public void setVenue(CoreVenue venue) {
        this.venue = venue;
    }

    public CoreTicketType getTicketType() {
        return ticketType;
    }

    public void setTicketType(CoreTicketType ticketType) {
        this.ticketType = ticketType;
    }

    public LocalDate getStartDate() {
        return startDate;
    }

    public void setStartDate(LocalDate startDate) {
        this.startDate = startDate;
    }

    public Instant getSellingStart() {
        return sellingStart;
    }

    public void setSellingStart(Instant sellingStart) {
        this.sellingStart = sellingStart;
    }

    public Instant getSellingEnd() {
        return sellingEnd;
    }

    public void setSellingEnd(Instant sellingEnd) {
        this.sellingEnd = sellingEnd;
    }

    public Integer getMaxPax() {
        return maxPax;
    }

    public void setMaxPax(Integer maxPax) {
        this.maxPax = maxPax;
    }
}
