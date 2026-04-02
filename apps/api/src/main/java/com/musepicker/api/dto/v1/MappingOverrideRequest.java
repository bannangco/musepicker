package com.musepicker.api.dto.v1;

import java.math.BigDecimal;
import java.util.UUID;

import jakarta.validation.constraints.DecimalMax;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;

public record MappingOverrideRequest(
    @NotBlank String source,
    @NotBlank String sourceActivityId,
    UUID coreActivityId,
    UUID mualbaActivityId,
    @DecimalMin("0.0") @DecimalMax("1.0") BigDecimal confidenceScore
) {
}
