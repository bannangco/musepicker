package com.musepicker.api.controller;

import java.net.URI;
import java.util.UUID;

import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.musepicker.api.service.AffiliateAttributionService;

@RestController
@RequestMapping("/api/affiliate")
public class AffiliateController {

    private final AffiliateAttributionService affiliateAttributionService;

    public AffiliateController(AffiliateAttributionService affiliateAttributionService) {
        this.affiliateAttributionService = affiliateAttributionService;
    }

    @GetMapping("/out/{offerId}")
    public ResponseEntity<Void> redirect(
        @PathVariable UUID offerId,
        @RequestParam String target,
        @RequestParam(required = false) String platform,
        @RequestHeader(value = "referer", required = false) String referrer,
        @RequestHeader(value = "user-agent", required = false) String userAgent
    ) {
        AffiliateAttributionService.RedirectResult result = affiliateAttributionService.trackAndBuildRedirect(
            offerId,
            target,
            platform,
            referrer,
            userAgent
        );

        HttpHeaders headers = new HttpHeaders();
        headers.setLocation(URI.create(result.redirectUrl()));
        headers.set("X-Musepicker-Click-Id", result.click().clickId().toString());
        return new ResponseEntity<>(headers, HttpStatus.FOUND);
    }
}
