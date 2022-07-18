import { useState } from "react";
import Button from 'react-bootstrap/Button';

export default function Tags() {
  const [tags, setTags] = useState({
    happy: false,
    horror: false,
    sad: false
  });

  const handleRadiobutton = (e) => {
    let tag = e.target.value;
    let newTags = {
      happy: false,
      horror: false,
      sad: false
    };
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
        type="radio" 
        name="tag" 
        value="happy"
        onChange={handleRadiobutton} />
      horror 
      <input 
        type="radio" 
        name="tag" 
        value="horror"
        onChange={handleRadiobutton} />
      sad 
      <input 
        type="radio" 
        name="tag" 
        value="sad"
        onChange={handleRadiobutton} />
      <Button onClick={handleSubmit}>Submit</Button>
    </main>
  );
}