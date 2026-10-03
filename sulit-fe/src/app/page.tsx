"use client";

import { useState } from "react";
import Header from "@/components/Header";
import MessageList from "@/components/Chat/MessageList";
import type { ChatMessage } from "@/components/Chat/MessageBubble";
import Chatbox from "../components/Chat/Chatbox";
import { sendChatMessage } from "@/services/chatService";

export default function Home() {
  const [isInputDisabled, setIsInputDisabled] = useState(false);

  const initialChatHistory: ChatMessage[] = [
    { id: 1, role: "user", text: "Hello" },
    { id: 2, role: "assistant", text: "Hey, what do you want to do?" },
    { id: 3, role: "user", text: "Start curating my grocery list" },
    {
      id: 4,
      role: "assistant",
      text: `Of course I'll help you! But first, I want to get to know you so I need some context on how you currently budget your grocery. Ways to give me context is by either of this following:\na. Give me link with public access (Excel sheets, Notion)\nb. Send notes file (txt, docs, excel)\nc. Type info directly to chat.\n\nThen from there, I can curate the best list for your upcoming grocery :)`,
    },
    { id: 5, role: "user", text: "https://app.notion.com/p/Grocery-3944..." },
    { id: 6, role: "assistant", text: "https://app.notion.com/p/Grocery-3944..." },
    { id: 7, role: "user", text: "https://app.notion.com/p/Grocery-3944..." },
    { id: 8, role: "assistant", text: "https://app.notion.com/p/Grocery-3944..." },
    {
      id: 9,
      role: "user",
      text: `Of course I'll help you! But first, I want to get to know you so I need some context on how you currently budget your grocery. Ways to give me context is by either of this following:\na. Give me link with public access (Excel sheets, Notion)\nb. Send notes file (txt, docs, excel)\nc. Type info directly to chat.\n\nThen from there, I can curate the best list for your upcoming grocery :)`,
    },
  ];

  const [chatHistory, setChatHistory] = useState<ChatMessage[]>(initialChatHistory);

  const handleSendMessage = async (value: string) => {
    const trimmedValue = value.trim();

    if (!trimmedValue || isInputDisabled) {
      return;
    }

    setIsInputDisabled(true);

    const userMessageId = Date.now();
    setChatHistory((prev) => [
      ...prev,
      {
        id: userMessageId,
        role: "user",
        text: trimmedValue,
      },
    ]);

    try {
      const response = await sendChatMessage(trimmedValue);
      const assistantReply = response.reply ?? response.message ?? "I received your message.";

      setChatHistory((prev) => [
        ...prev,
        {
          id: userMessageId + 1,
          role: "assistant",
          text: assistantReply,
        },
      ]);
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Something went wrong.";

      setChatHistory((prev) => [
        ...prev,
        {
          id: userMessageId + 1,
          role: "assistant",
          text: `Error: ${errorMessage}`,
        },
      ]);
    } finally {
      setIsInputDisabled(false);
    }
  };

  return (
    <main className="flex h-screen flex-col px-96">
      <Header />
      <MessageList messages={chatHistory} />
      <Chatbox onSend={handleSendMessage} isDisabled={isInputDisabled} />
    </main>
  );
}
