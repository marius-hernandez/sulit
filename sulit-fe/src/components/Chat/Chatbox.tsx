"use client";

import { useState, type FormEvent } from "react";
import { ArrowUp } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

// Must stay in sync with the backend's ChatRequest @Size limit.
const MAX_MESSAGE_LENGTH = 4000;

type ChatboxProps = {
  onSend: (value: string) => void;
  isDisabled: boolean;
};

export default function Chatbox({ onSend, isDisabled }: ChatboxProps) {
  const [inputValue, setInputValue] = useState("");
  const trimmedValue = inputValue.trim();
  const canSend = trimmedValue.length > 0 && !isDisabled;


  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!canSend) {
      return;
    }
    onSend(trimmedValue);
    setInputValue("");
  };

  return (
    <form className="chatbox-input mt-5 flex items-center gap-2" onSubmit={handleSubmit}>
      <Input
        value={inputValue}
        onChange={(e) => setInputValue(e.currentTarget.value)}
        maxLength={MAX_MESSAGE_LENGTH}
        placeholder="What's on your mind?"
        aria-label="Message"
        autoComplete="off"
        className="h-13 flex-1 border-border bg-input px-4 text-[15px] text-foreground shadow-none placeholder:text-muted-foreground focus-visible:ring-0"
      />

      <Button
        type="submit"
        size="icon"
        disabled={!canSend}
        className="h-12 w-12 rounded-full bg-primary text-white hover:bg-primary/90 disabled:cursor-not-allowed disabled:opacity-70"
        aria-label="Send"
      >
        <ArrowUp className="h-4 w-4" strokeWidth={2.6} />
      </Button>
    </form>
  );
}
