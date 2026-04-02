package com.musepicker.api;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import com.musepicker.api.dto.v1.PagedResponse;
import com.musepicker.api.dto.v1.ActivitySearchItemResponse;
import com.musepicker.api.service.ActivityQueryService;
import com.musepicker.api.service.SearchCriteria;

@SpringBootTest
class SearchRegressionTest {

    @Autowired
    private ActivityQueryService activityQueryService;

    @Test
    void cityAndCategoryFiltersRemainConsistent() {
        PagedResponse<ActivitySearchItemResponse> result = activityQueryService.searchActivities(
            new SearchCriteria("New York", "Museums", null, null, 1),
            0,
            20
        );

        assertThat(result.items()).isNotEmpty();
        assertThat(result.items().stream().allMatch(item -> "New York".equalsIgnoreCase(item.city()))).isTrue();
    }
}
