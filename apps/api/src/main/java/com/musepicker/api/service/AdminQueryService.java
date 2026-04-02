package com.musepicker.api.service;

import java.math.BigDecimal;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.musepicker.api.domain.source.SourceActivityMap;
import com.musepicker.api.dto.v1.MappingOverrideRequest;
import com.musepicker.api.dto.v1.MappingReviewItemResponse;
import com.musepicker.api.dto.v1.OfferAnomalyResponse;
import com.musepicker.api.dto.v1.SourceHealthResponse;
import com.musepicker.api.repository.CoreActivityRepository;
import com.musepicker.api.repository.CoreOfferRepository;
import com.musepicker.api.repository.MualbaCanonicalActivityRepository;
import com.musepicker.api.repository.SourceActivityMapRepository;
import com.musepicker.api.repository.SourceRawOfferRepository;

@Service
public class AdminQueryService {

    private final SourceRawOfferRepository rawOfferRepository;
    private final SourceActivityMapRepository activityMapRepository;
    private final CoreOfferRepository offerRepository;
    private final CoreActivityRepository activityRepository;
    private final MualbaCanonicalActivityRepository mualbaRepository;

    public AdminQueryService(
        SourceRawOfferRepository rawOfferRepository,
        SourceActivityMapRepository activityMapRepository,
        CoreOfferRepository offerRepository,
        CoreActivityRepository activityRepository,
        MualbaCanonicalActivityRepository mualbaRepository
    ) {
        this.rawOfferRepository = rawOfferRepository;
        this.activityMapRepository = activityMapRepository;
        this.offerRepository = offerRepository;
        this.activityRepository = activityRepository;
        this.mualbaRepository = mualbaRepository;
    }

    public List<SourceHealthResponse> getSourceHealth() {
        Map<String, Long> rawCount = new HashMap<>();
        rawOfferRepository.countBySource().forEach(row -> rawCount.put(row.getSource(), row.getTotal()));

        Map<String, Long> mappedCount = new HashMap<>();
        activityMapRepository.countBySource().forEach(row -> mappedCount.put(row.getSource(), row.getTotal()));

        return rawCount.entrySet().stream()
            .map(entry -> {
                String source = entry.getKey();
                long totalRaw = entry.getValue();
                long totalMapped = mappedCount.getOrDefault(source, 0L);
                long unmapped = Math.max(totalRaw - totalMapped, 0L);
                return new SourceHealthResponse(source, totalRaw, totalMapped, unmapped);
            })
            .sorted((a, b) -> a.source().compareToIgnoreCase(b.source()))
            .toList();
    }

    public List<MappingReviewItemResponse> getMappingReviewQueue() {
        return activityMapRepository.findReviewQueue().stream()
            .map(item -> new MappingReviewItemResponse(
                item.getSource(),
                item.getSourceActivityId(),
                item.getCoreActivity() == null ? null : item.getCoreActivity().getId(),
                item.getMualbaActivity() == null ? null : item.getMualbaActivity().getId()
            ))
            .toList();
    }

    public List<OfferAnomalyResponse> getOfferAnomalies() {
        return offerRepository.findAnomalyCandidates().stream()
            .filter(offer -> offer.effectivePrice().signum() <= 0 || (offer.getAvailability() != null && offer.getAvailability() <= 0))
            .map(offer -> {
                String reason = offer.effectivePrice().signum() <= 0 ? "NON_POSITIVE_EFFECTIVE_PRICE" : "NO_AVAILABILITY";
                return new OfferAnomalyResponse(
                    offer.getId(),
                    reason,
                    offer.effectivePrice(),
                    offer.getAvailability()
                );
            })
            .limit(200)
            .toList();
    }

    @Transactional
    public MappingReviewItemResponse applyMappingOverride(MappingOverrideRequest request) {
        if (request.coreActivityId() == null && request.mualbaActivityId() == null) {
            throw new IllegalArgumentException("coreActivityId or mualbaActivityId is required");
        }

        String source = request.source().trim().toLowerCase();
        String sourceActivityId = request.sourceActivityId().trim();
        SourceActivityMap map = activityMapRepository.findBySourceAndSourceActivityId(source, sourceActivityId)
            .orElseGet(() -> {
                SourceActivityMap created = new SourceActivityMap();
                created.setSource(source);
                created.setSourceActivityId(sourceActivityId);
                return created;
            });

        if (request.coreActivityId() != null) {
            map.setCoreActivity(activityRepository.findById(request.coreActivityId())
                .orElseThrow(() -> new IllegalArgumentException("Unknown coreActivityId: " + request.coreActivityId())));
        }

        if (request.mualbaActivityId() != null) {
            map.setMualbaActivity(mualbaRepository.findById(request.mualbaActivityId())
                .orElseThrow(() -> new IllegalArgumentException("Unknown mualbaActivityId: " + request.mualbaActivityId())));
        }

        map.setManualOverride(Boolean.TRUE);
        map.setConfidenceScore(request.confidenceScore() == null ? BigDecimal.ONE : request.confidenceScore());
        SourceActivityMap saved = activityMapRepository.save(map);

        return new MappingReviewItemResponse(
            saved.getSource(),
            saved.getSourceActivityId(),
            saved.getCoreActivity() == null ? null : saved.getCoreActivity().getId(),
            saved.getMualbaActivity() == null ? null : saved.getMualbaActivity().getId()
        );
    }
}
