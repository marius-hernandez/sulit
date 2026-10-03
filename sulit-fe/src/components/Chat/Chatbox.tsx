import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ArrowUp } from "lucide-react";
import React from "react";

const Chatbox = ({ onSend, isDisabled }: { onSend: (value: string) => void; isDisabled: boolean }) => {
  const [inputValue, setInputValue] = React.useState("");

  const handleSend = () => {
    const trimmedValue = inputValue.trim();

    if (!trimmedValue || isDisabled) {
      return;
    }

    onSend(trimmedValue);
    setInputValue("");
  };

  return (
    <div className="chatbox-input mt-5 flex items-center">
      <Input
        value={inputValue}
        disabled={isDisabled}
        onChange={(e) => setInputValue((e.target as HTMLInputElement).value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            handleSend();
          }
        }}
        placeholder="What's on your mind?"
        className="h-13 flex-1 border-border bg-input px-4 text-[15px] text-foreground shadow-none placeholder:text-muted-foreground focus-visible:ring-0 disabled:cursor-not-allowed disabled:opacity-70"
      />

      <Button
        size="icon"
        disabled={isDisabled}
        className="h-12 w-12 rounded-full bg-primary text-white hover:bg-primary/90 disabled:cursor-not-allowed disabled:opacity-70"
        aria-label="Send"
        onClick={handleSend}
      >
        <ArrowUp className="h-4 w-4" strokeWidth={2.6} />
      </Button>
    </div>
  );
};

export default Chatbox;
