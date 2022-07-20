import { useState } from "react";
import { Button, Container, Col, Form, Row } from 'react-bootstrap';

export default function Tags() {
  const [spotifyLink, setSpotifyLink] = useState('');
  const [tag, setTag] = useState('');
  const [vocals, setVocals] = useState(false);
  const [numSongs, setNumSongs] = useState('1');

  // These boolean states might not be necessary
  const [tagSelected, setTagSelected] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  

  const handleRadiobutton = (e) => {
    setTag(e.target.value);
    setTagSelected(true);
  }

  const handleCheckbox = (e) => {
    setVocals(!vocals);
  }

  const handleSubmit = (e) => {
    setSubmitted(true);
    // Limit the number of recommendations to 1 for now
    let request = 'http://localhost:8000/get-recommendations?mood=' + tag + '&vocals=' + vocals.toString() + '&limit=' + numSongs;
    fetch(request)
      .then(res => res.json())
      .then(data => setSpotifyLink('https://open.spotify.com/track/' + data));
    /*
    // TODO: Get the name of the song
    console.log(spotifyLink);
    fetch(spotifyLink)
      .then(res => res.json())
      .then(data => console.log(data));
    */
  }

  // TODO: Put the name of the song
  const SongLink = () => (
    <p>
      <br/>
      <a 
        href={spotifyLink} 
        target="_blank" 
        rel="noreferrer">
        Spotify link to song
      </a>
    </p>
  )

  
  return (
    <Container>
      <Form>
        <Row>
          <h3>Select your tags</h3>
          <Col>
            <h3>Mood</h3>
            {['happy', 'sad', 'horror'].map((tag) => (
              <div key={tag} className="mb-3">
                <Form.Check 
                  name='tag'
                  type='radio'
                  id={tag}
                  label={tag}
                  value={tag}
                  onChange={handleRadiobutton}
                />
              </div>
            ))}
          </Col>
          <Col>
            <h3>Options</h3>
            {['vocals'].map((tag) => (
              <div key={tag} className="mb-3">
                <Form.Check 
                  name='options'
                  type='checkbox'
                  id={tag}
                  label={tag}
                  value={tag}
                  onChange={handleCheckbox}
                />
              </div>
            ))}
          </Col>
        </Row>
        <Button 
          onClick={handleSubmit}
          disabled={!tagSelected}
        >
          Submit
        </Button>
        {submitted && <SongLink />}
      </Form>
    </Container>
  );
  
  /*
  return (
    <main style={{ padding: "1rem 0" }}>
      <h2>Select your tags</h2>
      happy 
      <input 
        type="radio" 
        name="tag" 
        value="happy"
        onChange={handleRadiobutton} />
      {" "} horror 
      <input 
        type="radio" 
        name="tag" 
        value="horror"
        onChange={handleRadiobutton} />
      {" "} sad 
      <input 
        type="radio" 
        name="tag" 
        value="sad"
        onChange={handleRadiobutton} />
      <br/>
      vocals 
      <input 
        type="checkbox" 
        name="tag" 
        value="vocals"
        onChange={handleCheckbox} />
      <br/>
      {tagSelected && <Button onClick={handleSubmit}>Submit</Button>}
      {submitted && <SongLink />}
    </main>
  );
  */
}