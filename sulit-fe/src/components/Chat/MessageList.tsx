"use client";

import { useEffect, useRef } from "react";
import MessageBubble, { ChatMessage } from "./MessageBubble";

export default function MessageList({
  messages,
}: {
  messages: ChatMessage[];
}) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  return (
    <div className="min-h-0 flex-1 overflow-y-auto">
      {messages.map((message) => (
        <MessageBubble
          key={message.id}
          message={message}
        />
      ))}

      {/* Invisible element at the very bottom */}
      <div ref={bottomRef} />
    </div>
  );
}