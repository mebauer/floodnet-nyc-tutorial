# Methods and data caveats

How the notebooks define their terms and choose their parameters, and the
caveats every FloodNet analysis here is checked against. If you build your own
analysis on this data, the caveats apply there too.

Most of the caveats below come from FloodNet's own
[data description](data/Floodnet_Open_Data_-_Data_Description_03.05.2026.pdf),
attached to the dataset on NYC Open Data and saved in `data/`. Read it before
drawing conclusions from the data.

## Approach
These tutorials aim to teach good practice, not to show off technique.
- **The method can come from anywhere; the parameters cannot.** A purely
  statistical method is fine, but it must not contradict how flooding
  physically works or what these sensors can observe. Every threshold, grouping
  rule or derived metric is a hydrological claim, so each one traces back to an
  established convention or a physical fact about the sensors, and the notebook
  says which. When a parameter has no such basis, the notebook says so
  plainly. A threshold isn't kept just because it is clever or because the
  results look good.
- **Judgment calls are named as such.** Where no convention exists, the
  notebook states the choice and its basis, and checks whether the conclusions
  survive a different choice.
- **Numbers come from code.** The data are refreshed about every two weeks, so
  counts, percentages and rankings are computed and printed in the notebooks,
  never written into the text.

## Definitions and parameters

| Term | Rule | Basis | Where |
|---|---|---|---|
| Event | A run of depth readings > 10 mm, verified as a flood by FloodNet QC | FloodNet's definition; one row in the Flood Events dataset | dataset |
| Flood | Event with peak depth ≥ 4 in at the sensor | NYC Stormwater Flood Maps "nuisance" tier (4 in to < 1 ft); matches `duration_above_4_inches_mins` | notebooks 02, 05–07 |
| Major flood | Event with peak depth ≥ 12 in at the sensor | Flood Maps "deep and contiguous" tier (≥ 1 ft); matches `duration_above_12_inches_mins` | notebooks 05–07 |
| Rain episode | **Exploratory grouping, not a definition of an event.** Non-tidal events grouped across the whole network: a new episode starts when an event begins more than 6 h after the latest end time of all earlier events | The 6 h default borrows the minimum interevent time used to separate rainstorms (e.g. Driscoll et al. 1989), adapted to flood timing. Results are worth checking at other gaps. See caveat 4 | `floodnet.build_rain_episodes`; notebook 06 checks episode counts across gaps |
| Deployment (exposure) | Days from install to removal or to the data cutoff, whichever comes first | Sensor metadata; assumes continuous operation (caveat 6) | `floodnet.days_deployed` |
| Data cutoff | End of the latest event in the dataset, not the download date | Keeps rates stable across re-runs. See caveat 8 | notebook 02 |
| Active sensor-month | Sensor installed on or before the month's last day and not removed before its first | Sensor metadata | notebook 05 |
| Minimum record | Only sensors deployed ≥ 180 days are ranked by rate | **Judgment call:** keeps one early flood from producing an extreme rate. Not hydrological; doesn't guarantee a full seasonal cycle | notebook 02 |
| Storm plot floor | `storm_events` / `plot_storm_events` drop events with peak ≤ 2 in | **No grounded basis yet;** a display filter only | `floodnet.storm_events` |

Flood and major flood are nested, not exclusive: every major flood is also a
flood. For mutually exclusive bins, use < 4 in, 4 to < 12 in, and ≥ 12 in.

## FloodNet data caveats

### What the sensors can see
1. **Depth is measured at the sensor, not at the lowest point.** Sensors
   hang from existing street infrastructure such as sign posts, so they usually
   sit above the lowest nearby point, where water collects first. The offset
   is in `lowest_point_height_delta_inches`. FloodNet's example: a sensor 4 in
   above the local low point misses floods shallower than 4 in, and a 10 in
   reading means about 14 in at the low point. Most sensors are also mounted
   over sidewalks, so they don't register water in the roadway until it tops
   the curb. Two consequences:
   - The flood and major-flood tiers apply to depth at the sensor, which is a
     lower bound on the deepest water nearby. The Flood Maps tiers classify
     modeled flood areas; applying them at one sensor is an adaptation.
   - Comparing raw depths across sensors partly compares mounting height.
     Notebooks that rank or compare depths across sensors say so.
