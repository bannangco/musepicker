package com.musepicker.api.dto.v1;

import java.util.UUID;

public record MappingReviewItemResponse(
    String source,
    String sourceActivityId,
    UUID coreActivityId,
    UUID mualbaActivityId
) {
}
