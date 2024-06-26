"use client";

import dynamic from "next/dynamic";
import { forwardRef } from "react";

const Editor = dynamic(() => import("./initialized-mdx-editor.js"), {
  ssr: false,
});

export const MarkdownEditor = forwardRef((props, ref) => (
  <Editor {...props} editorRef={ref} />
));

MarkdownEditor.displayName = "MarkdownEditor";
