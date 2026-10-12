
import { useEffect, useState } from "react";
import "./App.css";
import Dashboard from "./Dashboard.jsx";
import BuildingDetails from "./BuildingDetails.jsx";
import ResourceDetails from "./ResourceDetails.jsx";
import Anomalies from "./Anomalies.jsx";

function App() {
  const path = window.location.pathname;

  const [theme, setTheme] = useState(
    () => localStorage.getItem("sentinel-theme") || "system"
  );

  useEffect(() => {
    const root = document.documentElement;
    const media = window.matchMedia("(prefers-color-scheme: dark)");

    const applyTheme = () => {
      const activeTheme =
        theme === "system"
          ? media.matches
            ? "black"
            : "white"
          : theme;

      root.setAttribute("data-theme", activeTheme);
      root.style.colorScheme =
        activeTheme === "white" ? "light" : "dark";
    };

    applyTheme();
    media.addEventListener("change", applyTheme);

    return () => media.removeEventListener("change", applyTheme);
  }, [theme]);

  function changeTheme(newTheme) {
    localStorage.setItem("sentinel-theme", newTheme);
    setTheme(newTheme);
  }

  // Dashboard
  if (path === "/dashboard") {
    return (
      <Dashboard
        theme={theme}
        onThemeChange={changeTheme}
      />
    );
  }

  // Building details
  if (path === "/building") {
    return <BuildingDetails />;
  }

  // Resource details
  if (path === "/resources") {
    return <ResourceDetails />;
  }

  // Anomaly alerts
  if (path === "/anomalies") {
    return <Anomalies />;
  }

  // Landing page
  return (
    <main className="sentinel">
      <nav className="navbar">
        <a className="brand" href="#home">
          <span className="brand-mark">S</span>
          <span>
            SENTINEL<span className="brand-dot">.</span>
          </span>
        </a>

        <div className="nav-links">
          <a href="#about">ABOUT</a>
          <a href="#features">FEATURES</a>
          <a href="#campus">CAMPUS</a>
        </div>

        <a className="nav-cta" href="/dashboard">
          EXPLORE ↗
        </a>

        <a
          className="mobile-menu"
          href="#features"
          aria-label="Explore features"
        >
          ☰
        </a>
      </nav>

      <section className="hero" id="home">
        <div className="hero-copy">
          <div className="eyebrow">
            <span className="live-dot" />
            INTELLIGENT CAMPUS MONITORING
          </div>

          <h1>
            Stay ahead.
            <br />
            <span>See everything.</span>
          </h1>

          <p className="hero-description">
            Meet Sentinel — your campus resource intelligence
            platform. Detect unusual consumption, monitor
            electricity and water, and turn data into smarter
            sustainability decisions.
          </p>

          <form
            className="search-bar"
            onSubmit={(event) => {
              event.preventDefault();
              window.location.href = "/dashboard";
            }}
          >
            <span>⌕</span>
            <input
              type="text"
              aria-label="Search campus"
              placeholder="Explore your campus..."
            />
            <button type="submit" aria-label="Open dashboard">
              ↗
            </button>
          </form>

          <div className="hero-actions">
            <a className="button-primary" href="/dashboard">
              EXPLORE SENTINEL <span>↗</span>
            </a>
            <a className="button-secondary" href="#features">
              SEE HOW IT WORKS
            </a>
          </div>

          <div className="hero-footnote">
            <span className="footnote-line" />
            SMARTER INSIGHTS. MORE SUSTAINABLE FUTURES.
          </div>
        </div>

        <div className="hero-art" aria-hidden="true">
          <div className="art-glow" />

          <div className="contour contour-one">
            {Array.from({ length: 12 }, (_, i) => (
              <span key={i} style={{ "--i": i }} />
            ))}
          </div>

          <div className="contour contour-two">
            {Array.from({ length: 12 }, (_, i) => (
              <span key={i} style={{ "--i": i }} />
            ))}
          </div>

          <div className="art-caption">
            <span className="caption-symbol">◈</span>
            <p>Observe. Detect. Protect.</p>
            <small>ONE INTELLIGENT VIEW OF YOUR CAMPUS</small>
          </div>

          <div className="art-index">S / 360</div>
        </div>

        <div className="scroll-indicator">
          <span />
          SCROLL TO EXPLORE
        </div>
      </section>

      <section className="intro-section" id="about">
        <div>
          <span className="section-kicker">
            01 — THE BIG PICTURE
          </span>
          <h2>
            Your campus.
            <br />
            <span>Understood.</span>
          </h2>
        </div>

        <p>
          Resources leave signals. Sentinel helps bring those
          signals together, making it easier to understand
          usage patterns and identify areas that need attention.
        </p>
      </section>

      <section className="features-section" id="features">
        <div className="section-heading">
          <span className="section-kicker">
            02 — CORE CAPABILITIES
          </span>
          <h2>Intelligence in every signal.</h2>
        </div>

        <div className="features-grid">
          <article className="feature-card">
            <span className="feature-number">01</span>
            <span className="feature-icon">⌁</span>
            <h3>Resource monitoring</h3>
            <p>
              Understand electricity, water, and waste usage
              across campus spaces.
            </p>
            <a href="/resources">EXPLORE <span>↗</span></a>
          </article>

          <article className="feature-card">
            <span className="feature-number">02</span>
            <span className="feature-icon">◎</span>
            <h3>Anomaly detection</h3>
            <p>
              Highlight unusual consumption patterns that
              deserve a closer look.
            </p>
            <a href="/anomalies">EXPLORE <span>↗</span></a>
          </article>

          <article className="feature-card">
            <span className="feature-number">03</span>
            <span className="feature-icon">↗</span>
            <h3>Actionable insights</h3>
            <p>
              Turn resource data into practical recommendations
              for smarter campus operations.
            </p>
            <a href="/dashboard">EXPLORE <span>↗</span></a>
          </article>
        </div>
      </section>

      <section className="campus-section" id="campus">
        <div className="section-heading">
          <span className="section-kicker">
            03 — CAMPUS OVERVIEW
          </span>
          <h2>One campus. Five zones.</h2>
          <p>
            Explore the buildings included in the Sentinel demo.
          </p>
        </div>

        <div className="campus-grid">
          {[
            ["01", "Administration", "Campus operations"],
            ["02", "Maa Saraswati Block", "Academic building"],
            ["03", "EEE Block", "Labs & classrooms"],
            ["04", "Architecture Block", "Design studios"],
            ["05", "Library", "Learning resources"],
          ].map(([number, name, description]) => (
            <article className="campus-card" key={number}>
              <span className="campus-number">{number} / 05</span>
              <div className="campus-symbol">◇</div>
              <h3>{name}</h3>
              <p>{description}</p>

              <span className="demo-status">
                <span />
                DEMO SPACE
              </span>

              <a
                href={`/building?name=${encodeURIComponent(name)}`}
                className="campus-card-link"
              >
                VIEW BUILDING ↗
              </a>
            </article>
          ))}
        </div>

        <p className="demo-note">
          Campus cards are a preview. Live readings and verified
          building locations will be connected separately.
        </p>
      </section>

      <section className="closing-section">
        <span className="section-kicker">
          04 — THE NEXT MOVE
        </span>
        <h2>
          Awareness is power.
          <br />
          <span>Action is everything.</span>
        </h2>
        <a className="button-primary" href="/dashboard">
          OPEN DASHBOARD ↗
        </a>
      </section>

      <footer className="footer">
        <a className="brand" href="#home">
          <span className="brand-mark">S</span>
          <span>
            SENTINEL<span className="brand-dot">.</span>
          </span>
        </a>
        <p>Intelligence for a more sustainable campus.</p>
        <span>© SENTINEL · CAMPUS DEMO</span>
      </footer>
    </main>
  );
}

export default App;
