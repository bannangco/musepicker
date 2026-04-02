package com.musepicker.api.domain.source;

import java.util.UUID;

import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

import com.musepicker.api.domain.core.CoreActivity;
import com.musepicker.api.domain.mualba.MualbaCanonicalActivity;

@Entity
@Table(name = "source_activity_map")
public class SourceActivityMap {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column(columnDefinition = "char(36)")
    private UUID id;

    @Column(nullable = false, length = 64)
    private String source;

    @Column(name = "source_activity_id", nullable = false, length = 255)
    private String sourceActivityId;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "core_activity_id")
    private CoreActivity coreActivity;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "mualba_activity_id")
    private MualbaCanonicalActivity mualbaActivity;

    public UUID getId() {
        return id;
    }

    public String getSource() {
        return source;
    }

    public void setSource(String source) {
        this.source = source;
    }

    public String getSourceActivityId() {
        return sourceActivityId;
    }

    public void setSourceActivityId(String sourceActivityId) {
        this.sourceActivityId = sourceActivityId;
    }

    public CoreActivity getCoreActivity() {
        return coreActivity;
    }

    public void setCoreActivity(CoreActivity coreActivity) {
        this.coreActivity = coreActivity;
    }

    public MualbaCanonicalActivity getMualbaActivity() {
        return mualbaActivity;
    }

    public void setMualbaActivity(MualbaCanonicalActivity mualbaActivity) {
        this.mualbaActivity = mualbaActivity;
    }
}
