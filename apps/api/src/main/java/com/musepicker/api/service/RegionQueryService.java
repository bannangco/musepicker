package com.musepicker.api.service;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.stereotype.Service;

import com.musepicker.api.domain.core.CoreActivity;
import com.musepicker.api.domain.core.CoreOffer;
import com.musepicker.api.dto.v1.RegionCityResponse;
import com.musepicker.api.repository.CoreActivityRepository;
import com.musepicker.api.repository.CoreOfferRepository;
import com.musepicker.api.service.mapper.CoreMappers;

@Service
public class RegionQueryService {

    private final CoreActivityRepository activityRepository;
    private final CoreOfferRepository offerRepository;

    public RegionQueryService(CoreActivityRepository activityRepository, CoreOfferRepository offerRepository) {
        this.activityRepository = activityRepository;
        this.offerRepository = offerRepository;
    }

    public List<RegionCityResponse> getRegionCities() {
        List<CoreActivity> activities = activityRepository.findAllWithRegion();
        List<CoreOffer> offers = offerRepository.findAllForTrending();

        Map<String, RegionAccumulator> cityMap = new HashMap<>();

        for (CoreActivity activity : activities) {
            String city = activity.getRegion().getCity();
            RegionAccumulator acc = cityMap.computeIfAbsent(city, c -> new RegionAccumulator(activity.getRegion().getId(), city, activity.getRegion().getState()));
            acc.totalCount += 1;
            for (String category : CoreMappers.splitCsv(activity.getCategoriesCsv())) {
                if (acc.categories.size() < 3 && !acc.categories.contains(category)) {
                    acc.categories.add(category);
                }
            }
        }

        for (CoreOffer offer : offers) {
            String city = offer.getActivity().getRegion().getCity();
            RegionAccumulator acc = cityMap.get(city);
            if (acc == null) {
                continue;
            }
            BigDecimal effective = offer.effectivePrice();
            if (acc.lowestPrice == null || effective.compareTo(acc.lowestPrice) < 0) {
                acc.lowestPrice = effective;
            }
        }

        return cityMap.values().stream()
            .map(acc -> new RegionCityResponse(
                acc.id,
                acc.city,
                acc.state,
                acc.totalCount,
                acc.categories,
                acc.lowestPrice == null ? BigDecimal.ZERO : acc.lowestPrice
            ))
            .sorted(Comparator.comparing(RegionCityResponse::city))
            .toList();
    }

    private static final class RegionAccumulator {
        private final java.util.UUID id;
        private final String city;
        private final String state;
        private long totalCount;
        private final List<String> categories = new ArrayList<>();
        private BigDecimal lowestPrice;

        private RegionAccumulator(java.util.UUID id, String city, String state) {
            this.id = id;
            this.city = city;
            this.state = state;
        }
    }
}
