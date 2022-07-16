import { useState } from "react";
import Button from 'react-bootstrap/Button';

export default function Tags() {
  const [tags, setTags] = useState({
    happy: false,
    horror: false,
    sad: false
  });

  const handleCheckbox = (e) => {
    let tag = e.target.value;
    let newTags = tags;
    if(tag === "happy"){
      newTags.happy = !tags.happy;
    }
    if(tag === "horror"){
      newTags.horror = !tags.horror;
    }
    if(tag === "sad"){
      newTags.sad = !tags.sad;
    }
    setTags(newTags);
    //console.log(tags);
  }

  const handleSubmit = (e) => {
    console.log(tags);
  }
  
  return (
    <main style={{ padding: "1rem 0" }}>
      <h2>Select your tags</h2>
      happy 
      <input 
        type="checkbox" 
        name="tag" 
        value="happy"
        onChange={handleCheckbox} />
      horror 
      <input 
        type="checkbox" 
        name="tag" 
        value="horror"
        onChange={handleCheckbox} />
      sad 
      <input 
        type="checkbox" 
        name="tag" 
        value="sad"
        onChange={handleCheckbox} />
      <Button onClick={handleSubmit}>Submit</Button>
    </main>
  );
}