2. **Peaks can be spurious, and snow interferes.** Objects under a sensor
   (people, vehicles, trash) can leave anomalous readings. A single bad point
   can inflate `max_depth_inches` and distort `onset_time_mins` and
   `drain_time_mins`. Snow piled under a sensor can produce false readings or
   hide a flood shallower than the pile. Rankings by maximum depth and winter
   results deserve the most scrutiny. Before November 2021 some sensors
   sampled every 5 minutes instead of every minute, so early onset and drain
   times are coarser.

### What the observations mean
3. **Split tidal vs. non-tidal.** `tidally_influenced` (sensor metadata) marks
   two distinct flooding regimes. Analyze them separately or facet/color by the
   flag. A table or statistic that pools both groups is acceptable only when
   it is followed by the same view broken out by the flag. Tidal sensors flood
   with high tides, roughly twice a day, so a few coastal sites can dominate
   any pooled count. The flag is per sensor, not per event: a tidal sensor can
   still record rain-driven floods. Rain-based rules such as the episode
   grouping apply to non-tidal sensors only.
4. **Surface observations only.** These data contain no rainfall or drainage
   records. Conclusions stay at the surface hydrology the sensors observe:
   don't attribute floods to sewer capacity or storm intensity.
   `drain_time_mins` is recession at the sensor, not sewer performance. Rain
   episodes are an exploratory way to group events, inferred from flood timing,
   not confirmed rain events. The event itself is FloodNet's definition; the
   episode is ours, and a different gap would give different episodes. The
   6 h rule is also applied differently from its origin:
   - In rainfall analysis it is a dry gap in one gauge's record. Here it is a
     gap between flood events anywhere in the non-tidal network. A gap between
     floods is not a dry period: it is shortened by the time water takes to
     drain and lengthened by the time it takes to rise.
   - Because it is network-wide, the rule depends on network size. With more
     sensors deployed, it is more likely that some sensor is flooded within any
     6 h window, so later episodes may chain together and run longer than early
     ones. Compare episode counts or durations across years with this in mind.

   For rainfall, FloodNet recommends NYS Mesonet / NYC Micronet 5-minute
   station data; for tides, NOAA and USGS tide gauges.
5. **Observations ≠ vulnerability.** High depth or frequency at a sensor reflects
   where rain fell, where the sensor could be mounted (caveat 1) and how the
   site was chosen. Sites are not a random sample of the city: FloodNet installs
   sensors at known flood-prone locations (see Mydlarz et al. 2024 and Ceferino
   et al. 2023 for how sites are selected). Describe rankings as "observed at this sensor".
   Don't generalize them to neighborhoods or boroughs or treat them as a
   ranking of vulnerability, which also depends on exposure and the capacity to
   cope. Even comparing how prone sites are to flooding requires conditioning on
   rainfall.

### Coverage over time
6. **No events ≠ no flooding.** The dataset has no sensor uptime record. A
   sensor misses floods while offline awaiting repair, when weak connectivity
   leaves too few readings to confirm an event, or under snow. Many deployed
   sensors have recorded no events at all. Exposure calculations assume
   continuous operation, which makes them an upper bound on time actually
   observed; say so.
7. **Normalize for staggered deployment.** The first sensor was installed in
   October 2020; the network has grown since and some sensors were removed.
   Raw counts by year or month therefore track network growth as much as
   flooding. For any time comparison, use exposure (events per sensor-year) or
   a fixed cohort active for the whole period. Check the install-date
   distribution first, and flag partial years and years whose sensor count is
   thin relative to the rest.
