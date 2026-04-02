package com.musepicker.api.dto.v1;

import java.math.BigDecimal;
import java.util.List;
import java.util.UUID;

public record RegionCityResponse(
    UUID id,
    String city,
    String state,
    long totalCount,
    List<String> categories,
    BigDecimal lowestPrice
) {
}
