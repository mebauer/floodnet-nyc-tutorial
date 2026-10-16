# Methods

How the analyses in these notebooks choose their parameters, and the caveats
every FloodNet analysis here is checked against. If you build your own analysis
on this data, the caveats apply there too.

## Analytical approach
The point of this repo is to teach good practice, not to show off technique.
- **The method can come from anywhere; the parameters cannot.** A purely
  statistical analysis is fine, but it must not contradict how flooding
  physically works or what these sensors can observe. Any threshold, grouping
  rule or derived metric is a hydrological claim: it traces back to something the
  field actually does, and the notebook says what (e.g. the 6-hour interevent dry
  period separating storms; depth thresholds taken from the dataset's own
  `duration_above_*_inches_mins` columns). If a threshold has no such basis, say
  so plainly and propose the grounded alternative — don't keep it because it's
  clever or because the numbers look good.
- Be expressive and creative with the analytics, visuals and narrative. That part
  is open.
- Judgment calls are fine when named as such: state the choice, its basis, and
  check whether the conclusions survive a different one.

## FloodNet data caveats — check every analysis against these
1. **Split tidal vs. non-tidal.** `tidally_influenced` (sensor metadata) marks two
   distinct flooding regimes. Unless told otherwise, analyze them separately or
   facet/color by the flag; never pool them into one summary statistic. The flag
   is per sensor, not per event — a tidal sensor can still record rain-driven
   floods. Rain-based rules (e.g. the 6-hour interevent dry period) apply to
   non-tidal sensors; tidal flooding follows the ~12.4 h tidal cycle.
2. **Normalize for staggered deployment.** Sensors were installed from 2020 onward
   and some were removed, so raw counts by year/month mostly track network growth.
   For any time comparison use exposure (events per sensor-year, install→removal
   or data cutoff) or a fixed cohort active the whole period. Check the
   install-date distribution first; flag partial years and years whose sensor
   count is thin relative to the rest.
3. **Observations ≠ vulnerability.** High depth or frequency at a sensor reflects
   where rain fell, sensor siting (sites were chosen non-randomly, often from
   community flood reports) and what the sensor can see — not intrinsic
   vulnerability. Describe rankings as "observed at this sensor"; don't generalize
   to neighborhoods/boroughs or rank vulnerability. That needs rainfall forcing
   (e.g. rain-on-grid).
4. **Surface observations only.** No rainfall or drainage data yet. Conclusions
   stay at the surface hydrology the sensors observe. Don't attribute floods to
   sewer capacity or storm intensity. `drain_time_mins` is recession at the
   sensor, not sewer performance; interevent-grouped "storms" are inferred from
   flood timing, not confirmed rain events.
5. **Absence of events ≠ dry.** The dataset has no sensor uptime record; exposure
   calculations assume continuous operation — say so.
6. **Not every event is a flood.** A dataset "event" starts at > 10 mm, so many
   events are shallow. In this repo a **flood** is peak depth ≥ 4 in and a
   **major flood** is ≥ 12 in. These are the NYC Stormwater Flood Maps depth
   tiers ("nuisance" 4 in to < 1 ft; "deep and contiguous" ≥ 1 ft), and the
   dataset's `duration_above_4/12_inches_mins` columns use the same breaks. The
   maps classify modeled flood areas; here the tiers are applied to depth at a
   single sensor. (`duration_above_24_inches_mins` also exists; not used as a
   tier.) Raw event counts are dominated by < 4 in events and can skew
   frequency results. Whether to filter depends on the question, so decide
   deliberately and state which definition a count uses.
