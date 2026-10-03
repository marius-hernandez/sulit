"use client";

import { useEffect, useRef } from "react";
import MessageBubble from "./MessageBubble";
import type { ChatMessage } from "@/types/chat";

type MessageListProps = {
  messages: ChatMessage[];
  isTyping?: boolean;
};

export default function MessageList({ messages, isTyping = false }: MessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  return (
    <div className="min-h-0 flex-1 overflow-y-auto" role="log" aria-live="polite">
      {messages.map((message) => (
        <MessageBubble key={message.id} message={message} />
      ))}

      {isTyping && (
        <div className="mt-4 w-fit rounded-[24px] bg-secondary px-4 py-3 text-[17px] text-muted-foreground animate-pulse">
          Thinking...
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  );
}