package com.musepicker.api.dto.v1;

public record SourceHealthResponse(
    String source,
    long rawOfferCount,
    long mappedCount,
    long unmappedCount
) {
}
