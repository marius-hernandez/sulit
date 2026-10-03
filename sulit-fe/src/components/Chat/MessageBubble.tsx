"use client";

export type ChatMessage = {
  id: number;
  role: "user" | "assistant";
  text: string;
};

export default function MessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";
  const content = message.text;

  return (
    <div
      className={`w-fit mt-4 rounded-[24px] px-4 py-3 text-[17px] ${
        isUser
          ? "ml-auto max-w-1/2 bg-primary text-primary-foreground"
          : "max-w-1/2 bg-secondary text-secondary-foreground"
      }`}
    >
      {content}
    </div>
  );
}
