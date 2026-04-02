package com.musepicker.api.dto.v1;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.UUID;

public record OfferResponse(
    UUID id,
    UUID activityId,
    PlatformResponse platform,
    String ticketType,
    LocalDate date,
    BigDecimal basePrice,
    BigDecimal feeAmount,
    BigDecimal discountAmount,
    BigDecimal effectivePrice,
    String affiliateUrl
) {
}