8. **Recent weeks are incomplete.** Events are published only after QC, and
   each biweekly refresh adds older events that only just cleared review
   (notebook 04 calls them late arrivals). The record runs only to the data
   cutoff, and the weeks just before it are likely undercounted. Don't read a
   drop in the latest weeks as a drop in flooding.
9. **A sensor is not a site.** When a sensor is replaced at the same location
   it gets a new `sensor_id`, and the replacement's metadata (including
   `tidally_influenced`) can differ from the original's. Per-sensor results
   split such a site's record across ids; `sensor_name` identifies the
   location. Say whether a result is per sensor or per site.

### Which events count
10. **Not every event is a flood.** An event starts at > 10 mm, so many events
    are shallow, and the shallow share differs between tidal and non-tidal
    sensors. Raw event counts can skew frequency results. Whether to filter to
    floods (≥ 4 in) depends on the question, so decide deliberately and state
    which definition a count uses. `duration_above_24_inches_mins` also exists
    but is not used as a tier.

### Mapping flood extent
11. **A sensor measures a point, not an area.** Turning sensor depths into a
    flood extent, whether by projecting a sensor's water level across a DEM
    ("bathtub" mapping) or by interpolating depths between sensors, probably
    isn't best practice for street flooding. For rain-driven flooding the water
    surface is rarely level beyond the local low spot: water pools in separate
    dips and flows along streets, and curbs, buildings and storm drains shape
    where it goes, none of which a single reading captures. DEM vertical error
    can be similar in size to the depths involved, the depth at the sensor
    understates the low point (caveat 1), and sensors peak at different times.
    Modeled products such as the NYC Stormwater Flood Maps are a better starting
    point for extent, with sensor depths as point checks against them. For tidal
    flooding, a level water surface limited to land connected to the shoreline
    is a common first approximation. Any mapped extent is an estimate, not an
    observation, and is worth labeling that way.

## Time zones
Flood start and end times are published in UTC (the data dictionary labels them
GMT), with no offset in the values. The notebooks keep these UTC columns and add
New York local-time copies with an `_et` suffix (`America/New_York`, which
handles daylight saving) using `floodnet.to_local_time()`. Anything read off a
calendar or clock (hour of day, date, month, year) uses the `_et` columns, and
times shown in tables and plots are labeled ET. Durations are the same in either
zone. Sensor install and removal dates are calendar dates and are not converted.

## References
- FloodNet. *FloodNet NYC – Data Description* (March 2026). Attached to the
  NYC Open Data datasets; copy in
  [`data/`](data/Floodnet_Open_Data_-_Data_Description_03.05.2026.pdf).
- Mydlarz, C., et al. (2024). FloodNet: Low-cost ultrasonic sensors for
  real-time measurement of hyperlocal, street-level floods in New York City.
  *Water Resources Research*, 60, e2023WR036806.
  <https://doi.org/10.1029/2023WR036806>
- Ceferino, L., et al. (2023). *Developing a Framework to Optimize FloodNet
  Sensor Deployments around NYC for Equitable and Impact-Based Hyper-Local
  Street-Level Flood Monitoring and Data Collection.*
  <https://rosap.ntl.bts.gov/view/dot/68526>
- NYC Mayor's Office of Climate & Environmental Justice / DEP (2021).
  *Stormwater Resiliency Plan* (methodology for the Stormwater Flood Maps
  depth tiers). <https://www.nyc.gov/assets/orr/pdf/publications/stormwater-resiliency-plan.pdf>
- NYC Stormwater Flood Maps. <https://www.nyc.gov/stormwater-map>
- Driscoll, E. D., Palhegyi, G. E., Strecker, E. W., & Shelley, P. E. (1989).
  *Analysis of Storm Event Characteristics for Selected Rainfall Gauges
  Throughout the United States.* U.S. EPA. (Source of the 6 h minimum
  interevent time convention.)

**Citing the data.** FloodNet asks that publications list the project as
"FloodNet (New York University and The City University of New York)" and cite
Mydlarz et al. (2024).
