import { useState } from "react";
import { Button, Container, Col, Form, Row } from 'react-bootstrap';

export default function Tags() {
  const [tag, setTag] = useState('');
  const [vocals, setVocals] = useState(false);
  const [numSongs, setNumSongs] = useState('1');
  const [songInfo, setSongInfo] = useState({
    name: '',
    artist: '',
    link: '',
    image: '',
  });

  // These boolean states might not be necessary
  const [tagSelected, setTagSelected] = useState(false);
  

  const handleRadiobutton = (e) => {
    setTag(e.target.value);
    setTagSelected(true);
  }

  const handleCheckbox = (e) => {
    setVocals(!vocals);
  }

  const handleSubmit = (e) => {
    
    // Limit the number of recommendations to 1 for now
    let request = 'http://localhost:8000/get-recommendations?mood=' + tag + '&vocals=' + vocals.toString() + '&limit=' + numSongs;
    fetch(request)
      .then(res => res.json())
      .then(tID => { return fetch('http://localhost:8000/get-tracks?track_ids=' + tID) })
      .then(res => res.json())
      .then(data => {
        setSongInfo({
          artist: data[0].artists[0].name,
          name: data[0].name,
          link: data[0].external_urls.spotify,
          image: data[0].album.images[0].url,
        })
      });
  }

  const SongLink = () => (
    <p>
      <br/>
      <a 
        href={songInfo.link} 
        target="_blank" 
        rel="noreferrer">
        <img 
          src={songInfo.image}
          alt=''
          width='256'
          height='256'>
        </img>
        <br/>
        {songInfo.artist + ' - ' + songInfo.name}
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
        {(songInfo.link !== '') && <SongLink />}
      </Form>
    </Container>
  );
}