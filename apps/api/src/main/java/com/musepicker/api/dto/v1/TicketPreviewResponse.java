package com.musepicker.api.dto.v1;

import java.math.BigDecimal;

public record TicketPreviewResponse(String platformName, BigDecimal price) {
}
