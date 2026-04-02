package com.musepicker.api.domain.core;

import java.time.Instant;
import java.util.UUID;

import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

@Entity
@Table(name = "core_affiliate_click")
public class CoreAffiliateClick {
    @Id
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column(name = "click_id", columnDefinition = "char(36)")
    private UUID clickId;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "offer_id")
    private CoreOffer offer;

    @Column(name = "platform_code", nullable = false, length = 32)
    private String platformCode;

    @Column(name = "target_url", nullable = false, length = 2048)
    private String targetUrl;

    @Column(name = "request_id", nullable = false, length = 64)
    private String requestId;

    @Column(length = 2048)
    private String referrer;

    @Column(name = "user_agent", length = 1024)
    private String userAgent;

    @Column(name = "created_at", nullable = false)
    private Instant createdAt;

    public UUID getClickId() {
        return clickId;
    }

    public void setClickId(UUID clickId) {
        this.clickId = clickId;
    }

    public CoreOffer getOffer() {
        return offer;
    }

    public void setOffer(CoreOffer offer) {
        this.offer = offer;
    }

    public String getPlatformCode() {
        return platformCode;
    }

    public void setPlatformCode(String platformCode) {
        this.platformCode = platformCode;
    }

    public String getTargetUrl() {
        return targetUrl;
    }

    public void setTargetUrl(String targetUrl) {
        this.targetUrl = targetUrl;
    }

    public String getRequestId() {
        return requestId;
    }

    public void setRequestId(String requestId) {
        this.requestId = requestId;
    }

    public String getReferrer() {
        return referrer;
    }

    public void setReferrer(String referrer) {
        this.referrer = referrer;
    }

    public String getUserAgent() {
        return userAgent;
    }

    public void setUserAgent(String userAgent) {
        this.userAgent = userAgent;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(Instant createdAt) {
        this.createdAt = createdAt;
    }
}
