import { useState } from "react";
import Button from 'react-bootstrap/Button';

export default function Text() {

  const [text, setText] = useState('');

  const handleSubmit = (e) => {
    console.log(text);
  }

  return (
    <main style={{ padding: "1rem 0" }}>
      <h2>Enter your text</h2>
      <input
        type="text"
        required
        value={ text }
        onChange={(e) => setText(e.target.value)}
      />
      <Button onClick={handleSubmit}>Submit</Button>
    </main>
  );
}