package com.musepicker.api.controller;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.musepicker.api.dto.v1.MappingOverrideRequest;
import com.musepicker.api.dto.v1.MappingReviewItemResponse;
import com.musepicker.api.dto.v1.OfferAnomalyResponse;
import com.musepicker.api.dto.v1.SourceHealthResponse;
import com.musepicker.api.service.AdminQueryService;

import jakarta.validation.Valid;

@RestController
@RequestMapping("/api/admin")
public class AdminController {

    private final AdminQueryService adminQueryService;

    public AdminController(AdminQueryService adminQueryService) {
        this.adminQueryService = adminQueryService;
    }

    @GetMapping("/sources/health")
    public List<SourceHealthResponse> getSourceHealth() {
        return adminQueryService.getSourceHealth();
    }

    @GetMapping("/mappings/review")
    public List<MappingReviewItemResponse> getMappingReviewQueue() {
        return adminQueryService.getMappingReviewQueue();
    }

    @GetMapping("/offers/anomalies")
    public List<OfferAnomalyResponse> getOfferAnomalies() {
        return adminQueryService.getOfferAnomalies();
    }

    @PostMapping("/mappings/override")
    public MappingReviewItemResponse applyMappingOverride(@Valid @RequestBody MappingOverrideRequest request) {
        return adminQueryService.applyMappingOverride(request);
    }
}
