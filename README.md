### Globalis: Real-Time Radar for Public Pressure

## Overview
If surveys were invented today — they wouldn’t ask. They’d detect.
The world speaks. Globalis listens — before anyone else can.

No panels. No spin. Just the truth — direct from society, unfiltered and in real time.
Globalis is an AI-powered early-warning system that quantifies the pressure(relevance) building in society. It detects when public attention spikes, emotions intensify, and that combination breaks from the norm — before unrest erupts. We turn raw signals into the GIS (Globalis Intelligence Score) — a real-time score from 0 to 100. Below 50? Risk is rising, often days before headlines hit.

This isn’t mood tracking. It’s pressure (relevance) detection — for policy, crisis ops, and anyone who can’t afford to be late.

## Goal
Globalis aims to make collective pressure(relevance) transparent and actionable, replacing laggy surveys with dynamic, behavior-driven insights for fair policy, crisis response, and societal understanding.

## Vision
Fair. Transparent. Universal.

The GIS enables decision-makers to detect what truly moves people — not just what’s loud. Global topics like climate change, migration, or inflation aren’t just media-covered; they’re quantified as real-time pressure(relevance) signals.
GIS is the first step toward an AI-Governance Terminal for our time: Imagine watching a topic plunge into volatility — before the headlines hit.


## PIPELINE – How GIS Works

# DATA INPUT 

(real time social media posts)

# TOPIC DETECTION

classify posts (e.g. Inflation, Migration)

# OPINION DETECTION

check if post is opinion based

# SENTIMENT DETECTION 

 Measures emotional intensity (positive/negative -> pro/contra).

# Relevance (this is how WE define relevance)
We detect when three forces collide:

It gets loud (attention spikes).
It gets charged (emotion intensifies).
It gets abnormal (breaks from historical baselines). 

That’s when GIS moves — signaling rising relevance.

Storage & Historization
Weekly snapshots stored to track shifts over time — no guesswork, just patterns.
Explanation & Prediction
GIS compares developments (e.g. "Volatility rising on inflation — confidence crumbles"). Automatically generates insights like "Inflation panic surges — GIS at 32.9 signals high negative shift."
Visualization
Streamlit dashboard with:

Topic filters and interactive charts.
Color alerts (red for drops below 50).
CSV exports timestamped for audits.

Visualization Vision

Heatmaps per region: GIS + contrast on world maps (Plotly choropleth).
Stance pies: Pro/contra/neutral per topic, layered with sentiment.
Delta bars: Week-over-week changes (↑↓ arrows for pressure(relevance) shifts).
Topic explorer: Drill-down on GIS evolution.
Explain layer: Mini-insights under charts (e.g. "Energy costs through the roof — moderate positive shift").
Comparisons: Inflation DE vs. US.
Alerts: 🔴 for GIS panic levels.

# Usage
Console: Run python main.py [db/json/csv] to compute moods and GIS.
Web: Start streamlit run app.py for interactive radar with filters, charts, and contrasts.
Project Structure
main.py: Entry point for GIS calculation and runs.

app.py: Streamlit dashboard for visualization.

data_loader.py: Loads from DB, JSON, or CSV.

gsi_db_setup.py: Sets up and populates SQLite DB.

.env: API keys and secrets (gitignored).

requirements.txt: All Python deps.

README.md: This guide.

docs/: Docs and notes.

models/: Analyzer modules for sentiment, opinion, topic.

utils/: Core pipeline, helpers, explainers.

data/: Raw DB/JSON storage.

venv/: Virtual env (gitignored).
Further Notes
.env: Store sensitive API keys here – never commit to repo.

requirements.txt: Update with pip freeze > requirements.txt after installs.

venv/: Isolated env – ignore in Git.