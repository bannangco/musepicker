package com.musepicker.api.service;

import java.time.LocalDate;

public record SearchCriteria(
    String city,
    String category,
    String query,
    LocalDate date,
    int pax
) {
}
