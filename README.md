# FloodNet NYC Tutorials
Author: Mark Bauer

### Disclaimer
This analysis uses the FloodNet NYC datasets on NYC Open Data, but is not endorsed by The City of New York. The City of New York cannot vouch for the data or analyses derived from these data after the data have been retrieved from NYC Open Data or related websites.

--------------- 

# FloodNet NYC Data
FloodNet NYC consists of two datasets, both can be found on [NYC Open Data](https://data.cityofnewyork.us/browse?Data-Collection_Data-Collection=FloodNet+NYC&sortBy=relevance&page=1&pageSize=20):
- [Street Flooding Events Measured by FloodNet Sensors](https://data.cityofnewyork.us/Environment/FloodNet-Street-Flooding-Events-Measured-by-FloodN/aq7i-eu5q/about_data): Data presented here were collected by the FloodNet project, which is a collaboration between researchers at academic institutions (New York University and the City University of New York) and NYC government agencies (NYC Department of Environmental Protection, Mayor's Office of Climate & Environmental Justice, Office of Technology & Innovation), working with NYC residents. Data on flood water depth were collected by FloodNet sensors in one minute intervals, then analyzed to develop the flood event summary statistics presented here. A flood event is defined as a series of water depth measurements greater than 10 mm; all measured flood events presented here have undergone QC by a member of the FloodNet team.

- [Sensor Deployment Metadata](https://data.cityofnewyork.us/Environment/FloodNet-Sensor-Deployment-Metadata/kb2e-tjy3/about_data): This data consists of metadata for each FloodNet sensor including its location. This data can be used to associate FloodNet sensor metadata with Flood Events in the ""FloodNet: Street Flooding Events Measured by FloodNet Sensors"" dataset. The ""Sensor ID"" column in each dataset should be used to make the association.

From NYC Open Data:
>See attached data description document for more details on data collection, analysis & the publication to cite if using the data or including it in any publication or public presentation.
>
>More information on the FloodNet project can be found here: https://www.floodnet.nyc
>
>Visualization of the data in an online data dashboard can be found here: https://dataviz.floodnet.nyc

# 1. Introduction
FloodNet NYC is a network of low-cost sensors that measure hyperlocal, street-level flooding across New York City in near real time. These tutorials walk through downloading, inspecting, and analyzing the two FloodNet datasets published on NYC Open Data, from a first look at the raw data through sensor rankings and detailed flood-event profiles. They are intended for researchers, students, and community members interested in studying and downloading local flood data.

### Goals
The ultimate goal of this project is to promote these datasets for anyone interested in analyzing and downloading the data. The FloodNet NYC program is one of my favorite programs in New York City, and I hope you find these tutorials helpful in advancing the study and analysis of flood risk.

# 2. Notebooks
- [00-download-data.ipynb](https://github.com/mebauer/floodnet-nyc-tutorial/blob/main/00-download-data.ipynb): How to download the FloodNet NYC data from NYC Open Data.
- [01-load-inspect.ipynb](https://github.com/mebauer/floodnet-nyc-tutorial/blob/main/01-load-inspect.ipynb): Demonstrates how to inspect both the Sensor Metadata and Flood Events datasets.
- [02-sensor-rankings.ipynb](https://github.com/mebauer/floodnet-nyc-tutorial/blob/main/02-sensor-rankings.ipynb): Ranks sensors and flood events by various statistics (e.g., max flood depth).
- [03-flood-profiles.ipynb](https://github.com/mebauer/floodnet-nyc-tutorial/blob/main/03-flood-profiles.ipynb): Teaches how to generate flood profiles and other hydrograph statistics (e.g., rising limb, recession time, etc.).

# 3. Data 
- Street Flooding Events Measured by FloodNet Sensors. Retrieved from https://data.cityofnewyork.us/Environment/FloodNet-Street-Flooding-Events-Measured-by-FloodN/aq7i-eu5q/about_data
- Sensor Deployment Metadata. Retrieved from https://data.cityofnewyork.us/Environment/FloodNet-Sensor-Deployment-Metadata/kb2e-tjy3/about_data

# 4. FloodNet Resources

Start here to understand the FloodNet sensor network, datasets, methodology, quality control, and applications of hyperlocal street-flood measurements in New York City.

## Foundational Research

* [Mydlarz et al. (2024) — *FloodNet: Low-Cost Ultrasonic Sensors for Real-Time Measurement of Hyperlocal, Street-Level Floods in New York City*](https://doi.org/10.1029/2023WR036806): The primary technical paper describing FloodNet's low-cost sensor system, deployment, data collection, and measurement of hyperlocal street flooding across New York City.

* [Silverman et al. (2022) — *Making Waves: Uses of Real-Time, Hyperlocal Flood Sensor Data for Emergency Management, Resiliency Planning, and Flood Impact Mitigation*](https://doi.org/10.1016/j.watres.2022.118648): Foundational paper examining how hyperlocal flood measurements can support emergency management, resilience planning, research, and flood-impact mitigation.

## FloodNet Project & Methodology

* [FloodNet NYC](https://www.floodnet.nyc): The project's main website and central starting point for information about the FloodNet NYC program.

* [FloodNet Data Dashboard](https://dataviz.floodnet.nyc): Interactive dashboard for viewing and exploring real-time and historical measurements from FloodNet sensors across New York City.

* [FloodNet NYC — Sensors & Data / Methodology](https://www.floodnet.nyc/methodology): Background on FloodNet sensor hardware, deployment, data collection, and the quality-control processes behind the published datasets.

* [FloodNet NYC — Flood Event Summaries](https://www.floodnet.nyc/flood-event-summaries): Describes FloodNet flood-event summary statistics and provides visualizations for selected measured flood events.

* [FloodNet Documentation](https://floodnet-nyc.github.io/): Technical documentation covering the sensor network, real-time data pipeline, quality assurance, and quality control.

* [Science and Resilience Institute at Jamaica Bay (SRIJB) — FloodNet NYC](https://srijb.org/floodnet-nyc/): Institutional and community-engagement context for FloodNet NYC, including the FloodNet Community Engagement Network Map.

# 5. NYC Stormwater and Urban Drainage Resources
The NYC resources below are the ones worth knowing if you want to become very good at interpreting FloodNet data — that is, explaining *why* a given sensor flooded, not just *that* it did. They cover the full chain from rainfall to runoff to terrain to sewer hydraulics to physical infrastructure.

1. [NYC DEP — 2021 Stormwater Resiliency Plan](https://www.nyc.gov/assets/orr/pdf/publications/stormwater-resiliency-plan.pdf) — The document that produced the Stormwater Flood Maps. Appendix B is the methodology: the 13 InfoWorks ICM sewershed models built on the calibrated LTCP base models, the 1D–2D coupling, the composite rain-on-mesh approach, and the two design storms (~2"/hr + 2.5 ft sea-level rise; ~3.5"/hr + 4.8 ft SLR). Read this to understand what the modeled flood surface actually represents before comparing it to sensor data.

2. [NYC DEP — 2024 Stormwater Analysis](https://www.nyc.gov/assets/dep/downloads/pdf/water/stormwater/2024-stormwater-analysis-report.pdf) — The current-diagnosis companion to the 2021 Plan. Announces the completed citywide hydraulic model, identifies 86 priority drainage areas, and works through neighborhood case studies (Dyker Heights, Knickerbocker, Kissena Park, Jewel Streets). It carries no map methodology or dataset — pair it with the 2021 Plan, don't substitute it.

3. [NYC Stormwater Flood Maps](https://www.nyc.gov/stormwater-map) — The modeled rainfall-driven flood surface you overlay against observed sensor depth. The single most operational item here: **modeled flooding ↔ measured FloodNet flooding** is one of the strongest research opportunities in this dataset.

4. [NYC DEP — InfoWorks Citywide Recalibration Report](https://www.nyc.gov/assets/dep/downloads/pdf/water/nyc-waterways/citywide-ltcp/infoworks-citywide-recalibration-report.pdf) — The bridge from general SWMM concepts to NYC's actual rainfall-runoff and sewer-hydraulic modeling: subcatchments, imperviousness, nodes, pipes, and system performance. The hardest layer to learn and the one that most distinguishes an expert analyst. *(2012; the companion Hydraulic Capacity Analysis lives on the same [Citywide LTCP page](https://www.nyc.gov/site/dep/water/citywide-long-term-control-plan.page), and the current operational model is the newer one described in resource #1.)*

5. [NYC Stormwater Manual](https://www.nyc.gov/assets/dep/downloads/pdf/water/stormwater/unified-stormwater-rule/uswr_nyc_stormwater_manual.pdf) — The runoff-generation layer: contributing drainage area, impervious surfaces, retention, detention, siting, and sizing. Where you go deep on catchment delineation and what happens before water ever reaches a sewer or a sensor.

6. [NYC DEP Sewer Design Standards (Sept 2025)](https://www.nyc.gov/assets/ddc/downloads/publications/NYCDEPSEWERDESIGNSTANDARDS_RevisedSep2025.pdf) — The physical-engineering layer: pipe sizing, catch basins, velocities, and manhole spacing. FloodNet tells you what happened at the street; this tells you what the underground system was designed to handle. (September 2025 revision.)

7. [NYC Cloudburst Resiliency Planning Study](https://www.nyc.gov/assets/dep/downloads/pdf/climate-resiliency/nyc-cloudburst-study.pdf) — Extreme short-duration rainfall, topography, and overland surface-flow pathways — conceptually the closest match to the pluvial flooding FloodNet is uniquely positioned to observe. Also the origin of NYC's cloudburst-management program.

8. [NYC Stormwater Management Program Plan (MS4)](https://www.nyc.gov/site/dep/water/municipal-separate-storm-sewer-system.page) — The combined-vs-separate sewer distinction, the MS4 drainage map, and the storm-sewershed inventory. Directly changes how a given sensor behaves, and clarifies the difference between a topographic contributing area and an infrastructure-defined sewershed.

# 6. Case Studies
Real NYC drainage areas, modeled and documented — worked examples of how
hydrologic, hydraulic, terrain, and infrastructure concepts get applied to
this city's actual sewersheds and storms. These are not required reading from beginning to end. Use them as worked examples after learning the canonical resources above: each emphasizes a different part of the rainfall → runoff → terrain → sewer → flooding chain.

- [Tallman Island Sewershed Study (2026)](https://www.sciencedirect.com/science/article/pii/S221458182600162X):
  **Sewer-system performance.** Couples the InfoWorks-derived NYC sewer
  network for Tallman Island with EPA SWMM/PySWMM to identify critical nodes
  and link extreme rainfall, imperviousness, hydraulic constraints, pipe
  fullness, and ponding — the closest thing to a full diagnostic chain on
  real NYC infrastructure.

- [FiDi & Seaport Master Plan — Stormwater Management Studies (NYC EDC, 2024)](https://edc.nyc/sites/default/files/2024-03/FiDi-Master-Plan-Stormwater-Management-Studies.pdf):
  **Model refinement (1D-2D).** Shows a coarse citywide LTCP model (~30,000 ft
  of pipe in the study area) expanded to ~45,000 ft with high-resolution
  catchments and a 1D-2D build to visualize flood extent and depth. A
  transferable lesson in adapting a sewershed model from water quality to
  flood-risk work — Lower Manhattan.

- [NYC DEP — 2024 Stormwater Analysis](https://www.nyc.gov/assets/dep/downloads/pdf/water/stormwater/2024-stormwater-analysis-report.pdf):
  **DEP's own diagnostic reasoning.** Revisit the four neighborhood
  case-study chapters — Dyker Heights, Knickerbocker, Kissena Park, and Jewel
  Streets — where DEP diagnoses distinct drainage problems and weighs
  gray/green fixes against its citywide hydraulic model.

- [Flushing Bay Long Term Control Plan](https://www.nyc.gov/assets/dep/downloads/pdf/water/nyc-waterways/flushing-bay/ltcp-flushing-bay-cso.pdf):
  **Subcatchments & runoff (the approachable sewershed).** The strongest
  traditional DEP example for learning subcatchments, imperviousness/DCIA,
  and InfoWorks CS representation. Focus on the watershed-characterization
  and modeling sections; skim the CSO water-quality material, which is most
  of the page count.

- [Newtown Creek Long Term Control Plan](https://www.nyc.gov/assets/dep/downloads/pdf/water/nyc-waterways/newtown-creek/ltcp-newtown-creek-cso.pdf):
  **Complex combined-sewer hydraulics (the harder system).** A large
  Brooklyn–Queens drainage area with regulators, interceptors, outfalls, and
  storage alternatives. Read right after Flushing Bay — same strategy, harder
  system.

- [Compounding effects of changing sea level and rainfall regimes on pluvial flooding in NYC (*Natural Hazards*, 2024)](https://link.springer.com/article/10.1007/s11069-024-06466-8):
  **Citywide boundary conditions.** Uses a citywide hydrologic/hydraulic
  model to investigate how rainfall intensity/duration combined with sea
  level or surge affects pluvial flooding and gravity drainage at outfalls.

- [NYC Cloudburst Resiliency Planning Study](https://www.nyc.gov/assets/dep/downloads/pdf/climate-resiliency/nyc-cloudburst-study.pdf):
  **Surface exceedance pathways.** Southeast Queens: terrain, overland flow
  paths, and surface storage for rainfall that exceeds sewer capacity — the
  flooding mode conventional sewer models handle least well.

- [Pluvial and potential compound flooding in a coupled coastal modeling framework: NYC during post-tropical Cyclone Ida (2021) (*HESS*, 2025)](https://hess.copernicus.org/articles/29/2043/2025/):
  **Observed-event reconstruction.** Reconstructs Ida across the Jamaica Bay
  watershed with the COAWST coastal model, using rain-on-grid and a single
  calibrated "drain rate" as a stand-in for the stormwater system rather than
  an explicit sewer network. Validated against surveyed high-water marks —
  plus 10 FloodNet gauges from a separate September 2023 storm used as extra
  calibration points — reaching ~20 cm RMSE. The natural bridge to the
  FloodNet-utilized papers.

# 7. Related Projects
- [mebauer/nyc-flood-data](https://github.com/mebauer/nyc-flood-data): Flood Data for NYC — a comprehensive, reproducible inventory of flood-related datasets across NYC Open Data.

# 8. Say Hello!
Feel free to reach out.
- LinkedIn: [markebauer](https://www.linkedin.com/in/markebauer/)   
- Portfolio: [mebauer.github.io](https://mebauer.github.io/)
- GitHub: [mebauer](https://github.com/mebauer)