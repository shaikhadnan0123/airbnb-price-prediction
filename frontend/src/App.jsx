import { useState, useEffect } from "react";
import "./App.css";

// Quick Preset Scenarios for realistic testing
const PRESETS = [
  {
    id: "manhattan-luxury",
    title: "Manhattan Midtown",
    badge: "Entire Home",
    icon: "🏙️",
    data: {
      neighbourhood_group: "Manhattan",
      neighbourhood: "Midtown",
      room_type: "Entire home/apt",
      latitude: 40.7549,
      longitude: -73.9840,
      minimum_nights: 2,
      number_of_reviews: 45,
      reviews_per_month: 1.5,
      calculated_host_listings_count: 1,
      availability_365: 180,
    },
  },
  {
    id: "brooklyn-bedstuy",
    title: "Brooklyn Bed-Stuy",
    badge: "Private Room",
    icon: "🎨",
    data: {
      neighbourhood_group: "Brooklyn",
      neighbourhood: "Bedford-Stuyvesant",
      room_type: "Private room",
      latitude: 40.6872,
      longitude: -73.9418,
      minimum_nights: 1,
      number_of_reviews: 28,
      reviews_per_month: 2.1,
      calculated_host_listings_count: 1,
      availability_365: 90,
    },
  },
  {
    id: "manhattan-uws",
    title: "Upper West Side",
    badge: "Entire Home",
    icon: "🌳",
    data: {
      neighbourhood_group: "Manhattan",
      neighbourhood: "Upper West Side",
      room_type: "Entire home/apt",
      latitude: 40.7870,
      longitude: -73.9750,
      minimum_nights: 3,
      number_of_reviews: 12,
      reviews_per_month: 0.8,
      calculated_host_listings_count: 2,
      availability_365: 220,
    },
  },
  {
    id: "queens-astoria",
    title: "Queens Astoria",
    badge: "Private Room",
    icon: "🌉",
    data: {
      neighbourhood_group: "Queens",
      neighbourhood: "Astoria",
      room_type: "Private room",
      latitude: 40.7644,
      longitude: -73.9235,
      minimum_nights: 1,
      number_of_reviews: 15,
      reviews_per_month: 1.2,
      calculated_host_listings_count: 1,
      availability_365: 150,
    },
  },
];

// Popular Neighbourhood Suggestions per Group
const NEIGHBOURHOOD_TAGS = {
  Manhattan: ["Midtown", "Upper West Side", "Harlem", "East Village", "Chelsea", "Financial District"],
  Brooklyn: ["Bedford-Stuyvesant", "Williamsburg", "Bushwick", "Crown Heights", "DUMBO"],
  Queens: ["Astoria", "Long Island City", "Flushing", "Sunnyside", "Ridgewood"],
  Bronx: ["Mott Haven", "Riverdale", "Concourse", "Fordham"],
  "Staten Island": ["St. George", "Tompkinsville", "Stapleton"],
};

