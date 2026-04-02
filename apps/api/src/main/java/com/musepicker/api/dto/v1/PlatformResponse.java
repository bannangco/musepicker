package com.musepicker.api.dto.v1;

import java.util.UUID;

public record PlatformResponse(
    UUID id,
    String code,
    String name,
    String homepageUrl
) {
}
