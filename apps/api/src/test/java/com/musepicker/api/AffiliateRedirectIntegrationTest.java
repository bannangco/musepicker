package com.musepicker.api;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class AffiliateRedirectIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void affiliateRedirectCreatesClickAndRedirects() throws Exception {
        mockMvc.perform(
                get("/api/affiliate/out/{offerId}", "100e8400-e29b-41d4-a716-446655440001")
                    .param("target", "https://www.klook.com/activity/moma?aid=musepicker")
                    .param("platform", "KLOOK")
            )
            .andExpect(status().isFound())
            .andExpect(header().exists("Location"))
            .andExpect(header().exists("X-Musepicker-Click-Id"));
    }
}
