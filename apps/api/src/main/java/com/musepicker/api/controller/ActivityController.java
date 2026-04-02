package com.musepicker.api.controller;

import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.musepicker.api.dto.v1.ActivityDetailResponse;
import com.musepicker.api.dto.v1.ActivitySearchItemResponse;
import com.musepicker.api.dto.v1.OfferResponse;
import com.musepicker.api.dto.v1.PagedResponse;
import com.musepicker.api.dto.v1.TrendingActivityResponse;
import com.musepicker.api.service.ActivityQueryService;
import com.musepicker.api.service.SearchCriteria;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;

@RestController
@RequestMapping({"/api/activities", "/activities"})
@Validated
public class ActivityController {

    private final ActivityQueryService activityQueryService;

    public ActivityController(ActivityQueryService activityQueryService) {
        this.activityQueryService = activityQueryService;
    }

    @GetMapping("/trending")
    public List<TrendingActivityResponse> getTrending() {
        return activityQueryService.getTrendingActivities();
    }

    @GetMapping("/search")
    public PagedResponse<ActivitySearchItemResponse> search(
        @RequestParam(required = false) String city,
        @RequestParam(required = false) String category,
        @RequestParam(required = false) String query,
        @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate date,
        @RequestParam(required = false, defaultValue = "1") @Min(1) int pax,
        @RequestParam(required = false, defaultValue = "0") @Min(0) int page,
        @RequestParam(required = false, defaultValue = "20") @Min(1) @Max(100) int size
    ) {
        return activityQueryService.searchActivities(new SearchCriteria(city, category, query, date, pax), page, size);
    }

    @PostMapping("/search")
    public PagedResponse<ActivitySearchItemResponse> searchCompatibility(
        @RequestParam(required = false) String city,
        @RequestParam(required = false) String category,
        @RequestParam(required = false) String query,
        @RequestBody(required = false) LegacyFilterRequest body,
        @RequestParam(required = false, defaultValue = "0") @Min(0) int page,
        @RequestParam(required = false, defaultValue = "20") @Min(1) @Max(100) int size
    ) {
        LocalDate date = body == null ? null : body.date();
        int pax = body == null || body.pax() == null ? 1 : Math.max(body.pax(), 1);
        return activityQueryService.searchActivities(new SearchCriteria(city, category, query, date, pax), page, size);
    }

    @GetMapping("/{activityId}")
    public ActivityDetailResponse getActivity(@PathVariable UUID activityId) {
        return activityQueryService.getActivity(activityId);
    }

    @GetMapping("/{activityId}/offers")
    public List<OfferResponse> getOffers(
        @PathVariable UUID activityId,
        @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate date
    ) {
        return activityQueryService.getOffers(activityId, date);
    }

    @GetMapping("/{activityId}/tickets")
    public List<OfferResponse> getTicketsCompatibility(
        @PathVariable UUID activityId,
        @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate date
    ) {
        return activityQueryService.getOffers(activityId, date);
    }

    public record LegacyFilterRequest(
        @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate date,
        Integer pax
    ) {
    }
}
