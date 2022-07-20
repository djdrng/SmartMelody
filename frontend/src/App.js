import './App.css';

import { Outlet, Link } from "react-router-dom";
import { Button, Card } from "react-bootstrap";

export default function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Card style={{ color: "#000 "}}>
          <Card.Body>
            <Card.Title>
            <h1><b><i>SmartMelody</i></b></h1>
            </Card.Title>
            <Card.Text>
              <nav
                style={{
                  borderBottom: "solid 1px",
                  paddingBottom: "1rem",
                }}
              >
                <Link to="/text">
                  <Button variant="outline-dark">Text</Button>
                </Link> {" "}
                <Link to="/tags">
                  <Button variant="outline-dark">Tags</Button>
                </Link>
              </nav>
              <Outlet />
            </Card.Text>
          </Card.Body>
        </Card>
      </header>
    </div>
  );
}
