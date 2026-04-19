import { describe, expect, it } from "vitest";

import { resolveApiBaseUrl } from "./client";

describe("resolveApiBaseUrl", () => {
  it("uses the same-origin API path when no base URL is configured", () => {
    expect(resolveApiBaseUrl(undefined)).toBe("/api/v1");
  });

  it("normalizes local backend URLs to the same-origin proxy path in the browser", () => {
    expect(resolveApiBaseUrl("http://localhost:8000/api/v1")).toBe("/api/v1");
    expect(resolveApiBaseUrl("http://127.0.0.1:8000/api/v1")).toBe("/api/v1");
  });

  it("preserves non-local API URLs", () => {
    expect(resolveApiBaseUrl("https://api.example.com/api/v1")).toBe("https://api.example.com/api/v1");
  });
});
