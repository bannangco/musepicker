package com.musepicker.api.service;

import java.net.URI;
import java.time.Instant;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.UUID;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.util.UriComponentsBuilder;

import com.musepicker.api.config.RequestContext;
import com.musepicker.api.domain.core.CoreAffiliateClick;
import com.musepicker.api.domain.core.CoreOffer;
import com.musepicker.api.dto.v1.AffiliateClickResponse;
import com.musepicker.api.exception.ResourceNotFoundException;
import com.musepicker.api.repository.CoreAffiliateClickRepository;
import com.musepicker.api.repository.CoreOfferRepository;

@Service
public class AffiliateAttributionService {

    private final CoreOfferRepository offerRepository;
    private final CoreAffiliateClickRepository clickRepository;

    public AffiliateAttributionService(CoreOfferRepository offerRepository, CoreAffiliateClickRepository clickRepository) {
        this.offerRepository = offerRepository;
        this.clickRepository = clickRepository;
    }

    @Transactional
    public RedirectResult trackAndBuildRedirect(
        UUID offerId,
        String target,
        String platformHint,
        String referrer,
        String userAgent
    ) {
        CoreOffer offer = offerRepository.findById(offerId)
            .orElseThrow(() -> new ResourceNotFoundException("Offer not found: " + offerId));

        String platformCode = platformHint == null || platformHint.isBlank()
            ? offer.getPlatform().getCode()
            : platformHint.trim().toUpperCase();

        URI destination = validateTarget(target);
        UUID clickId = UUID.randomUUID();
        String resolvedTarget = appendTrackingParams(destination, clickId, platformCode);

        CoreAffiliateClick click = new CoreAffiliateClick();
        click.setClickId(clickId);
        click.setOffer(offer);
        click.setPlatformCode(platformCode);
        click.setTargetUrl(resolvedTarget);
        click.setRequestId(RequestContext.getRequestId());
        click.setReferrer(trimOrNull(referrer));
        click.setUserAgent(trimOrNull(userAgent));
        click.setCreatedAt(Instant.now());
        clickRepository.save(click);

        AffiliateClickResponse response = new AffiliateClickResponse(
            clickId,
            offer.getId(),
            platformCode,
            resolvedTarget,
            click.getRequestId(),
            click.getCreatedAt()
        );
        return new RedirectResult(response, resolvedTarget);
    }

    private static URI validateTarget(String target) {
        if (target == null || target.isBlank()) {
            throw new IllegalArgumentException("target is required");
        }
        URI uri;
        try {
            uri = URI.create(target.trim());
        } catch (RuntimeException ex) {
            throw new IllegalArgumentException("target must be a valid URI");
        }
        String scheme = uri.getScheme();
        if (!"http".equalsIgnoreCase(scheme) && !"https".equalsIgnoreCase(scheme)) {
            throw new IllegalArgumentException("target must use http or https");
        }
        return uri;
    }

    private static String appendTrackingParams(URI destination, UUID clickId, String platformCode) {
        Map<String, String> params = new LinkedHashMap<>();
        params.put("mp_click_id", clickId.toString());
        params.put("utm_source", "musepicker");
        params.put("utm_medium", "affiliate");

        String normalizedPlatform = platformCode.toUpperCase();
        switch (normalizedPlatform) {
            case "TRIPCOM" -> params.put("trip_sub1", clickId.toString());
            case "KLOOK" -> params.put("sub_id1", clickId.toString());
            case "VIATOR" -> params.put("pid", clickId.toString());
            case "TICKETSTODO" -> params.put("subid", clickId.toString());
            default -> params.put("mp_sub1", clickId.toString());
        }

        UriComponentsBuilder builder = UriComponentsBuilder.fromUri(destination);
        var existingParams = builder.build(true).getQueryParams();
        params.forEach((key, value) -> {
            if (!existingParams.containsKey(key)) {
                builder.queryParam(key, value);
            }
        });
        return builder.build(true).toUriString();
    }

    private static String trimOrNull(String value) {
        if (value == null) {
            return null;
        }
        String trimmed = value.trim();
        return trimmed.isEmpty() ? null : trimmed;
    }

    public record RedirectResult(AffiliateClickResponse click, String redirectUrl) {
    }
}
