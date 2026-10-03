import * as React from "react";
import { cn } from "@/lib/utils";

type MessageProps = Omit<React.HTMLAttributes<HTMLDivElement>, "title"> & {
  title?: React.ReactNode;
  description?: React.ReactNode;
};

function Message({ className, title, description, children, ...props }: MessageProps) {
  return (
    <div
      role="status"
      className={cn("p-3 rounded-2xl bg-muted text-muted-foreground", className)}
      {...props}
    >
      {title ? <div className="font-medium">{title}</div> : null}
      {description ? <div className="mt-1 text-sm text-muted-foreground">{description}</div> : null}
      {!title && !description ? <div>{children}</div> : null}
    </div>
  );
}

export { Message };
