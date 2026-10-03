export type ChatMessageRequest = {
  message: string;
};

export type ChatMessageResponse = {
  reply?: string;
  message?: string;
  success?: boolean;
};

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:3001";

export async function sendChatMessage(message: string): Promise<ChatMessageResponse> {
  const response = await fetch(`${API_BASE_URL}/api/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message } satisfies ChatMessageRequest),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || "Unable to send message to backend.");
  }

  return response.json();
}
