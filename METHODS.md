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
  statistical method is fine, but its assumptions, and how its results are
  read, must fit how flooding physically works and what these sensors can
  observe. Every threshold, grouping rule or derived metric is a hydrological
  claim, so each one traces back to an established convention or a physical
  fact about the sensors, and the notebook says which. Display choices, such as
  how many sensors a chart shows, aren't parameters in this sense. When a
  parameter has no such basis, the notebook says so
  plainly. A threshold isn't kept just because it is clever or because the
  results look good.
- **Judgment calls are named as such.** Where no convention exists, the
  notebook states the choice and its basis, and checks whether the conclusions
  survive a different choice.
- **Numbers come from code.** The data are refreshed about every two weeks, so
  counts, percentages and rankings are computed and printed in the notebooks,
  never written into the text.

## Definitions and parameters

Each basis says where a rule comes from: an official source, which is cited,
or a choice made for this project, marked **Judgment call**. The notebooks
say which when they use it.

| Term | Rule | Basis | Where |
|---|---|---|---|
| Event | A run of depth readings > 10 mm, verified as a flood by FloodNet QC | FloodNet's definition; one row in the Flood Events dataset | dataset |
| Flood | Event with peak depth ≥ 4 in at the sensor | NYC Stormwater Flood Maps "nuisance" tier (4 in to < 1 ft); matches `duration_above_4_inches_mins` | notebooks 02, 05–08 |
| Severe flood | Event with peak depth ≥ 12 in at the sensor | Flood Maps "deep and contiguous" tier (≥ 1 ft); "severe" is this project's name for it. Matches `duration_above_12_inches_mins` | notebooks 02, 05–07 |
| 24 in depth | Time to 24 in and time above 24 in (`duration_above_24_inches_mins`) | FloodNet's dataset column. Not a Flood Maps tier, so it doesn't classify floods | notebook 02 section 2 |
| Rain episode | **Exploratory grouping, not a definition of an event.** Non-tidal events grouped across the whole network: a new episode starts when an event begins more than 6 h after the latest end time of all earlier events | The 6 h default borrows the minimum interevent time used to separate rainstorms (e.g. Driscoll et al. 1989), adapted to flood timing. Results are worth checking at other gaps. See caveat 4 | `floodnet.build_rain_episodes`; notebook 06 checks episode counts across gaps |
| Deployment (exposure) | Days from install to removal or to the data cutoff, whichever comes first | Sensor metadata; assumes continuous operation (caveat 6) | `floodnet.days_deployed` |
| Data cutoff | End of the latest event in the dataset, not the download date | Keeps rates stable across re-runs. See caveat 8 | notebooks 02, 08 |
| New event | An event not in `data/event-log.csv` when a download is compared with it, matched on `sensor_id` + `flood_start_time`. The latest batch is the events with the newest `first_seen`. `first_seen` is when this repo first saw the event, not a publish date; events from before the first logged download share that download's date | Row-load timestamps can't be used: a full reload re-stamps every row. A skipped refresh merges two publishes into one batch, and a removed event that returns counts as new | `floodnet.update_event_log`; notebooks 00, 02, 04 |
| Started before the previous cutoff | Latest-batch event whose start is earlier than the latest end time among events first seen before that batch | Same idea as the data cutoff, applied to the previous batch. Marks events that reached us late; publication has no sharp line, so it isn't a QC measure | `floodnet.previous_cutoff`; notebook 04 |
| Active sensor-month | Sensor installed on or before the month's last day and not removed before its first | Sensor metadata | notebooks 05, 08 |
| Minimum record | Only sensors deployed ≥ 180 days are ranked by rate | **Judgment call:** keeps one early flood from producing an extreme rate. Not hydrological; doesn't guarantee a full seasonal cycle | notebook 02 |
| Minimum floods | Only sensors with ≥ 3 qualifying events (floods for the 4 in average, severe floods for the 12 in average) are ranked by average time above a depth. Notebook 07 uses the same minimum of 3 severe floods per sensor for its within-site correlation (`MIN_EVENTS_PER_SENSOR`) | **Judgment call:** keeps one or two events from standing in for an average. Not hydrological; notebook 02 prints how much each top 10 changes at a minimum of 2 or 5, and notebook 07 suggests trying 2 or 4 | notebook 02 section 5; notebook 07 section 4 |
| Share of sensors flooded | Rain episodes are ranked by the lower bound of the 95% Wilson score interval for the share of active non-tidal sensors that reached 4 in | Wilson (1927) interval, a standard choice for small counts. **Judgment call:** ranking on the lower bound keeps episodes with few active sensors from ranking first on a high share alone. Sensors aren't a random sample of the city (caveat 5), so the interval reflects how few sensors were counted, not uncertainty about the city as a whole | notebook 05 sections 3.4 and 6 |
| Storm window | `storm_events` / `plot_storm_events` keep events overlapping the storm's ET calendar day, padded by `time_buffer` hours on each side | **Judgment call, no grounded basis yet:** the buffer is set per storm (0 to 12 h) to take in its flooding. Counts depend on it, so storms compared by count should share a buffer | `floodnet.storm_events`; notebook 03 |
| Outlier (metadata) | A `lowest_point_height_delta_inches` value more than 1.5 × IQR below the first quartile or above the third | Tukey's (1977) box-plot rule, a standard screening convention. Flags values to check, not errors | notebook 01 |
| Storm plot floor | `storm_events` / `plot_storm_events` keep events with peak ≥ `min_depth_inches`; the default of 0 keeps every event | No filter by default. Pass 4 to show floods only, or another floor with a stated basis | `floodnet.storm_events`; notebook 03 |
| Separate tidal rise | Within one flood at a tidal sensor, a run of profile readings ≥ 4 in, located by its peak (deepest reading); rises whose peaks are less than 6.2 h apart are joined into one, keeping the deeper peak. A gap in the readings doesn't end a rise | Flood tier for the depth. The 6.2 h spacing is half the M2 tidal period (12.42 h): two high-tide peaks can't be closer than that, so closer peaks are depth flickering around 4 in or one uneven crest. A multi-rise flood is a candidate for merged tides, not a confirmed one: peaks spaced far from 12.4 or 24.8 h point to rain, surge or a bad reading. The count can also miss tides that stay below 4 in at the sensor (caveat 1). The notebook prints counts at 3 h and 9 h too | notebook 08 section 2 |
| Tidal flood day | A New York calendar date (ET) on which at least one tidal sensor recorded a flood; counted once however many sensors flooded | **Judgment call:** one high tide can flood many sensors, so counting floods would treat one tide as many observations. Consecutive days still aren't independent | notebook 08 section 4 |
| Moon phase | Days since the most recent new or full moon (0 to ≈ 14.77), from the UTC instant of the day's first flood, using the mean synodic month (29.530589 days) counted from the new moon of 2000-01-06 18:14 UTC | Mean lunar cycle (Meeus, *Astronomical Algorithms*); actual new and full moons differ from the mean by up to about 14 h | notebook 08 section 4 |

