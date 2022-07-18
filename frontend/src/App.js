import { Outlet, Link } from "react-router-dom";

export default function App() {
  return (
    <div>
      <h1>SmartMelody</h1>
      <nav
        style={{
          borderBottom: "solid 1px",
          paddingBottom: "1rem",
        }}
      >
        <Link to="/text">Text</Link> |{" "}
        <Link to="/tags">Tags</Link>
      </nav>
      <Outlet />
    </div>
  );
}
