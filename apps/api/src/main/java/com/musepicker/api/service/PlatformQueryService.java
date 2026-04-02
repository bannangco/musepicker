package com.musepicker.api.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.musepicker.api.dto.v1.PlatformResponse;
import com.musepicker.api.repository.CorePlatformRepository;

@Service
public class PlatformQueryService {

    private final CorePlatformRepository platformRepository;

    public PlatformQueryService(CorePlatformRepository platformRepository) {
        this.platformRepository = platformRepository;
    }

    public List<PlatformResponse> getPlatforms() {
        return platformRepository.findByEnabledTrueOrderByNameAsc().stream()
            .map(p -> new PlatformResponse(p.getId(), p.getCode(), p.getName(), p.getHomepageUrl()))
            .toList();
    }
}
