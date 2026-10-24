import { cn } from "@/lib/utils";
import type { ChatMessage } from "@/types/chat";
import MarkdownMessage from "../ui/MarkdownMessage";

export default function MessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";

  return (
    <div
      className={cn(
        "w-fit mt-4 max-w-[85%] md:max-w-1/2 rounded-[24px] px-4 py-3 text-[17px] whitespace-pre-wrap wrap-break-word",
        isUser && "ml-auto bg-primary text-primary-foreground",
        !isUser && !message.isError && "w-full bg-secondary text-secondary-foreground",
        message.isError && "bg-destructive/10 text-destructive",
      )}
    >
      <MarkdownMessage content={message.content} />
      {}
    </div>
  );
}
