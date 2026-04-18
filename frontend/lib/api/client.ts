import axios, { AxiosError } from "axios";
import { FocusPulseApiError, type ApiEnvelope } from "./types";

export const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1",
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
