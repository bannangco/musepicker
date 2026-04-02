package com.musepicker.api.service.mapper;

import java.util.Arrays;
import java.util.List;

public final class CoreMappers {
    private CoreMappers() {
    }

    public static List<String> splitCsv(String csv) {
        if (csv == null || csv.isBlank()) {
            return List.of();
        }
        return Arrays.stream(csv.split(","))
            .map(String::trim)
            .filter(s -> !s.isBlank())
            .toList();
    }
}
