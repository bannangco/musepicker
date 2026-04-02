package com.musepicker.api.dto.v1;

import java.math.BigDecimal;
import java.util.UUID;

public record OfferAnomalyResponse(
    UUID offerId,
    String reason,
    BigDecimal effectivePrice,
    Integer availability
) {
}