Flood and severe flood are nested, not exclusive: every severe flood is also a
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
   - The flood and severe-flood tiers apply to depth at the sensor, which is a
     lower bound on the deepest water nearby. The Flood Maps tiers classify
     modeled flood areas; applying them at one sensor is an adaptation.
   - Comparing raw depths across sensors partly compares mounting height.
     Notebooks that rank or compare depths across sensors say so.
2. **Peaks can be spurious, and snow interferes.** Objects under a sensor
   (people, vehicles, trash) can leave anomalous readings. A single bad point
   can inflate `max_depth_inches` and distort `onset_time_mins` and
   `drain_time_mins`. Snow piled under a sensor can produce false readings or
   hide a flood shallower than the pile. Rankings by maximum depth and winter
   results deserve the most scrutiny. An unusually long event at a non-tidal
   sensor can be spurious (an object or snow pile left under the sensor can
   hold readings above 10 mm for hours or days) or real (water ponding where
   it can't drain); check the depth profile before reading it either way.
   Readings are usually a minute apart, but gaps of 5 minutes or more occur
   throughout the record, not only before November 2021, when some sensors
   sampled every 5 minutes. Where readings are sparse, onset, drain and
   threshold-crossing times are coarser. A few events also disagree with
   themselves or with the metadata: the deepest reading in the depth profile
   can differ from `max_depth_inches`, and an event can start before its
   sensor's `date_installed`. Check both before relying on a single event.

### What the observations mean
3. **Split tidal vs. non-tidal.** `tidally_influenced` (sensor metadata) marks
   two distinct flooding regimes. Analyze them separately or facet/color by the
   flag. A table or statistic that pools both groups is acceptable only when
   it is followed by the same view broken out by the flag. Tidal sensors flood
   with high tides, roughly twice a day, so a few coastal sites can dominate
   any pooled count. The flag is per sensor, not per event: a tidal sensor can
   still record rain-driven floods. Rain-based rules such as the episode
   grouping apply to non-tidal sensors only.
   - An event at a tidal sensor can span several high tides. FloodNet's
     events can include stretches where depth drops to 10 mm or below, so
     successive tides can join into one event even if the water drains
     between them. That event counts once, its `duration_mins` includes the
     low-tide troughs, and it outranks single-tide events in any per-event
     duration ranking or average. `duration_above_4_inches_mins` excludes
     time below 4 in but still adds up every tide. Where this happens,
     per-event results partly measure how many tides merged. Many long tidal
     events show one sustained peak instead, and notebook 08 section 2 counts
     how many floods hold more than one separate rise. Check that count, and
     the depth profile, before reading a long tidal event either way.
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
   (notebook 04 counts the new events that started before the previous
   cutoff, calling them late arrivals). The record runs only to the data
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
- Tukey, J. W. (1977). *Exploratory Data Analysis.* Addison-Wesley. (Source
  of the 1.5 × IQR outlier rule.)
- Wilson, E. B. (1927). Probable inference, the law of succession, and
  statistical inference. *Journal of the American Statistical Association*,
  22(158), 209–212. <https://doi.org/10.2307/2276774>

**Citing the data.** FloodNet asks that publications list the project as
"FloodNet (New York University and The City University of New York)" and cite
Mydlarz et al. (2024).
