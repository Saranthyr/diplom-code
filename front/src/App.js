import { useState } from "react";

function Square() {
  const [val, setVal] = useState(null);
  function handleClick() {
    setVal("X");
  }
  return (
    <button className="square" onClick={handleClick}>
      {val}
    </button>
  );
}

export default function Board() {
  return (
    <>
      <div className="board-row">
        <Square />
        <Square />
        <Square />
      </div>
      <div className="board-row">
        <Square />
        <Square />
        <Square />
      </div>
      <div className="board-row">
        <Square />
        <Square />
        <Square />
      </div>
    </>
  );
}
