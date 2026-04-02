package com.musepicker.api.controller;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.musepicker.api.dto.v1.PlatformResponse;
import com.musepicker.api.service.PlatformQueryService;

@RestController
@RequestMapping("/api/platforms")
public class PlatformController {

    private final PlatformQueryService platformQueryService;

    public PlatformController(PlatformQueryService platformQueryService) {
        this.platformQueryService = platformQueryService;
    }

    @GetMapping
    public List<PlatformResponse> getPlatforms() {
        return platformQueryService.getPlatforms();
    }
}
