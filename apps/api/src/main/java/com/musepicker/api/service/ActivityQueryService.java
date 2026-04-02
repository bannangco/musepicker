package com.musepicker.api.service;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import org.springframework.stereotype.Service;

import com.musepicker.api.domain.core.CoreActivity;
import com.musepicker.api.domain.core.CoreOffer;
import com.musepicker.api.dto.v1.ActivityDetailResponse;
import com.musepicker.api.dto.v1.ActivitySearchItemResponse;
import com.musepicker.api.dto.v1.OfferResponse;
import com.musepicker.api.dto.v1.PagedResponse;
import com.musepicker.api.dto.v1.PlatformResponse;
import com.musepicker.api.dto.v1.RegionCityResponse;
import com.musepicker.api.dto.v1.TicketPreviewResponse;
import com.musepicker.api.dto.v1.TrendingActivityResponse;
import com.musepicker.api.exception.ResourceNotFoundException;
import com.musepicker.api.repository.CoreActivityRepository;
import com.musepicker.api.repository.CoreOfferRepository;
import com.musepicker.api.service.mapper.CoreMappers;

@Service
public class ActivityQueryService {

    private final CoreActivityRepository activityRepository;
    private final CoreOfferRepository offerRepository;

    public ActivityQueryService(CoreActivityRepository activityRepository, CoreOfferRepository offerRepository) {
        this.activityRepository = activityRepository;
        this.offerRepository = offerRepository;
    }

    public PagedResponse<ActivitySearchItemResponse> searchActivities(SearchCriteria criteria, int page, int size) {
        List<CoreOffer> offers = offerRepository.searchOffers(
            emptyToNull(criteria.city()),
            emptyToNull(criteria.category()),
            emptyToNull(criteria.query()),
            criteria.date()
        );

        if (criteria.pax() > 0) {
            offers = offers.stream()
                .filter(o -> o.getSchedule() == null || o.getSchedule().getMaxPax() == null || o.getSchedule().getMaxPax() >= criteria.pax())
                .toList();
        }

        Map<UUID, List<CoreOffer>> byActivity = new HashMap<>();
        for (CoreOffer offer : offers) {
            byActivity.computeIfAbsent(offer.getActivity().getId(), ignored -> new ArrayList<>()).add(offer);
        }

        List<ActivitySearchItemResponse> items = byActivity.values().stream()
            .map(this::toSearchItem)
            .sorted(Comparator.comparing(ActivitySearchItemResponse::name))
            .toList();

        int fromIndex = Math.min(page * size, items.size());
        int toIndex = Math.min(fromIndex + size, items.size());
        List<ActivitySearchItemResponse> pagedItems = items.subList(fromIndex, toIndex);

        int totalPages = size == 0 ? 0 : (int) Math.ceil((double) items.size() / (double) size);
        return new PagedResponse<>(page, size, items.size(), totalPages, pagedItems);
    }

    public List<TrendingActivityResponse> getTrendingActivities() {
        Map<UUID, List<CoreOffer>> byActivity = new HashMap<>();
        for (CoreOffer offer : offerRepository.findAllForTrending()) {
            byActivity.computeIfAbsent(offer.getActivity().getId(), ignored -> new ArrayList<>()).add(offer);
        }

        List<TrendingActivityResponse> trending = new ArrayList<>();
        for (List<CoreOffer> offers : byActivity.values()) {
            CoreActivity activity = offers.get(0).getActivity();
            BigDecimal lowestEffective = offers.stream().map(CoreOffer::effectivePrice).min(BigDecimal::compareTo).orElse(BigDecimal.ZERO);
            BigDecimal highestBase = offers.stream().map(CoreOffer::getBasePrice).max(BigDecimal::compareTo).orElse(BigDecimal.ZERO);
            double discountRate = BigDecimal.ZERO.compareTo(highestBase) == 0
                ? 0
                : highestBase.subtract(lowestEffective)
                    .divide(highestBase, 4, java.math.RoundingMode.HALF_UP)
                    .multiply(BigDecimal.valueOf(100))
                    .doubleValue();
            trending.add(new TrendingActivityResponse(activity.getId(), activity.getName(), nullToEmpty(activity.getImageUrl()), lowestEffective, discountRate));
        }

        return trending.stream()
            .sorted(Comparator.comparing(TrendingActivityResponse::discountRate).reversed())
            .limit(12)
            .toList();
    }

