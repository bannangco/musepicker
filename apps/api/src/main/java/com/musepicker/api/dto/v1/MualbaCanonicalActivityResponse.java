package com.musepicker.api.dto.v1;

import java.util.UUID;

public record MualbaCanonicalActivityResponse(
    UUID id,
    String slug,
    String name,
    String canonicalCategory,
    String status
) {
}
