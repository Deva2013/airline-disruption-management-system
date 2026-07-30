# AI-Powered Airline Disruption Detection & Recovery System

An independent, faculty-mentored research project applying real public aviation data to build a two-phase system for detecting, predicting, and responding to airline flight disruptions.

**Status:** 🚧 In progress (Phase 1) — started June 2026

## Overview

Most academic and industry work on airline disruption management relies on synthetic or simulated data. This project uses only real, publicly available datasets to build an end-to-end pipeline — from raw flight/weather data to a predictive model and (in Phase 2) an AI-driven passenger communication workflow.

## Architecture

![System Architecture](architecture.png)

**Phase 1 — Detect, Monitor & Predict** (in progress)
- Ingests BTS On-Time Performance data, FAA OPSNET, NOAA METAR weather data, and OpenSky flight-tracking data
- Classifies delay type and severity, flags impacted downstream flights
- Real-time operations dashboard (Plotly)
- Predictive delay model (XGBoost / LightGBM)

**Phase 2 — Respond, Rebook & Retain** (planned)
- LLM-powered decision agent for passenger triage and rebooking
- Automated, personalized delay communications
- Customer-facing dashboard with predicted recovery time

## Data Sources
- [BTS On-Time Performance Data](https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FGJ)
- [NOAA Aviation Weather Center METAR API](https://aviationweather.gov/data/api/)
- [OpenSky Network](https://opensky-network.org/data)
- [FAA OPSNET](https://aspm.faa.gov/opsnet/sys/Main.asp)

## Tech Stack
Python, Pandas, XGBoost, LightGBM, Plotly, fastparquet, Google Colab

## Current Dataset
10.5M+ flight records, Jan 2022 – Dec 2024, across 10 major US hub airports

## Mentorship
This project is being developed under the mentorship of a faculty advisor at the W. P. Carey School of Business, Arizona State University.

## Author
Devajith Indrajith Subramoniam — [LinkedIn](https://linkedin.com/in/devajithindrajith) | [Tableau Public](https://public.tableau.com/app/profile/devajith.indrajith.subramoniam)
