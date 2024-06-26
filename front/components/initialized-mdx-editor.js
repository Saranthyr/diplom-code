import {
  headingsPlugin,
  listsPlugin,
  quotePlugin,
  thematicBreakPlugin,
  markdownShortcutPlugin,
  MDXEditor,
  toolbarPlugin,
  UndoRedo,
  BoldItalicUnderlineToggles,
  CreateLink,
  linkDialogPlugin,
  BlockTypeSelect,
} from "@mdxeditor/editor";
import "@mdxeditor/editor/style.css";

export default function InitializedMDXEditor({ editorRef, ...props }) {
  return (
    <MDXEditor
      className="border rounded-xl min-h-96"
      plugins={[
        headingsPlugin(),
        listsPlugin(),
        quotePlugin(),
        thematicBreakPlugin(),
        markdownShortcutPlugin(),
        linkDialogPlugin(),
        toolbarPlugin({
          toolbarContents: () => (
            <>
              <BlockTypeSelect />
              <UndoRedo />
              <BoldItalicUnderlineToggles />
              <CreateLink />
            </>
          ),
        }),
      ]}
      {...props}
      ref={editorRef}
    />
  );
}
