package com.musepicker.api.dto.v1;

import java.util.List;
import java.util.UUID;

public record ActivitySearchItemResponse(
    UUID id,
    String name,
    String image,
    String city,
    String state,
    int ticketTypeCount,
    int platformCount,
    List<TicketPreviewResponse> ticketPreview
) {
}
