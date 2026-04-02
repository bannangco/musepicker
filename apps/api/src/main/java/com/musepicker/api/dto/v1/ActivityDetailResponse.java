package com.musepicker.api.dto.v1;

import java.util.List;
import java.util.UUID;

public record ActivityDetailResponse(
    UUID id,
    String name,
    String description,
    List<String> images,
    List<String> categories,
    RegionCityResponse region
) {
}