    public ActivityDetailResponse getActivity(UUID activityId) {
        CoreActivity activity = activityRepository.findById(activityId)
            .orElseThrow(() -> new ResourceNotFoundException("Activity not found: " + activityId));

        RegionCityResponse region = new RegionCityResponse(
            activity.getRegion().getId(),
            activity.getRegion().getCity(),
            activity.getRegion().getState(),
            0,
            List.of(),
            BigDecimal.ZERO
        );

        return new ActivityDetailResponse(
            activity.getId(),
            activity.getName(),
            nullToEmpty(activity.getDescription()),
            activity.getImageUrl() == null || activity.getImageUrl().isBlank() ? List.of() : List.of(activity.getImageUrl()),
            CoreMappers.splitCsv(activity.getCategoriesCsv()),
            region
        );
    }

    public List<OfferResponse> getOffers(UUID activityId, LocalDate date) {
        List<CoreOffer> offers = offerRepository.findByActivityAndDate(activityId, date);
        if (offers.isEmpty()) {
            if (activityRepository.findById(activityId).isEmpty()) {
                throw new ResourceNotFoundException("Activity not found: " + activityId);
            }
            return List.of();
        }

        return offers.stream()
            .sorted(Comparator
                .comparing(CoreOffer::effectivePrice)
                .thenComparing(o -> o.getPlatform().getCode())
                .thenComparing(CoreOffer::getLastSeenAt, Comparator.reverseOrder())
            )
            .map(this::toOfferResponse)
            .toList();
    }

    private ActivitySearchItemResponse toSearchItem(List<CoreOffer> offers) {
        CoreActivity activity = offers.get(0).getActivity();

        List<TicketPreviewResponse> preview = offers.stream()
            .sorted(Comparator.comparing(CoreOffer::effectivePrice))
            .limit(3)
            .map(o -> new TicketPreviewResponse(o.getPlatform().getName(), o.effectivePrice()))
            .toList();

        int ticketTypeCount = (int) offers.stream()
            .map(o -> o.getTicketType() == null ? "general" : o.getTicketType().getName())
            .distinct()
            .count();

        int platformCount = new HashSet<>(offers.stream().map(o -> o.getPlatform().getId()).toList()).size();

        return new ActivitySearchItemResponse(
            activity.getId(),
            activity.getName(),
            nullToEmpty(activity.getImageUrl()),
            activity.getRegion().getCity(),
            nullToEmpty(activity.getRegion().getState()),
            ticketTypeCount,
            platformCount,
            preview
        );
    }

    private OfferResponse toOfferResponse(CoreOffer offer) {
        PlatformResponse platform = new PlatformResponse(
            offer.getPlatform().getId(),
            offer.getPlatform().getCode(),
            offer.getPlatform().getName(),
            offer.getPlatform().getHomepageUrl()
        );

        return new OfferResponse(
            offer.getId(),
            offer.getActivity().getId(),
            platform,
            offer.getTicketType() == null ? "General" : offer.getTicketType().getName(),
            offer.getSchedule() == null ? null : offer.getSchedule().getStartDate(),
            offer.getBasePrice(),
            offer.getFeeAmount(),
            offer.getDiscountAmount(),
            offer.effectivePrice(),
            offer.getAffiliateUrl()
        );
    }

    private static String nullToEmpty(String value) {
        return value == null ? "" : value;
    }

    private static String emptyToNull(String value) {
        if (value == null || value.isBlank()) {
            return null;
        }
        return value;
    }
}
