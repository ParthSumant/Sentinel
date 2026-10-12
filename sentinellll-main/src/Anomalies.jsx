
import { useState } from "react";
import {
  ArrowLeft,
  AlertTriangle,
  Search,
  ShieldCheck,
  Zap,
  Droplets,
  Recycle,
} from "lucide-react";
import { alerts } from "./data/demoData.js";
import "./Anomalies.css";

const resourceIcons = {
  Electricity: Zap,
  Water: Droplets,
  Waste: Recycle,
};

export default function Anomalies() {
  const [search, setSearch] = useState("");
  const [severity, setSeverity] = useState("All");
  const [resource, setResource] = useState("All");

  const filteredAlerts = alerts.filter((alert) => {
    const query = search.toLowerCase();

    const matchesSearch =
      alert.title.toLowerCase().includes(query) ||
      alert.building.toLowerCase().includes(query);

    const matchesSeverity =
      severity === "All" || alert.severity === severity;

    const matchesResource =
      resource === "All" || alert.resource === resource;

    return matchesSearch && matchesSeverity && matchesResource;
  });

  const highCount = alerts.filter(
    (alert) => alert.severity === "High"
  ).length;

  return (
    <main className="anomalies-page">
      <header className="anomalies-topbar">
        <button
          className="anomalies-back"
          onClick={() => (window.location.href = "/dashboard")}
        >
          <ArrowLeft size={18} />
          Back to dashboard
        </button>
        <span className="anomalies-demo">DEMO DATA</span>
      </header>

      <section className="anomalies-heading">
        <p className="anomalies-eyebrow">
          SENTINEL / CAMPUS MONITORING
        </p>
        <h1>Anomaly alerts</h1>
        <p>
          Review unusual resource patterns and identify spaces
          that may need attention.
        </p>
      </section>

      <section className="anomaly-summary">
        <article>
          <AlertTriangle size={22} />
          <span>Total demo alerts</span>
          <strong>{alerts.length}</strong>
        </article>

        <article>
          <ShieldCheck size={22} />
          <span>High-severity demo alerts</span>
          <strong>{highCount}</strong>
        </article>

        <article>
          <Search size={22} />
          <span>Matching alerts</span>
          <strong>{filteredAlerts.length}</strong>
        </article>
      </section>

      <section className="anomaly-list-section">
        <div className="anomaly-list-heading">
          <div>
            <p className="anomalies-eyebrow">ALERT MANAGEMENT</p>
            <h2>Campus alerts</h2>
          </div>
          <span>{filteredAlerts.length} results</span>
        </div>

        <div className="anomaly-filters">
          <label className="anomaly-search">
            <Search size={18} />
            <input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search alerts or buildings..."
            />
          </label>

          <select
            value={severity}
            onChange={(event) => setSeverity(event.target.value)}
            aria-label="Filter by severity"
          >
            <option value="All">All severities</option>
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
          </select>

          <select
            value={resource}
            onChange={(event) => setResource(event.target.value)}
            aria-label="Filter by resource"
          >
            <option value="All">All resources</option>
            <option value="Electricity">Electricity</option>
            <option value="Water">Water</option>
            <option value="Waste">Waste</option>
          </select>
        </div>

        <div className="anomaly-list">
          {filteredAlerts.map((alert) => {
            const Icon = resourceIcons[alert.resource] || AlertTriangle;

            return (
              <article className="anomaly-card" key={alert.id}>
                <div className="anomaly-resource-icon">
                  <Icon size={22} />
                </div>

                <div className="anomaly-card-content">
                  <div className="anomaly-card-title">
                    <h3>{alert.title}</h3>
                    <span
                      className={`severity-pill severity-${alert.severity.toLowerCase()}`}
                    >
                      {alert.severity}
                    </span>
                  </div>

                  <p>{alert.building}</p>

                  <div className="anomaly-card-meta">
                    <span>{alert.resource}</span>
                    <span>{alert.time}</span>
                  </div>
                </div>
              </article>
            );
          })}

          {filteredAlerts.length === 0 && (
            <div className="anomaly-empty">
              <Search size={25} />
              <h3>No matching alerts</h3>
              <p>Try changing your search or filters.</p>
            </div>
          )}
        </div>

        <p className="anomaly-disclaimer">
          These are illustrative demo alerts, not live detections.
          Real anomaly rules and sensor readings can be integrated later.
        </p>
      </section>
    </main>
  );
}
