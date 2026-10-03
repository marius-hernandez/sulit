"use client";

import { useCallback, useEffect, useState } from "react";
import Header from "@/components/Header";
import Chatbox from "@/components/Chat/Chatbox";
import MessageList from "@/components/Chat/MessageList";
import { ApiError, getConversationMessages, sendChatMessage } from "@/services/chatService";
import type { ChatMessage } from "@/types/chat";

const CONVERSATION_STORAGE_KEY = "sulit.conversationId";

const WELCOME_MESSAGE: ChatMessage = {
  id: "welcome",
  role: "assistant",
  content: "Hi! I'm Sulit, your grocery buddy. Tell me about your budget or what you need, and I'll help you build a smart grocery list.",
};

export default function ChatWindow() {
  const [messages, setMessages] = useState<ChatMessage[]>([WELCOME_MESSAGE]);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [isSending, setIsSending] = useState(false);

  useEffect(() => {
    const storedId = window.localStorage.getItem(CONVERSATION_STORAGE_KEY);
    if (!storedId) {
      return;
    }

    const controller = new AbortController();

    getConversationMessages(storedId, controller.signal)
      .then((history) => {
        // Don't clobber a conversation the user already started while history was loading.
        setConversationId((current) => current ?? storedId);
        setMessages((current) => (current.length === 1 ? [WELCOME_MESSAGE, ...history] : current));
      })
      .catch((error: unknown) => {
        if (error instanceof ApiError && error.status === 404) {
          window.localStorage.removeItem(CONVERSATION_STORAGE_KEY);
        }
      });

    return () => controller.abort();
  }, []);

  const handleSend = useCallback(
    async (text: string) => {
      if (isSending) {
        return;
      }

      setIsSending(true);
      setMessages((prev) => [...prev, { id: crypto.randomUUID(), role: "user", content: text }]);

      try {
        const response = await sendChatMessage(text, conversationId);
        setConversationId(response.conversationId);
        window.localStorage.setItem(CONVERSATION_STORAGE_KEY, response.conversationId);
        setMessages((prev) => [...prev, response.message]);
      } catch (error) {
        const content = error instanceof Error ? error.message : "Something went wrong.";
        setMessages((prev) => [
          ...prev,
          { id: crypto.randomUUID(), role: "assistant", content, isError: true },
        ]);
      } finally {
        setIsSending(false);
      }
    },
    [conversationId, isSending],
  );

  const handleNewChat = useCallback(() => {
    window.localStorage.removeItem(CONVERSATION_STORAGE_KEY);
    setConversationId(null);
    setMessages([WELCOME_MESSAGE]);
  }, []);

  return (
    <div className="mx-auto flex h-dvh w-full max-w-3xl flex-col px-4 pb-4">
      <Header status={isSending ? "Thinking..." : "Ready"} onNewChat={handleNewChat} isNewChatDisabled={isSending} />
      <MessageList messages={messages} isTyping={isSending} />
      <Chatbox onSend={handleSend} isDisabled={isSending} />
    </div>
  );
}
