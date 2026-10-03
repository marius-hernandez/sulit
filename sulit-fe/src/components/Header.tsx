import { Menu } from "lucide-react";

import { Button } from "@/components/ui/button";

export default function Header() {
  return (
    <header className="flex items-center w-full bg-yellow-500">
      <Button
        variant="ghost"
        size="icon"
        className="h-9 w-9 rounded-full text-foreground hover:bg-muted/50"
        aria-label="Open menu"
      >
        <Menu className="h-5 w-5" strokeWidth={2.2} />
      </Button>

      <div className="title-bar w-full">
        <h1 className="text-[18px] font-semibold tracking-[-0.02em] text-foreground">
          Sulit
        </h1>
        <p className="mt-2 text-[14px] font-medium tracking-[-0.01em] text-muted-foreground">
          Status: ready
        </p>
      </div>
    </header>
  );
}
