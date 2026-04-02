package com.musepicker.api.dto.v1;

import java.math.BigDecimal;
import java.util.UUID;

public record TrendingActivityResponse(
    UUID id,
    String name,
    String image,
    BigDecimal lowestPrice,
    double discountRate
) {
}
