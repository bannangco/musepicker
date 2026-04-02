package com.musepicker.api;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class AdminMappingOverrideIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void mappingOverrideUpsertsMappingAndMarksManualOverride() throws Exception {
        String payload = """
            {
              "source": "klook",
              "sourceActivityId": "moma-activity-1",
              "coreActivityId": "660e8400-e29b-41d4-a716-446655440001",
              "mualbaActivityId": "aa0e8400-e29b-41d4-a716-446655440001",
              "confidenceScore": 1.0
            }
            """;

        mockMvc.perform(
                post("/api/admin/mappings/override")
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(payload)
            )
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.source").value("klook"))
            .andExpect(jsonPath("$.sourceActivityId").value("moma-activity-1"))
            .andExpect(jsonPath("$.coreActivityId").value("660e8400-e29b-41d4-a716-446655440001"))
            .andExpect(jsonPath("$.mualbaActivityId").value("aa0e8400-e29b-41d4-a716-446655440001"));
    }
}
