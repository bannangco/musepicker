package com.musepicker.api;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class ApiContractTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void regionCitiesContract() throws Exception {
        mockMvc.perform(get("/api/regions/cities"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$[0].city").exists())
            .andExpect(jsonPath("$[0].lowestPrice").exists());
    }

    @Test
    void activitySearchContract() throws Exception {
        mockMvc.perform(get("/api/activities/search").param("city", "New York").param("size", "10"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.items").isArray())
            .andExpect(jsonPath("$.page").value(0));
    }

    @Test
    void platformsContract() throws Exception {
        mockMvc.perform(get("/api/platforms"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$[0].code").exists())
            .andExpect(jsonPath("$[0].homepageUrl").exists());
    }
}
