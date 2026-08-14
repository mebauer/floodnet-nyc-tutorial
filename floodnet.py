# floodnet.py
# Standard library
import ast
from datetime import timedelta

# Third-party libraries
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import polars as pl

# Colorblind-friendly palette (Paul Tol's bright scheme)
COLORBLIND_PALETTE = [
    "#4477AA",  # blue
    "#EE6677",  # red
    "#228833",  # green
    "#CCBB44",  # yellow
    "#66CCEE",  # cyan
    "#AA3377",  # purple
    "#BBBBBB",  # grey
    "#EE9944",  # orange
]


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def time_to_threshold(
    df,
    threshold_inches: float,
    top_n: int = 10,
    ts_sec_col="flood_profile_time_secs",
    ts_in_col="flood_profile_depth_inches",
    max_col="max_depth_inches",
    name_col="sensor_name",
    start_col="flood_start_time_et",
    end_col="flood_end_time_et",
):
    """Rank flood events by how fast they reached a depth threshold.

    For each event whose peak clears `threshold_inches`, finds the first
    upward crossing and linearly interpolates between the bracketing readings
    so the answer isn't quantized to the sampling interval.

    Args:
        df: One row per flood event. Pandas accepted.
        threshold_inches: Depth to time. Events peaking below are skipped.
        top_n: Rows returned, fastest first.
        ts_sec_col: List column of elapsed seconds. JSON strings decoded.
        ts_in_col: List column of depths, parallel to `ts_sec_col`.
        max_col: Precomputed event peak; used to skip events cheaply.
        name_col, start_col, end_col: Carried through for labeling.

    Returns:
        Ranked frame with crossing time in seconds and minutes, average rate
        to threshold, and the full profile as `x_values`/`y_values` for
        plotting. Empty frame if nothing crosses.
    """
    if not isinstance(df, pl.DataFrame):
        df = pl.from_pandas(df)

    if df.is_empty():
        return pl.DataFrame()

    # Stable key to group by after exploding.
    df = df.with_row_index("event_id")

    # Parse list columns.
    df = df.with_columns([
        pl.col(ts_sec_col).map_elements(
            lambda x: ast.literal_eval(x) if isinstance(x, str) else x,
            return_dtype=pl.List(pl.Float64),
        ).alias("sec"),

        pl.col(ts_in_col).map_elements(
            lambda x: ast.literal_eval(x) if isinstance(x, str) else x,
            return_dtype=pl.List(pl.Float64),
        ).alias("depth"),
    ])

    # Skip events that never peak above threshold, before the costly explode.
    df = df.filter(
        pl.col("sec").is_not_null()
        & pl.col("depth").is_not_null()
        & (pl.col(max_col) >= threshold_inches)
    )

    if df.is_empty():
        return pl.DataFrame()

    # Explode to one row per reading; the two lists stay aligned.
    long = (
        df.select(
            "event_id",
            name_col,
            start_col,
            end_col,
            max_col,
            "sec",
            "depth",
        )
        .explode(["sec", "depth"])
        .with_columns([
            pl.col("sec").cast(pl.Float64),
            pl.col("depth").cast(pl.Float64),
        ])
        .drop_nulls(["sec", "depth"])
    )

    # Re-anchor each event to its own start; clamp sub-zero sensor noise.
    long = (
        long
        .with_columns(
            (pl.col("sec") - pl.first("sec").over("event_id")).alias("rel_sec")
        )
        .with_columns(
            pl.when(pl.col("depth") < 0)
            .then(0.0)
            .otherwise(pl.col("depth"))
            .alias("depth")
        )
        .sort(["event_id", "rel_sec"])
    )

    # Stash the full series before collapsing, so callers can plot the curve.
    series_data = (
        long
        .group_by("event_id")
        .agg([
            pl.col("rel_sec").implode().alias("x_values"),
            pl.col("depth").implode().alias("y_values"),
        ])
    )

    # Add previous point for interpolation.
    long = long.with_columns([
        pl.col("depth").shift(1).over("event_id").alias("prev_depth"),
        pl.col("rel_sec").shift(1).over("event_id").alias("prev_sec"),
        pl.first("depth").over("event_id").alias("start_depth"),
    ])

    # Upward crossings only: below on the previous reading, at or above now.
    crossings = long.filter(
        (pl.col("prev_depth") < threshold_inches) &
        (pl.col("depth") >= threshold_inches)
    )

    # Interpolate crossing time.
    crossings = crossings.with_columns(
        (
            pl.col("prev_sec")
            + (threshold_inches - pl.col("prev_depth"))
            / (pl.col("depth") - pl.col("prev_depth"))
            * (pl.col("rel_sec") - pl.col("prev_sec"))
        ).alias("time_to_thresh_sec")
    )

    # Collapse to one row per event; `first` takes the earliest crossing.
    crossings = (
        crossings
        .group_by("event_id")
        .agg([
            pl.first("time_to_thresh_sec"),
            pl.first("start_depth"),
            pl.first(name_col).alias("name"),
            pl.first(start_col).alias("start"),
            pl.first(end_col).alias("end"),
            pl.first(max_col).alias("depth_max_inches"),
        ])
    )

    if crossings.is_empty():
        return pl.DataFrame()

    crossings = crossings.join(series_data, on="event_id", how="left")

    # Rate is the average climb from the event's opening depth, not a slope
    # at the crossing itself.
    crossings = crossings.with_columns([
        pl.lit(threshold_inches).alias("threshold_inches"),
        pl.col("time_to_thresh_sec").round(2),
        (pl.col("time_to_thresh_sec") / 60).round(2).alias("time_to_thresh_minutes"),
        (
            (threshold_inches - pl.col("start_depth"))
            / (pl.col("time_to_thresh_sec") / 60)
        ).round(2).alias("rate_to_thresh_in_per_min"),
    ])

    return (
        crossings
        .sort("time_to_thresh_sec")
        .head(top_n)
        .select([
            "name",
            "depth_max_inches",
            "start",
            "end",
            "threshold_inches",
            "time_to_thresh_sec",
            "time_to_thresh_minutes",
            "rate_to_thresh_in_per_min",
            "x_values",
            "y_values",
        ])
    )


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def plot_threshold_crossings(
    profiles,
    time_col: str = "time_to_thresh_sec",
    threshold_col: str = "threshold_inches",
    name_col: str = "name",
    depth_max_col: str = "depth_max_inches",
    start_col: str = "start",
    end_col: str = "end",
    x_values_col: str = "x_values",
    y_values_col: str = "y_values",
):
    """Plot one figure per event, marking the threshold crossing.

    Consumes the output of `time_to_threshold`: each row carries its full
    profile plus the crossing time, drawn as a horizontal line at the
    threshold depth and a vertical line at the time it was reached.

    Args:
        profiles: One row per event. Pandas accepted; None or empty is a
            no-op. Rows with missing, empty, or mismatched profiles are
            skipped.
        time_col: Crossing time in seconds; positions the vertical line.
        threshold_col: Threshold depth; positions the horizontal line.
        name_col, depth_max_col, start_col, end_col: Title text only.
        x_values_col: Elapsed seconds, parallel to `y_values_col`.
        y_values_col: Depths in inches.

    Returns:
        list[(Figure, Axes)], one pair per plotted event, undisplayed, so the
        caller can title or save each. Empty list if there is nothing to plot.
    """
    if profiles is None:
        return []
    if not isinstance(profiles, pl.DataFrame):
        profiles = pl.from_pandas(profiles)
    if profiles.is_empty():
        return []

    figures = []

    for profile in profiles.iter_rows(named=True):
        name = profile.get(name_col, "")
        depth_max_inches = profile.get(depth_max_col, np.nan)
        start = profile.get(start_col)
        end = profile.get(end_col)
        time_to_thresh = profile.get(time_col, np.nan)
        threshold_inches = profile.get(threshold_col, np.nan)

        x = profile.get(x_values_col)
        y = profile.get(y_values_col)

        # Skip unplottable rows: parallel arrays must be present and aligned.
        if x is None or y is None:
            continue
        if len(x) == 0 or len(y) == 0 or len(x) != len(y):
            continue

        fig, ax = plt.subplots(figsize=(6, 4))

        # Plot time series.
        ax.plot(x, y, marker="o", linestyle="-")

        # Vertical line at time-to-threshold.
        if np.isfinite(time_to_thresh):
            ax.axvline(
                x=float(time_to_thresh),
                color="purple",
                linestyle="--",
                label=f"Time to {threshold_inches:g}in",
            )

        # Horizontal threshold line.
        if np.isfinite(threshold_inches):
            ax.axhline(
                y=float(threshold_inches),
                color="red",
                linestyle="--",
                label=f"{threshold_inches:g}in",
            )

        main_title = f"{name}"
        start_txt = (
            start.strftime("%Y-%m-%d %H:%M") if start is not None else "?"
        )
        # End is same-day in the common case, so time alone reads cleaner.
        end_txt = (
            end.strftime("%H:%M") if end is not None else "?"
        )
        subtitle = (
            f"Threshold: {threshold_inches:g} in • "
            f"Time to threshold: {time_to_thresh:.1f} s ({time_to_thresh/60:.2f} min)\n"
            f"Max depth: {depth_max_inches:.1f} in • "
            f"{start_txt} – {end_txt}"
        )
        # suptitle carries the sensor; ax title carries the stats subtitle.
        fig.suptitle(main_title, fontsize=12, fontweight="bold", y=0.94)
        ax.set_title(subtitle, fontsize=10)

        ax.set_xlabel("Time (seconds)")
        ax.set_ylabel("Depth (inches)")
        ax.legend()
        ax.grid(True)
        fig.tight_layout()

        figures.append((fig, ax))

    return figures


