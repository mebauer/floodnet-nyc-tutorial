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

# 2. Tutorials
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

# 5. NYC Engineering Reference Library

Official NYC resources for understanding stormwater runoff, sewer hydraulics, drainage infrastructure and modeled flood risk.

1. [NYC DEP — 2021 Stormwater Resiliency Plan](https://www.nyc.gov/assets/orr/pdf/publications/stormwater-resiliency-plan.pdf) — Methodology behind NYC's Stormwater Flood Maps, including coupled 1D–2D hydraulic modeling and design-storm scenarios.

2. [NYC DEP — 2024 Stormwater Analysis](https://www.nyc.gov/assets/dep/downloads/pdf/water/stormwater/2024-stormwater-analysis-report.pdf) — Citywide hydraulic modeling, 86 priority drainage areas and neighborhood flood-risk assessments.

3. [NYC Stormwater Flood Maps](https://www.nyc.gov/stormwater-map) — Modeled rainfall-driven flood extents and depths for comparison with FloodNet observations under appropriate conditions.

4. [NYC DEP — InfoWorks Citywide Recalibration Report](https://www.nyc.gov/assets/dep/downloads/pdf/water/nyc-waterways/citywide-ltcp/infoworks-citywide-recalibration-report.pdf) — Technical documentation of NYC's sewer-system modeling, including subcatchments, runoff and hydraulic calibration.

5. [NYC Stormwater Manual](https://www.nyc.gov/assets/dep/downloads/pdf/water/stormwater/unified-stormwater-rule/uswr_nyc_stormwater_manual.pdf) — Design criteria and sizing methods for stormwater retention, detention and green infrastructure.

6. [NYC DEP Sewer Design Standards (2025)](https://www.nyc.gov/assets/ddc/downloads/publications/NYCDEPSEWERDESIGNSTANDARDS_RevisedSep2025.pdf) — Standard engineering drawings and details for sewers, manholes, catch basins and related infrastructure.

7. [NYC Stormwater Management Program Plan (MS4)](https://www.nyc.gov/site/dep/water/municipal-separate-storm-sewer-system.page) — NYC's separate storm sewer program, drainage mapping and stormwater management requirements.

8. [DEP Standard Sewer and Water Main Specifications (2022)](https://www.nyc.gov/assets/ddc/downloads/publications/scops/NYCDEPStandard%20Sewer_WaterSpecifications_2022-08-08.pdf) — Construction specifications for sewer and water-main materials, installation and associated infrastructure.

# 6. Applied Case Studies

NYC engineering studies and academic research illustrating how hydrology, hydraulics and drainage infrastructure influence urban flooding.

## NYC Case Studies

- [FiDi & Seaport Master Plan — Stormwater Management Studies (NYC EDC, 2024)](https://edc.nyc/sites/default/files/2024-03/FiDi-Master-Plan-Stormwater-Management-Studies.pdf) — Refinement of an existing sewer model into a higher-resolution 1D–2D model of flooding in Lower Manhattan.

- [NYC DEP — 2024 Stormwater Analysis](https://www.nyc.gov/assets/dep/downloads/pdf/water/stormwater/2024-stormwater-analysis-report.pdf) — Drainage assessments and potential interventions for Dyker Heights, Knickerbocker, Kissena Park and Jewel Streets.

- [Flushing Bay Long Term Control Plan](https://www.nyc.gov/assets/dep/downloads/pdf/water/nyc-waterways/flushing-bay/ltcp-flushing-bay-cso.pdf) — Sewer-system modeling, subcatchment delineation, imperviousness and runoff characterization.

- [Newtown Creek Long Term Control Plan](https://www.nyc.gov/assets/dep/downloads/pdf/water/nyc-waterways/newtown-creek/ltcp-newtown-creek-cso.pdf) — Combined-sewer modeling, including regulators, interceptors, outfalls and storage alternatives.

- [NYC Cloudburst Resiliency Planning Study](https://www.nyc.gov/assets/dep/downloads/pdf/climate-resiliency/nyc-cloudburst-study.pdf) — Extreme-rainfall flooding, overland flow and surface-storage strategies in Southeast Queens.

## Academic Case Studies

- [Tallman Island Sewershed Study (2026)](https://www.sciencedirect.com/science/article/pii/S221458182600162X) — SWMM-based analysis of sewer-network performance, hydraulic constraints and flooding in NYC.

- [Pluvial and Potential Compound Flooding During Hurricane Ida (HESS, 2025)](https://hess.copernicus.org/articles/29/2043/2025/) — Coupled coastal and rainfall-driven flood modeling in NYC, evaluated using high-water marks and additional FloodNet observations.

- [Compounding Effects of Changing Sea Level and Rainfall Regimes on Pluvial Flooding in NYC (Natural Hazards, 2024)](https://link.springer.com/article/10.1007/s11069-024-06466-8) — Modeling the combined effects of extreme rainfall and elevated coastal water levels on urban flooding.

# 7. National Engineering References

Federal engineering manuals, modeling documentation and precipitation data for urban stormwater analysis and drainage design.

1. [EPA Storm Water Management Model (SWMM)](https://www.epa.gov/water-research/storm-water-management-model-swmm) — Official software and documentation for urban runoff and drainage-network modeling.

2. [EPA SWMM Fact Sheet](https://www.epa.gov/sites/default/files/2016-09/documents/swmm_factsheet_final_16sep01-508_compliant.pdf) — Brief overview of SWMM's capabilities and engineering applications.

3. [SWMM 5.2 User's Manual](https://www.epa.gov/system/files/documents/2022-04/swmm-users-manual-version-5.2.pdf) — Practical guide to building, running and interpreting SWMM models.

4. [SWMM Reference Manual, Volume I — Hydrology (2016)](https://nepis.epa.gov/Exe/ZyPDF.cgi/P100NYRA.PDF?Dockey=P100NYRA.PDF) — Mathematical foundations of rainfall–runoff modeling, infiltration and subcatchment routing.

5. [SWMM Reference Manual, Volume II — Hydraulics (2017)](https://nepis.epa.gov/Exe/ZyPDF.cgi/P100S9AS.PDF?Dockey=P100S9AS.PDF) — Hydraulic methods for pipe flow, dynamic-wave routing, backwater, surcharge and flooding.

6. [FHWA HEC-22: Urban Drainage Design, Fourth Edition (2024)](https://www.fhwa.dot.gov/engineering/hydraulics/pubs/hif24006.pdf) — Engineering methods for runoff estimation, gutter hydraulics, inlet interception and storm-drain design.

7. [NOAA Atlas 14](https://hdsc.nws.noaa.gov/pfds/) — Location-specific precipitation-frequency estimates for rainfall analysis and design-storm development.

# 8. Related Projects

- [mebauer/nyc-flood-data](https://github.com/mebauer/nyc-flood-data) — Reproducible inventory of NYC flood-related datasets.

# 9. Say Hello!

Feel free to reach out.

- [LinkedIn](https://www.linkedin.com/in/markebauer/)
- [Portfolio](https://mebauer.github.io/)
- [GitHub](https://github.com/mebauer)