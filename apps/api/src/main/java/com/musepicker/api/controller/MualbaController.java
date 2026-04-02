package com.musepicker.api.controller;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.musepicker.api.dto.v1.MualbaCanonicalActivityResponse;
import com.musepicker.api.service.MualbaQueryService;

@RestController
@RequestMapping("/api/mualba")
public class MualbaController {

    private final MualbaQueryService mualbaQueryService;

    public MualbaController(MualbaQueryService mualbaQueryService) {
        this.mualbaQueryService = mualbaQueryService;
    }

    @GetMapping("/activities")
    public List<MualbaCanonicalActivityResponse> listCanonicalActivities() {
        return mualbaQueryService.listCanonicalActivities();
    }
}
