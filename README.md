# AI-Powered Airline Disruption Detection & Recovery System

An independent, faculty-mentored research project applying real public aviation data to build a two-phase system for detecting, predicting, and responding to airline flight disruptions.

**Status:** 🚧 In progress (Phase 1) — started June 2026

## Overview

Most academic and industry work on airline disruption management relies on synthetic or simulated data. This project uses only real, publicly available datasets to build an end-to-end pipeline — from raw flight/weather data to a predictive model and (in Phase 2) an AI-driven passenger communication workflow.

## Architecture

![System Architecture](Project_workflow_architecture_updated.jpg)

**Phase 1 — Detect, Monitor & Predict** (in progress)
- Ingests BTS On-Time Performance data (implemented) and historical METAR weather data via the Iowa Environmental Mesonet ASOS archive (in progress)
- Classifies delay type and severity, flags impacted downstream flights
- Real-time operations dashboard (Plotly)
- Predictive delay model (XGBoost / LightGBM)
- OpenSky flight-tracking data and FAA OPSNET airport-capacity/ground-stop data are planned enrichments — see [Data Sources](#data-sources) for current status of each

**Phase 2 — Respond, Rebook & Retain** (planned)
- LLM-powered decision agent for passenger triage and rebooking
- Automated, personalized delay communications
- Customer-facing dashboard with predicted recovery time

## Data Sources

| Source | Status | Notes |
|---|---|---|
| [BTS On-Time Performance Data](https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FGJ) | ✅ Implemented | 10.5M+ flight records cleaned and loaded via direct PREZIP download |
| [Iowa Environmental Mesonet — ASOS/METAR Archive](https://mesonet.agron.iastate.edu/request/download.phtml) | ⚠️ In progress | Replaces the NOAA Aviation Weather Data API, which only serves ~15 days of live METAR observations and cannot return historical data back to 2022. IEM provides true historical depth (2022+), CSV output, no login required |
| [OpenSky Network](https://opensky-network.org/data) | 🔲 Planned | Live flight-position enrichment, not yet integrated |
| [FAA OPSNET / ASPM](https://www.aspm.faa.gov/opsnet/sys/Main.asp) | 🔲 Planned | No public API — data is exported manually per airport/date range via the OPSNET web reporting tool as daily, facility-level delay-by-cause figures, then joined in as a daily airport-level feature (not a per-flight join) |

## Tech Stack
Python, Pandas, XGBoost, LightGBM, Plotly, fastparquet, Google Colab

## Current Dataset
10.5M+ flight records, Jan 2022 – Dec 2024, across 10 major US hub airports

## Mentorship
This project is being developed under the mentorship of a faculty advisor at the W. P. Carey School of Business, Arizona State University.

## Author
Devajith Indrajith Subramoniam — [LinkedIn](https://linkedin.com/in/devajithindrajith) | [Tableau Public](https://public.tableau.com/app/profile/devajith.indrajith.subramoniam)
