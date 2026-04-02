package com.musepicker.api.dto.v1;

import java.time.Instant;
import java.util.UUID;

public record AffiliateClickResponse(
    UUID clickId,
    UUID offerId,
    String platformCode,
    String targetUrl,
    String requestId,
    Instant createdAt
) {
}
