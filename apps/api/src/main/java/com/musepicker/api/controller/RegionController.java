package com.musepicker.api.controller;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.musepicker.api.dto.v1.RegionCityResponse;
import com.musepicker.api.service.RegionQueryService;

@RestController
@RequestMapping("/api/regions")
public class RegionController {

    private final RegionQueryService regionQueryService;

    public RegionController(RegionQueryService regionQueryService) {
        this.regionQueryService = regionQueryService;
    }

    @GetMapping("/cities")
    public List<RegionCityResponse> getCities() {
        return regionQueryService.getRegionCities();
    }
}