function App() {
  const [formData, setFormData] = useState({
    neighbourhood_group: "Manhattan",
    neighbourhood: "Midtown",
    room_type: "Entire home/apt",
    latitude: 40.7549,
    longitude: -73.9840,
    minimum_nights: 2,
    number_of_reviews: 45,
    reviews_per_month: 1.5,
    calculated_host_listings_count: 1,
    availability_365: 180,
  });

  const [predictedPrice, setPredictedPrice] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [apiStatus, setApiStatus] = useState("checking"); // 'healthy' | 'offline' | 'checking'
  const [activePreset, setActivePreset] = useState("manhattan-luxury");

  // Check API health status on mount
  useEffect(() => {
    checkApiHealth();
  }, []);

  const checkApiHealth = async () => {
    setApiStatus("checking");
    try {
      const res = await fetch("http://127.0.0.1:5000/");
      if (res.ok) {
        setApiStatus("healthy");
      } else {
        setApiStatus("offline");
      }
    } catch {
      setApiStatus("offline");
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setActivePreset(null);

    setFormData((prev) => ({
      ...prev,
      [name]:
        name === "neighbourhood_group" ||
        name === "neighbourhood" ||
        name === "room_type"
          ? value
          : Number(value),
    }));
  };

  const handleSelectGroup = (group) => {
    setActivePreset(null);
    const defaultHood = NEIGHBOURHOOD_TAGS[group]?.[0] || "";
    setFormData((prev) => ({
      ...prev,
      neighbourhood_group: group,
      neighbourhood: defaultHood,
    }));
  };

  const handleSelectRoomType = (roomType) => {
    setActivePreset(null);
    setFormData((prev) => ({
      ...prev,
      room_type: roomType,
    }));
  };

  const handleApplyPreset = (preset) => {
    setActivePreset(preset.id);
    setFormData(preset.data);
    setPredictedPrice(null);
    setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setPredictedPrice(null);

    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.error || "Prediction request failed");
      }

      setPredictedPrice(result.predicted_price);
      setApiStatus("healthy");

      // Scroll smoothly to prediction result card
      setTimeout(() => {
        const resultElem = document.getElementById("prediction-result");
        if (resultElem) {
          resultElem.scrollIntoView({ behavior: "smooth", block: "nearest" });
        }
      }, 100);
    } catch (err) {
      setError(
        err.message.includes("Failed to fetch")
          ? "Unable to connect to Flask API backend (http://127.0.0.1:5000). Please ensure your Flask server is running!"
          : err.message
      );
    } finally {
      setLoading(false);
    }
  };

  // Helper for price tier analysis display
  const getPriceTier = (price) => {
    if (price <= 100) return { label: "Budget Tier", badge: "budget", color: "#10B981", range: "$0 – $100/night" };
    if (price <= 200) return { label: "Mid-Range Tier", badge: "midrange", color: "#3B82F6", range: "$100 – $200/night" };
    return { label: "High-End Tier", badge: "highend", color: "#8B5CF6", range: "$200 – $500/night" };
  };

  const locationInteraction = (formData.latitude * formData.longitude).toFixed(2);

  return (
    <div className="app-shell">
      {/* Background Glow Overlay */}
      <div className="bg-glow bg-glow-1"></div>
      <div className="bg-glow bg-glow-2"></div>

      {/* Main Container */}
      <div className="main-wrapper">
        {/* Header */}
        <header className="app-header">
          <div className="brand-badge">
            <svg className="brand-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
              <polyline points="9 22 9 12 15 12 15 22"></polyline>
            </svg>
            <span>NYC Airbnb Intelligence</span>
          </div>

          <h1 className="hero-title">
            NYC Airbnb Price Predictor
          </h1>

          <p className="hero-description">
            Estimate nightly listing prices powered by an <strong>Extra Trees Regressor</strong> machine learning model trained on NYC listings ($10 – $500/night scope).
          </p>

          <div className="status-bar">
            <div className={`status-pill ${apiStatus}`}>
              <span className="status-dot"></span>
              {apiStatus === "healthy" && "Flask API Online (Extra Trees Active)"}
              {apiStatus === "offline" && "Flask API Offline (127.0.0.1:5000)"}
              {apiStatus === "checking" && "Connecting to API..."}
            </div>

            <button type="button" onClick={checkApiHealth} className="ping-btn" title="Check connection status">
              <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/>
              </svg>
              Check Status
            </button>
          </div>
        </header>

        {/* Quick Scenarios Bar */}
        <section className="preset-section">
          <div className="preset-title">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2">
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
            </svg>
            <span>Try Preset NYC Scenarios</span>
          </div>

          <div className="preset-grid">
            {PRESETS.map((preset) => (
              <button
                key={preset.id}
                type="button"
                className={`preset-card ${activePreset === preset.id ? "active" : ""}`}
                onClick={() => handleApplyPreset(preset)}
              >
                <span className="preset-emoji">{preset.icon}</span>
                <div className="preset-info">
                  <div className="preset-name">{preset.title}</div>
                  <div className="preset-badge">{preset.badge}</div>
                </div>
              </button>
            ))}
          </div>
        </section>

        {/* Predictor Form */}
        <form onSubmit={handleSubmit} className="predictor-form">
          
          {/* SECTION 1: LOCATION */}
          <div className="form-card">
            <div className="card-header">
              <div className="card-icon-wrapper">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                  <circle cx="12" cy="10" r="3"></circle>
                </svg>
              </div>
              <div>
                <h3 className="card-title">1. Location & Geographic Data</h3>
                <p className="card-subtitle">NYC Neighbourhood Group and GPS coordinates</p>
              </div>
            </div>

            {/* Neighbourhood Group Tabs */}
            <div className="form-field">
              <label className="field-label">Neighbourhood Group (Borough)</label>
              <div className="borough-tabs">
                {["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island"].map((b) => (
                  <button
                    key={b}
                    type="button"
                    className={`borough-btn ${formData.neighbourhood_group === b ? "active" : ""}`}
                    onClick={() => handleSelectGroup(b)}
                  >
                    {b}
                  </button>
                ))}
              </div>
            </div>

            {/* Neighbourhood Input & Tags */}
            <div className="form-grid-2">
              <div className="form-field">
                <label className="field-label" htmlFor="neighbourhood">
                  Neighbourhood Name
                </label>
                <input
                  id="neighbourhood"
                  type="text"
                  name="neighbourhood"
                  value={formData.neighbourhood}
                  onChange={handleChange}
                  placeholder="e.g. Midtown, Astoria"
                  className="custom-input"
                  required
                />
                
                {/* Popular Tags */}
                {NEIGHBOURHOOD_TAGS[formData.neighbourhood_group] && (
                  <div className="tag-chips">
                    <span className="tag-label">Suggestions:</span>
                    {NEIGHBOURHOOD_TAGS[formData.neighbourhood_group].slice(0, 4).map((tag) => (
                      <button
                        key={tag}
                        type="button"
                        className={`chip-btn ${formData.neighbourhood === tag ? "active" : ""}`}
                        onClick={() => {
                          setActivePreset(null);
                          setFormData((prev) => ({ ...prev, neighbourhood: tag }));
                        }}
                      >
                        {tag}
                      </button>
                    ))}
                  </div>
                )}
              </div>

              {/* Coordinates Grid */}
              <div className="coords-subgrid">
                <div className="form-field">
                  <label className="field-label" htmlFor="latitude">
                    Latitude
                  </label>
                  <input
                    id="latitude"
                    type="number"
                    step="any"
                    name="latitude"
                    value={formData.latitude}
                    onChange={handleChange}
                    className="custom-input mono"
                    required
                  />
                </div>

                <div className="form-field">
                  <label className="field-label" htmlFor="longitude">
                    Longitude
                  </label>
                  <input
                    id="longitude"
                    type="number"
                    step="any"
                    name="longitude"
                    value={formData.longitude}
                    onChange={handleChange}
                    className="custom-input mono"
                    required
                  />
                </div>
              </div>
            </div>

            {/* Feature Engineering Highlight */}
            <div className="feature-tip">
              <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#F59E0B" strokeWidth="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="16" x2="12" y2="12"></line>
                <line x1="12" y1="8" x2="12.01" y2="8"></line>
              </svg>
              <span>
                Engineered Feature: <code>location_interaction</code> (lat × long) = <strong>{locationInteraction}</strong> calculated automatically for model input.
              </span>
            </div>
          </div>

          {/* SECTION 2: PROPERTY & ROOM TYPE */}
          <div className="form-card">
            <div className="card-header">
              <div className="card-icon-wrapper">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                  <line x1="9" y1="3" x2="9" y2="21"></line>
                </svg>
              </div>
              <div>
                <h3 className="card-title">2. Property Category</h3>
                <p className="card-subtitle">Room type selection (Primary price driver in NYC model)</p>
              </div>
            </div>

            <div className="room-grid">
              {[
                {
                  type: "Entire home/apt",
                  label: "Entire Home / Apt",
                  desc: "Full private home or apartment unit",
                  icon: "🏠",
                },
                {
                  type: "Private room",
                  label: "Private Room",
                  desc: "Private bedroom in shared space",
                  icon: "🔑",
                },
                {
                  type: "Shared room",
                  label: "Shared Room",
                  desc: "Shared bedroom or sleeping area",
                  icon: "🛋️",
                },
              ].map((rt) => (
                <div
                  key={rt.type}
                  className={`room-card ${formData.room_type === rt.type ? "selected" : ""}`}
                  onClick={() => handleSelectRoomType(rt.type)}
                >
                  <div className="room-header">
                    <span className="room-icon">{rt.icon}</span>
                    {formData.room_type === rt.type && (
                      <span className="room-check">
                        <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" strokeWidth="3">
                          <polyline points="20 6 9 17 4 12"></polyline>
                        </svg>
                      </span>
                    )}
                  </div>
                  <h4 className="room-title">{rt.label}</h4>
                  <p className="room-desc">{rt.desc}</p>
                </div>
              ))}
            </div>
          </div>

          {/* SECTION 3: LISTING & HOST PARAMETERS */}
          <div className="form-card">
            <div className="card-header">
              <div className="card-icon-wrapper">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                  <line x1="16" y1="2" x2="16" y2="6"></line>
                  <line x1="8" y1="2" x2="8" y2="6"></line>
                  <line x1="3" y1="10" x2="21" y2="10"></line>
                </svg>
              </div>
              <div>
                <h3 className="card-title">3. Listing Specs & Host Statistics</h3>
                <p className="card-subtitle">Stay restrictions, reviews, and annual availability</p>
              </div>
            </div>

            <div className="form-grid-3">
              {/* Minimum Nights */}
              <div className="form-field">
                <label className="field-label" htmlFor="minimum_nights">
                  Minimum Nights
                </label>
                <div className="number-stepper">
                  <input
                    id="minimum_nights"
                    type="number"
                    min="1"
                    max="365"
                    name="minimum_nights"
                    value={formData.minimum_nights}
                    onChange={handleChange}
                    className="custom-input"
                    required
                  />
                </div>
              </div>

              {/* Number of Reviews */}
              <div className="form-field">
                <label className="field-label" htmlFor="number_of_reviews">
                  Total Reviews
                </label>
                <input
                  id="number_of_reviews"
                  type="number"
                  min="0"
                  name="number_of_reviews"
                  value={formData.number_of_reviews}
                  onChange={handleChange}
                  className="custom-input"
                  required
                />
              </div>

              {/* Reviews Per Month */}
              <div className="form-field">
                <label className="field-label" htmlFor="reviews_per_month">
                  Reviews / Month
                </label>
                <input
                  id="reviews_per_month"
                  type="number"
                  step="0.01"
                  min="0"
                  name="reviews_per_month"
                  value={formData.reviews_per_month}
                  onChange={handleChange}
                  className="custom-input"
                  required
                />
              </div>
            </div>

            <div className="form-grid-2" style={{ marginTop: "16px" }}>
              {/* Host Listings Count */}
              <div className="form-field">
                <label className="field-label" htmlFor="calculated_host_listings_count">
                  Host Total Listings
                </label>
                <input
                  id="calculated_host_listings_count"
                  type="number"
                  min="1"
                  name="calculated_host_listings_count"
                  value={formData.calculated_host_listings_count}
                  onChange={handleChange}
                  className="custom-input"
                  required
                />
              </div>

              {/* Availability 365 Days */}
              <div className="form-field">
                <div className="range-header">
                  <label className="field-label" htmlFor="availability_365">
                    Availability (Days / Year)
                  </label>
                  <span className="range-badge">{formData.availability_365} days</span>
                </div>
                <input
                  id="availability_365"
                  type="range"
                  min="0"
                  max="365"
                  name="availability_365"
                  value={formData.availability_365}
                  onChange={handleChange}
                  className="custom-range"
                />
                <div className="range-labels">
                  <span>0d (Rarely)</span>
                  <span>180d</span>
                  <span>365d (Year-round)</span>
                </div>
              </div>
            </div>
          </div>

          {/* SUBMIT BUTTON */}
          <div className="action-area">
            <button type="submit" className="predict-submit-btn" disabled={loading}>
              {loading ? (
                <span className="btn-loading">
                  <span className="spinner"></span>
                  Calculating Model Prediction...
                </span>
              ) : (
                <span className="btn-content">
                  <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2.5">
                    <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
                  </svg>
                  Predict Nightly Airbnb Price
                </span>
              )}
            </button>
          </div>
        </form>

        {/* ERROR DISPLAY */}
        {error && (
          <div className="error-card">
            <div className="error-icon">
              <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
              </svg>
            </div>
            <div className="error-body">
              <h4>Prediction Error</h4>
              <p>{error}</p>
            </div>
          </div>
        )}

        {/* PREDICTION RESULT CARD */}
        {predictedPrice !== null && (
          <div id="prediction-result" className="result-card glow-in">
            <div className="result-header">
              <div className="result-tag">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" strokeWidth="2">
                  <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
                Model Output Ready
              </div>

              <span className="model-badge">Extra Trees Regressor</span>
            </div>

            <div className="price-main">
              <div className="price-label">Estimated Nightly Rate</div>
              <div className="price-amount">
                <span className="currency">$</span>
                <span className="amount-number">{predictedPrice.toFixed(2)}</span>
                <span className="per-night">/ night</span>
              </div>
            </div>

            {/* Price Tier Badge */}
            {(() => {
              const tier = getPriceTier(predictedPrice);
              return (
                <div className="tier-bar">
                  <span className={`tier-pill ${tier.badge}`} style={{ color: tier.color, borderColor: tier.color }}>
                    {tier.label} ({tier.range})
                  </span>
                </div>
              );
            })()}

            {/* Listing Summary Table */}
            <div className="summary-grid">
              <div className="summary-item">
                <span className="summary-label">Borough</span>
                <span className="summary-val">{formData.neighbourhood_group}</span>
              </div>
              <div className="summary-item">
                <span className="summary-label">Neighbourhood</span>
                <span className="summary-val">{formData.neighbourhood}</span>
              </div>
              <div className="summary-item">
                <span className="summary-label">Room Type</span>
                <span className="summary-val">{formData.room_type}</span>
              </div>
              <div className="summary-item">
                <span className="summary-label">Min Stay</span>
                <span className="summary-val">{formData.minimum_nights} nights</span>
              </div>
            </div>

            {/* Model Scoping & Error Metrics Context */}
            <div className="model-metrics-box">
              <h5 className="metrics-title">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                  <polyline points="14 2 14 8 20 8"></polyline>
                  <line x1="16" y1="13" x2="8" y2="13"></line>
                  <line x1="16" y1="17" x2="8" y2="17"></line>
                </svg>
                Model Performance & Scope Context
              </h5>
              <div className="metrics-pills">
                <div className="metric-chip">
                  <span className="m-label">MAE</span>
                  <span className="m-val">$38.55</span>
                </div>
                <div className="metric-chip">
                  <span className="m-label">RMSE</span>
                  <span className="m-val">$61.63</span>
                </div>
                <div className="metric-chip">
                  <span className="m-label">R² Score</span>
                  <span className="m-val">0.508 (50.8%)</span>
                </div>
                <div className="metric-chip">
                  <span className="m-label">Scope</span>
                  <span className="m-val">$10 – $500 / night</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Footer */}
        <footer className="app-footer">
          <p>
            NYC Airbnb Price Prediction Model • Project Scoped to Listings ≤ $500/night
          </p>
        </footer>
      </div>
    </div>
  );
}

export default App;