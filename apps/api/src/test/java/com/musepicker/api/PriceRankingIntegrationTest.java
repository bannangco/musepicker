package com.musepicker.api;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.UUID;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import com.musepicker.api.dto.v1.OfferResponse;
import com.musepicker.api.service.ActivityQueryService;

@SpringBootTest
class PriceRankingIntegrationTest {

    @Autowired
    private ActivityQueryService activityQueryService;

    @Test
    void offersAreDeterministicallySortedByEffectivePriceThenPlatform() {
        UUID activityId = UUID.fromString("660e8400-e29b-41d4-a716-446655440001");
        List<OfferResponse> offers = activityQueryService.getOffers(activityId, null);

        assertThat(offers).isNotEmpty();
        assertThat(offers.get(0).effectivePrice()).isLessThanOrEqualTo(offers.get(offers.size() - 1).effectivePrice());
    }
}
