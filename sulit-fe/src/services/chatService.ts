import type { ChatMessage, ChatResponse } from "@/types/chat";

const API_BASE_URL = (process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080").replace(/\/+$/, "");

const FALLBACK_ERROR = "Something went wrong. Please try again.";

/** RFC 9457 body returned by the Spring Boot backend. */
type ProblemDetail = {
  title?: string;
  detail?: string;
  status?: number;
};

export class ApiError extends Error {
  readonly status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function readErrorMessage(response: Response): Promise<string> {
  try {
    const body = (await response.json()) as ProblemDetail;
    return body.detail ?? body.title ?? FALLBACK_ERROR;
  } catch {
    return FALLBACK_ERROR;
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      ...init,
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        ...init?.headers,
      },
    });
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError") {
      throw error;
    }
    throw new ApiError("Unable to reach the server. Please try again.", 0);
  }

  if (!response.ok) {
    throw new ApiError(await readErrorMessage(response), response.status);
  }

  return (await response.json()) as T;
}

export function sendChatMessage(message: string, conversationId: string | null): Promise<ChatResponse> {
  return request<ChatResponse>("/api/chat", {
    method: "POST",
    body: JSON.stringify({ message, conversationId }),
  });
}

export function getConversationMessages(conversationId: string, signal?: AbortSignal): Promise<ChatMessage[]> {
  return request<ChatMessage[]>(`/api/conversations/${encodeURIComponent(conversationId)}/messages`, { signal });
}
