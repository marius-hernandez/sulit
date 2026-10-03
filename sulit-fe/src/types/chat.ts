export type ChatRole = "user" | "assistant";

export type ChatMessage = {
  id: string;
  role: ChatRole;
  content: string;
  createdAt?: string;
  isError?: boolean;
};

export type ChatResponse = {
  conversationId: string;
  message: ChatMessage;
};
