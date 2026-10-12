
import { useState } from "react";
import {
  Activity,
  AlertTriangle,
  Building2,
  Droplets,
  LayoutDashboard,
  Leaf,
  Recycle,
  ShieldCheck,
  Zap,
  Menu,
  X,
  ArrowUpRight,
} from "lucide-react";

import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

import {
  buildings,
  resourceTotals,
  consumptionData,
  alerts,
} from "./data/demoData";

import "./Dashboard.css";

const iconMap = {
  Zap,
  Droplets,
  Recycle,
  Leaf,
};

function Dashboard() {
  const [selectedBuilding, setSelectedBuilding] = useState("All buildings");
  const [selectedResource, setSelectedResource] = useState("electricity");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [activeSection, setActiveSection] = useState("Overview");

  const filteredAlerts =
    selectedBuilding === "All buildings"
      ? alerts
      : alerts.filter((alert) => alert.building === selectedBuilding);

  const resourceLabel =
    selectedResource.charAt(0).toUpperCase() + selectedResource.slice(1);

  const resourceUnit = {
    electricity: "kWh",
    water: "L (demo units)",
    waste: "kg",
  }[selectedResource];

  function navigateTo(section) {
    setActiveSection(section);
    setSidebarOpen(false);

    const element = document.getElementById(
      section.toLowerCase().replaceAll(" ", "-")
    );

    element?.scrollIntoView({ behavior: "smooth" });
  }

  return (
    <main className="dashboard">
      {sidebarOpen && (
        <button
          className="sidebar-overlay"
          aria-label="Close navigation"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      <aside className={`dashboard-sidebar ${sidebarOpen ? "sidebar-open" : ""}`}>
        <a className="dashboard-brand" href="/">
          <span className="dashboard-brand-mark">S</span>
          <span>SENTINEL<span className="brand-dot">.</span></span>
        </a>

        <div className="workspace-label">WORKSPACE</div>

        {[
          { name: "Overview", icon: LayoutDashboard },
          { name: "Resources", icon: Activity },
          { name: "Anomalies", icon: AlertTriangle },
          { name: "Buildings", icon: Building2 },
          { name: "Recommendations", icon: ShieldCheck },
        ].map(({ name, icon: Icon }) => (
          <button
            className={`sidebar-link ${activeSection === name ? "active" : ""}`}
            key={name}
            onClick={() => navigateTo(name)}
          >
            <Icon size={17} />
            <span>{name}</span>
          </button>
        ))}

        <div className="sidebar-bottom">
          <span className="sidebar-status-dot" />
          FRONTEND DEMO MODE
        </div>
      </aside>

      <section className="dashboard-main">
        <header className="dashboard-header">
          <button
            className="mobile-nav-toggle"
            aria-label={sidebarOpen ? "Close menu" : "Open menu"}
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            {sidebarOpen ? <X /> : <Menu />}
          </button>

          <div>
            <div className="dashboard-breadcrumb">SENTINEL / WORKSPACE</div>
            <h1>Campus overview</h1>
            <p>Understand your campus. Make smarter decisions.</p>
          </div>

          <span className="demo-tag">● DEMO DATA</span>
        </header>

        <section className="dashboard-welcome" id="overview">
          <div>
            <span className="dashboard-eyebrow">CAMPUS INTELLIGENCE SYSTEM</span>
            <h2>Every resource tells a story.</h2>
            <p>
              A unified view of resource consumption, potential anomalies,
              and campus sustainability.
            </p>
          </div>
          <div className="welcome-orbit" aria-hidden="true">S</div>
        </section>

        <section className="dashboard-section" id="resources">
          <div className="dashboard-section-heading">
            <div>
              <span className="section-overline">RESOURCE MONITORING</span>
              <h2>Resource overview</h2>
            </div>

            <select
              aria-label="Filter dashboard by building"
              value={selectedBuilding}
              onChange={(event) => setSelectedBuilding(event.target.value)}
            >
              <option>All buildings</option>
              {buildings.map((building) => (
                <option key={building}>{building}</option>
              ))}
            </select>
          </div>

          <div className="resource-grid">
            {resourceTotals.map((resource) => {
              const Icon = iconMap[resource.icon];

              return (
                <article className="resource-card" key={resource.name}>
                  <div className="resource-card-top">
                    <span className="resource-icon"><Icon size={20} /></span>
                    <ArrowUpRight size={17} className="resource-arrow" />
                  </div>

                  <p>{resource.name}</p>

                  <div className="resource-value">
                    {resource.value}
                    <span>{resource.unit}</span>
                  </div>

                  <small>{resource.change}</small>
                </article>
              );
            })}
          </div>
        </section>

        <section className="dashboard-panel" id="anomalies">
          <div className="dashboard-section-heading">
            <div>
              <span className="section-overline">PATTERN MONITORING</span>
              <h2>Consumption analytics</h2>
            </div>

            <select
              aria-label="Choose resource chart"
              value={selectedResource}
              onChange={(event) => setSelectedResource(event.target.value)}
            >
              <option value="electricity">Electricity</option>
              <option value="water">Water</option>
              <option value="waste">Waste</option>
            </select>
          </div>

          <p className="chart-caption">
            Illustrative weekly trend · {resourceLabel} · {resourceUnit}
          </p>

          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={consumptionData}>
                <defs>
                  <linearGradient id="resourceGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#9b76ff" stopOpacity={0.35} />
                    <stop offset="100%" stopColor="#9b76ff" stopOpacity={0.01} />
                  </linearGradient>
                </defs>

                <CartesianGrid stroke="#ffffff10" vertical={false} />

                <XAxis
                  dataKey="day"
                  stroke="#8f8a9f"
                  tickLine={false}
                  axisLine={false}
                  tick={{ fontSize: 11 }}
                />

                <YAxis
                  stroke="#8f8a9f"
                  tickLine={false}
                  axisLine={false}
                  tick={{ fontSize: 11 }}
                  width={38}
                />

                <Tooltip
                  contentStyle={{
                    background: "#15121f",
                    border: "1px solid #594580",
                    borderRadius: 8,
                    color: "#ffffff",
                  }}
                />

                <Area
                  type="monotone"
                  dataKey={selectedResource}
                  stroke="#a68aff"
                  strokeWidth={2.5}
                  fill="url(#resourceGradient)"
                  activeDot={{ r: 5, fill: "#c7b3ff" }}
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="dashboard-panel" id="buildings">
          <div className="dashboard-section-heading">
            <div>
              <span className="section-overline">CAMPUS DIRECTORY</span>
              <h2>Buildings & spaces</h2>
            </div>
            <span className="panel-count">05 BUILDINGS</span>
          </div>

          <div className="building-list">
            {buildings.map((building, index) => (
              <button
                className="dashboard-building"
                key={building}
                onClick={() => {
                  setSelectedBuilding(building);
                  setActiveSection("Buildings");
                }}
              >
                <span className="building-code">
                  {String(index + 1).padStart(2, "0")}
                </span>

                <span className="building-details">
                  <strong>{building}</strong>
                  <small>Resource monitoring · Demo preview</small>
                </span>

                <ArrowUpRight size={17} />
              </button>
            ))}
          </div>

          <div className="integration-note">
            <Building2 size={17} />
            <p>
              <strong>Campus map integration point</strong>
              <span>
                A Google Maps view and verified building coordinates can be
                added here later.
              </span>
            </p>
          </div>
        </section>

        <section className="dashboard-panel" id="recommendations">
          <div className="dashboard-section-heading">
            <div>
              <span className="section-overline">ATTENTION REQUIRED</span>
              <h2>Resource alerts</h2>
            </div>
            <span className="panel-count">{filteredAlerts.length} DEMO ALERTS</span>
          </div>

          <div className="alert-list">
            {filteredAlerts.length > 0 ? (
              filteredAlerts.map((alert) => (
                <article className="alert-item" key={alert.id}>
                  <span className={`alert-icon severity-${alert.severity.toLowerCase()}`}>
                    <AlertTriangle size={18} />
                  </span>

                  <div className="alert-details">
                    <strong>{alert.title}</strong>
                    <span>{alert.building} · {alert.resource}</span>
                  </div>

                  <span className={`severity-tag severity-${alert.severity.toLowerCase()}`}>
                    {alert.severity}
                  </span>
                </article>
              ))
            ) : (
              <p className="empty-alert">
                No demo alerts for this building.
              </p>
            )}
          </div>

          <p className="demo-disclaimer">
            Demo interface only. Metrics, trends, and alerts are illustrative;
            no live readings or detection service is connected.
          </p>
        </section>

        <footer className="dashboard-footer">
          SENTINEL · CAMPUS INTELLIGENCE
          <span>FRONTEND PREVIEW</span>
          <a href="/resources">Explore resource details ↗</a>
        </footer>
      </section>
    </main>
  );
  
}

export default Dashboard;
