import { useState } from "react";
import Button from 'react-bootstrap/Button';

export default function Tags() {
  const [trackID, setTrackID] = useState('');
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
    /*
    fetch('https://jsonplaceholder.typicode.com/users')
      .then(res => res.json())
      .then(json => console.log(json));
    */
    fetch('http://localhost:8000/get-recommendations?mood=happy&vocals=true&limit=1')
      .then(res => res.json())
      .then(json => setTrackID(json));
    //console.log(fetch('http://localhost:8000/get-recommendations?mood=happy&vocals=true&limit=1'));
    //console.log(tags);
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
      <p>{ trackID }</p>
    </main>
  );
}