def plot_flood_event(
    df,
    name_col: str = "sensor_name",
    start_col: str = "flood_start_time_et",
    ts_sec_col: str = "flood_profile_time_secs",
    ts_in_col: str = "flood_profile_depth_inches",
):
    """Plot one flood event's depth profile against wall-clock time.

    Uses the first row of `df` only; filter before calling. Elapsed seconds
    are re-anchored to the earliest reading and offset from the event's start
    timestamp, so the x-axis reads as real dates rather than seconds.

    Args:
        df: Frame whose first row is the event. Pandas accepted.
        name_col: Sensor label for the title.
        start_col: Event start timestamp; anchors the x-axis.
        ts_sec_col: List column of elapsed seconds. JSON strings decoded.
        ts_in_col: List column of depths, parallel to `ts_sec_col`.

    Returns:
        (Figure, Axes), undisplayed.

    Raises:
        ValueError: Empty frame, missing/empty/mismatched profile arrays, or
            a null start time.
    """
    if not isinstance(df, pl.DataFrame):
        df = pl.from_pandas(df)
    if df.is_empty():
        raise ValueError("df is empty.")

    # Decode if the profiles survived a CSV round-trip as JSON strings.
    schema = df.schema
    if schema[ts_sec_col] == pl.Utf8:
        df = df.with_columns(
            pl.col(ts_sec_col).str.json_decode(pl.List(pl.Float64))
        )
    if schema[ts_in_col] == pl.Utf8:
        df = df.with_columns(
            pl.col(ts_in_col).str.json_decode(pl.List(pl.Float64))
        )

    event = df.row(0, named=True)
    sensor_name = event.get(name_col)
    start_time = event.get(start_col)
    if start_time is None:
        raise ValueError(f"Could not parse start time from '{start_col}'.")

    secs = event.get(ts_sec_col)
    depths_in = event.get(ts_in_col)
    if secs is None or depths_in is None:
        raise ValueError(
            f"Missing time-series data in '{ts_sec_col}' and/or '{ts_in_col}'."
        )
    if len(secs) == 0 or len(depths_in) == 0:
        raise ValueError("Time-series arrays are empty.")
    # Parallel arrays: a length mismatch means silently misaligned readings.
    if len(secs) != len(depths_in):
        raise ValueError("Time-series arrays have different lengths (secs vs depths).")

    # Pair the arrays so drops and sorting keep them aligned.
    ts = (
        pl.DataFrame({"sec": secs, "depth_in": depths_in})
        .drop_nulls()
        .sort("sec")
    )
    if ts.is_empty():
        raise ValueError("Time-series data is all null after cleaning.")

    # Re-anchor to the earliest reading so a nonzero first sample starts at 0.
    ts = ts.with_columns((pl.col("sec") - pl.first("sec")).alias("sec"))

    # Offset from the event start to get absolute timestamps.
    ts = ts.with_columns(
        (pl.lit(start_time) + pl.duration(seconds=pl.col("sec"))).alias("timestamp")
    )

    timestamps = ts["timestamp"].to_list()
    depths = ts["depth_in"].to_list()

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(timestamps, depths, marker="o", linestyle="-")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d/%y %H:%M"))
    fig.autofmt_xdate(rotation=30, ha="right")

    title_start = start_time.strftime("%m/%d/%y %H:%M")
    ax.set_title(f"Sensor: {sensor_name}\nFlood Start: {title_start}")
    ax.set_xlabel("Date/Time")
    ax.set_ylabel("Flood Depth (inches)")
    ax.grid(True)
    fig.tight_layout()

    return fig, ax


