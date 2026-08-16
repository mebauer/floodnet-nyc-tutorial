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
The ultimate goal of this project is to promote these datasets for academic research and to assist communities in analyzing and downloading the data. The FloodNet NYC program is one of my favorite programs in New York City, and I hope you find these tutorials helpful in advancing the study and analysis of flood risk.

# 2. Notebooks
- [00-download-data.ipynb](https://github.com/mebauer/floodnet-nyc-tutorial/blob/main/00-download-data.ipynb): How to download the FloodNet NYC data from NYC Open Data.
- [01-load-inspect.ipynb](https://github.com/mebauer/floodnet-nyc-tutorial/blob/main/01-load-inspect.ipynb): Demonstrates how to inspect both the Sensor Metadata and Flood Events datasets.
- [02-sensor-rankings.ipynb](https://github.com/mebauer/floodnet-nyc-tutorial/blob/main/02-sensor-rankings.ipynb): Ranks sensors and flood events by various statistics (e.g., max flood depth).
- [03-flood-profiles.ipynb](https://github.com/mebauer/floodnet-nyc-tutorial/blob/main/03-flood-profiles.ipynb): Teaches how to generate and produce flood profiles and other hydrograph statistics (e.g., rising limb, recession time, etc.).

# 3. Data 
- Street Flooding Events Measured by FloodNet Sensors. Retrieved from https://data.cityofnewyork.us/Environment/FloodNet-Street-Flooding-Events-Measured-by-FloodN/aq7i-eu5q/about_data
- Sensor Deployment Metadata. Retrieved from https://data.cityofnewyork.us/Environment/FloodNet-Sensor-Deployment-Metadata/kb2e-tjy3/about_data)

# 4. Additional Resources
## Academic Research:
- Mydlarz, C., Sai Venkat Challagonda, P., Steers, B., Rucker, J., Brain, T., Branco, B., et al. (2024). FloodNet: Low-cost ultrasonic sensors for real-time measurement of hyperlocal, street-level floods in New York City. Water Resources Research, 60, e2023WR036806. https://doi.org/10.1029/2023WR036806

# 5. Say Hello!
Feel free to reach out.
- LinkedIn: [markebauer](https://www.linkedin.com/in/markebauer/)   
- Portfolio: [mebauer.github.io](https://mebauer.github.io/)
- GitHub: [mebauer](https://github.com/mebauer) 

