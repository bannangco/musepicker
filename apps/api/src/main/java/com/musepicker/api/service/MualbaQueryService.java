package com.musepicker.api.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.musepicker.api.dto.v1.MualbaCanonicalActivityResponse;
import com.musepicker.api.repository.MualbaCanonicalActivityRepository;

@Service
public class MualbaQueryService {

    private final MualbaCanonicalActivityRepository repository;

    public MualbaQueryService(MualbaCanonicalActivityRepository repository) {
        this.repository = repository;
    }

    public List<MualbaCanonicalActivityResponse> listCanonicalActivities() {
        return repository.findAll().stream()
            .map(entity -> new MualbaCanonicalActivityResponse(
                entity.getId(),
                entity.getSlug(),
                entity.getName(),
                entity.getCanonicalCategory(),
                entity.getStatus()
            ))
            .toList();
    }
}