def plot_sensor_profiles(df, sensor_id=None, alpha=None):
    """Overlay flood depth-vs-time curves, one line per event.

    Args:
        df: Frame with list columns `flood_profile_time_secs` and
            `flood_profile_depth_inches`, plus `sensor_id`. Pandas accepted.
            Any subsetting beyond `sensor_id` is the caller's job.
        sensor_id: Plot only this sensor. None plots every event in `df`.
        alpha: Line opacity 0-1. None scales it to row count so dense
            overlays stay legible.

    Returns:
        (Figure, Axes), undisplayed, so the caller can title or save.

    Raises:
        ValueError: No rows to plot.
    """
    if not isinstance(df, pl.DataFrame):
        df = pl.from_pandas(df)

    if sensor_id is not None:
        df = df.filter(pl.col("sensor_id") == sensor_id)

    # Fail loudly: a typo'd sensor_id would otherwise render a blank grid.
    if df.is_empty():
        raise ValueError(
            f"No events to plot for sensor_id={sensor_id!r}."
            if sensor_id is not None
            else "No events to plot; `df` is empty."
        )

    # Fade lines as they pile up so dense overlays stay legible.
    if alpha is None:
        n_events = df.height
        alpha = 1.0 if n_events <= 1 else max(0.1, min(1.0, 5.0 / n_events))

    fig, ax = plt.subplots(figsize=(6, 4))

    # iter_rows yields each event's two lists as parallel sequences.
    for secs, depths in df.select([
        "flood_profile_time_secs",
        "flood_profile_depth_inches"
    ]).iter_rows():
        ax.plot(
            secs,
            depths,
            color=COLORBLIND_PALETTE[0],
            alpha=alpha,
            marker="o",  # exposes irregular sampling a bare line would hide
            linestyle="-",
        )

    ax.set_xlabel("Seconds from start")
    ax.set_ylabel("Flood depth (inches)")
    ax.grid(True)
    fig.tight_layout()

    return fig, ax


