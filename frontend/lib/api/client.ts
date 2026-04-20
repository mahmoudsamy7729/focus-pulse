import axios, { AxiosError } from "axios";
import { FocusPulseApiError, type ApiEnvelope } from "./types";

const SAME_ORIGIN_API_BASE_URL = "/api/v1";
const LOCAL_BACKEND_ORIGINS = new Set(["http://localhost:8000", "http://127.0.0.1:8000"]);

export function resolveApiBaseUrl(configuredBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL): string {
  if (!configuredBaseUrl) {
    return SAME_ORIGIN_API_BASE_URL;
  }

  if (typeof window === "undefined") {
    return configuredBaseUrl;
  }

  try {
    const parsed = new URL(configuredBaseUrl, window.location.origin);
    if (LOCAL_BACKEND_ORIGINS.has(parsed.origin)) {
      return parsed.pathname || SAME_ORIGIN_API_BASE_URL;
    }
  } catch {
    return configuredBaseUrl;
  }

  return configuredBaseUrl;
}

export const apiClient = axios.create({
  baseURL: resolveApiBaseUrl(),
  headers: {
    "Content-Type": "application/json"
  }
});

export async function getApiData<T>(url: string, params?: Record<string, string | undefined>): Promise<T> {
  try {
    const response = await apiClient.get<ApiEnvelope<T>>(url, { params });
    if (response.data.success) {
      return response.data.data;
    }
    throw new FocusPulseApiError(response.data.error, response.status);
  } catch (error) {
    if (error instanceof AxiosError && error.response?.data) {
      const body = error.response.data as ApiEnvelope<unknown>;
      if (!body.success) {
        throw new FocusPulseApiError(body.error, error.response.status);
      }
    }
    throw error;
  }
}

export async function postApiData<T, TBody = unknown>(url: string, body?: TBody): Promise<T> {
  try {
    const response = await apiClient.post<ApiEnvelope<T>>(url, body);
    if (response.data.success) {
      return response.data.data;
    }
    throw new FocusPulseApiError(response.data.error, response.status);
  } catch (error) {
    if (error instanceof AxiosError && error.response?.data) {
      const responseBody = error.response.data as ApiEnvelope<unknown>;
      if (!responseBody.success) {
        throw new FocusPulseApiError(responseBody.error, error.response.status);
      }
    }
    throw error;
  }
}
