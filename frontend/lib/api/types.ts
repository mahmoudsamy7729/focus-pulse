export type ApiSuccess<T> = {
  success: true;
  data: T;
};

export type ApiErrorBody = {
  code: string;
  message: string;
  details: Record<string, unknown>;
};

export type ApiErrorEnvelope = {
  success: false;
  error: ApiErrorBody;
};

export type ApiEnvelope<T> = ApiSuccess<T> | ApiErrorEnvelope;

export class FocusPulseApiError extends Error {
  readonly code: string;
  readonly status?: number;
  readonly details: Record<string, unknown>;

  constructor(error: ApiErrorBody, status?: number) {
    super(error.message);
    this.name = "FocusPulseApiError";
    this.code = error.code;
    this.status = status;
    this.details = error.details;
  }
}