def plot_storm_events(
    df,
    date_storm,
    time_buffer: int,
    storm_name: str,
    legend_out: bool = False,
    start_col: str = "flood_start_time_et",
    end_col: str = "flood_end_time_et",
    max_col: str = "max_depth_inches",
    sensor_col: str = "sensor_name",
    ts_sec_col: str = "flood_profile_time_secs",
    ts_in_col: str = "flood_profile_depth_inches",
    min_depth_inches: float = 2.0,
):
    """Overlay every sensor's flood profile for one storm on a shared clock.

    Unlike the per-event plots, all curves share a real datetime x-axis, so
    sensors can be compared for onset order and peak timing. Events are kept
    if they overlap the storm window at all, not just if they start inside it.

    Args:
        df: One row per flood event. Pandas accepted.
        date_storm: Storm date string; parsed then truncated to local midnight.
        time_buffer: Hours of padding on each side of the 24-hour storm day.
        storm_name: Title text.
        legend_out: Place the legend outside the axes for crowded plots.
        start_col: Event start; also the anchor for each profile's timestamps.
        end_col: Event end; used for window overlap and x-limits.
        max_col: Event peak; events at or below `min_depth_inches` are dropped.
        sensor_col: Grouping key for color and legend entries.
        ts_sec_col: List column of elapsed seconds, parallel to `ts_in_col`.
        ts_in_col: List column of depths.
        min_depth_inches: Exclusive floor on peak depth.

    Returns:
        (Figure, Axes), undisplayed.

    Raises:
        ValueError: Empty frame, or no events overlapping the window.
    """
    if df is None:
        raise ValueError("df is empty.")

    if not isinstance(df, pl.DataFrame):
        df = pl.from_pandas(df)

    if df.is_empty():
        raise ValueError("df is empty.")

    # --- Match storm datetime timezone to dataframe
    # Borrow the column's zone so comparisons below don't mix naive and aware.
    tz = df.schema[start_col].time_zone

    storm_dt = (
        pl.Series([date_storm])
        .str.to_datetime()
        .dt.replace_time_zone(tz)
        .item()
    ).replace(hour=0, minute=0, second=0, microsecond=0)

    # Symmetric buffer: time_buffer hours before storm start and after storm end (24h window)
    window_start = storm_dt - timedelta(hours=time_buffer)
    window_end = storm_dt + timedelta(hours=24) + timedelta(hours=time_buffer)

    # --- Select events overlapping the storm window
    # Overlap, not containment: an event straddling either edge still counts.
    events = (
        df.filter(
            (pl.col(end_col) >= window_start)
            & (pl.col(start_col) <= window_end)
            & (pl.col(max_col) > min_depth_inches)
            & pl.col(ts_sec_col).is_not_null()
            & pl.col(ts_in_col).is_not_null()
        )
        .sort(start_col)
    )

    if events.is_empty():
        raise ValueError("No matching events found for the requested storm window.")

    # --- Sensor color map (colorblind-friendly)
    unique_sensors = (
        events.select(sensor_col)
        .drop_nulls()
        .unique()
        .to_series()
        .to_list()
    )

    # Repeat the palette so more sensors than colors still maps cleanly.
    palette = COLORBLIND_PALETTE * ((len(unique_sensors) // len(COLORBLIND_PALETTE)) + 1)
    sensor_colors = {sensor: palette[i] for i, sensor in enumerate(unique_sensors)}

    # Scope the style so it doesn't leak into other plots in the session.
    with plt.style.context("seaborn-v0_8-whitegrid"):
        fig, ax = plt.subplots(figsize=(8, 6))

        seen_sensors = set()
        cols = [sensor_col, start_col, ts_sec_col, ts_in_col]

        for row in events.select(cols).iter_rows(named=True):

            sensor_name = row.get(sensor_col)
            start_time = row.get(start_col)

            secs = row.get(ts_sec_col)
            depths = row.get(ts_in_col)

            # Skip unplottable rows: parallel arrays must be present and aligned.
            if secs is None or depths is None or start_time is None:
                continue

            if len(secs) == 0 or len(depths) == 0 or len(secs) != len(depths):
                continue

            # Clamp sub-zero sensor noise to the dry baseline.
            secs = np.asarray(secs, dtype=float)
            depths = np.maximum(np.asarray(depths, dtype=float), 0)

            # Drop NaN pairwise so both arrays stay index-aligned.
            mask = ~np.isnan(secs) & ~np.isnan(depths)
            secs = secs[mask]
            depths = depths[mask]

            if secs.size == 0:
                continue

            order = np.argsort(secs)
            secs = secs[order]
            depths = depths[order]

            # Re-anchor to the earliest reading so a nonzero first sample starts at 0.
            secs = secs - secs[0]

            # Strip tzinfo only here, just before passing to matplotlib
            timestamps = [
                (start_time + timedelta(seconds=float(s))).replace(tzinfo=None)
                for s in secs
            ]

            # label sensor only once
            # A sensor with several events gets one legend entry, not one per curve.
            label = None
            if sensor_name not in seen_sensors:
                label = sensor_name
                seen_sensors.add(sensor_name)

            color = sensor_colors.get(sensor_name)

            ax.plot(
                timestamps,
                depths,
                linestyle="-",
                linewidth=1.5,
                color=color,
                label=label,
                zorder=2,
            )

        # --- Axis bounds
        # Bound to observed events, not the requested window, so a wide buffer
        # doesn't leave dead space on either side.
        x_start = events[start_col].min()
        x_end = events[end_col].max()

        if x_end is None:
            x_end = events[start_col].max()

        x_start_naive = x_start.replace(tzinfo=None)
        x_end_naive = x_end.replace(tzinfo=None)
        ax.set_xlim(x_start_naive - timedelta(hours=1), x_end_naive + timedelta(hours=1))

        # --- Axis formatting
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d %H:%M"))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=3))

        ax.set_title(
            f"{storm_name}: {storm_dt.strftime('%b %d, %Y')}",
            fontsize=12,
            fontweight="bold",
        )
        ax.set_xlabel("Date / Time", fontsize=10)
        ax.set_ylabel("Flood Depth (inches)", fontsize=10)

        if legend_out:
            ax.legend(title="Sensor", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8, title_fontsize=9)
        else:
            ax.legend(title="Sensor", loc="upper right", fontsize=8, title_fontsize=9)

        fig.autofmt_xdate()
        fig.tight_layout()

    return fig, ax


def plot_ranked_sensors(
    ranked_df,
    metadata_gdf,
    boro_gdf,
    value_col,
    title,
    label=None,
    join_col="sensor_id",
    figsize=(8, 8),
    cmap="viridis",
):
    """
    Plot ranked FloodNet sensors on a NYC borough map.

    Merges a ranked sensor DataFrame onto point geometries and renders
    each sensor as a choropleth dot scaled by value_col. All sensors
    in metadata_gdf are shown as light gray reference points; only those
    present in ranked_df are colored.

    Parameters
    ----------
    ranked_df : pl.DataFrame
        Polars DataFrame of ranked sensors. Must contain join_col and value_col.
    metadata_gdf : gpd.GeoDataFrame
        Point geometries for all deployed sensors. Must contain join_col.
    boro_gdf : gpd.GeoDataFrame
        NYC borough boundary polygons used as the base map.
    value_col : str
        Column name in ranked_df to use for color mapping.
    title : str
        Map title displayed above the plot.
    label : str, optional
        Colorbar label. If None, no label is added to the legend.
    join_col : str, optional
        Column name to join ranked_df onto metadata_gdf. Default is "sensor_id".
    figsize : tuple of float, optional
        Figure dimensions as (width, height) in inches. Default is (8, 8).
    cmap : str, optional
        Matplotlib colormap name. Default is "viridis".

    Returns
    -------
    fig : matplotlib.figure.Figure
        The figure object.
    ax : matplotlib.axes.Axes
        The axes object.
    """
    # convert Polars to pandas
    ranked_pd = ranked_df.to_pandas()

    # merge ranked metrics onto geometry
    plot_gdf = (
        metadata_gdf
        .merge(
            ranked_pd,
            on=join_col,
            how="inner",
        )
        .sort_values(value_col)
    )

    legend_kwds = {
        "shrink": 0.70,
    }

    # optional legend label
    if label is not None:
        legend_kwds["label"] = label

    # create figure
    fig, ax = plt.subplots(figsize=figsize)

    # sensor plot
    plot_gdf.plot(
        column=value_col,
        ax=ax,
        legend=True,
        cmap=cmap,
        zorder=2,
        legend_kwds=legend_kwds,
    )

    # borough boundaries
    boro_gdf.plot(
        ax=ax,
        facecolor="None",
        linewidth=.5,
        edgecolor="gray",
        zorder=0,
    )

    metadata_gdf.plot(
        ax=ax,
        color="lightgray",
        alpha=0.35,
        zorder=1,
    )

    # labels
    ax.set_title(title, fontsize=13)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    plt.tight_layout()

    return fig, ax