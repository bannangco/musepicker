package com.musepicker.api.dto.v1;

import java.time.Instant;

public record ApiErrorResponse(
    String code,
    String message,
    String requestId,
    Instant timestamp
) {
}
