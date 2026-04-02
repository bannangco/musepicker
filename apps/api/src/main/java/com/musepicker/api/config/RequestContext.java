package com.musepicker.api.config;

public final class RequestContext {
    private static final ThreadLocal<String> REQUEST_ID = new ThreadLocal<>();

    private RequestContext() {
    }

    public static void setRequestId(String requestId) {
        REQUEST_ID.set(requestId);
    }

    public static String getRequestId() {
        String requestId = REQUEST_ID.get();
        return requestId == null ? "unknown" : requestId;
    }

    public static void clear() {
        REQUEST_ID.remove();
    }
}
