import numpy as np
import pandas as pd
import altair as alt

from culib.field.getters import get_axes_from_list
from culib.plot.settings import (
    ALT_CATEGORY_COLOR_SCHEME,
    MLX_COLORS,
    CHART_WIDTH,
    CHART_HEIGHT,
    DEFAULT_NB_PLOT_MAX_MARK_POINTS,
)


def generate_chart_fields(
    df_plot,
    axis: str,
    Baxis: list,
    list_graphtitles: list[str],
    list_graphsubtitles: list[str],
    dezoom_factor: float,
    is_mark_points: bool = True,
) -> alt.Chart:
    # Param names
    x_param = axis
    field_ax = get_axes_from_list(Baxis) if len(get_axes_from_list(Baxis)) == 1 else ""
    y_param = f"B{field_ax}_mT"
    color_param = "Baxis_Coil"
    dict_graph_legends = {
        x_param: f"{x_param[0]} (mm)",
        y_param: f"{y_param[:-3]} (mT)",
    }
    dict_color_legend = {}
    for B in Baxis:
        # Display legend as "Bx mycoil", "Bx Total", "By A1" ...
        Btype = B[:2]  # Get "Bx", "By" or "Bz"
        coil_name = B[3:].split("_mT")[0]  # Look for stuff after Bx_
        coil_name = coil_name if (coil_name != "" and coil_name != "total") else "Total"
        dict_color_legend[B] = f"{Btype} {coil_name}"

    # Manage scale
    y_min_val = np.min(df_plot[Baxis].values)
    y_max_val = np.max(df_plot[Baxis].values)
    if y_min_val >= 0:
        y_min_plot = y_min_val * (1 - dezoom_factor)
    else:
        y_min_plot = y_min_val * (1 + dezoom_factor)

    if y_max_val >= 0:
        y_max_plot = y_max_val * (1 + dezoom_factor)
    else:
        y_max_plot = y_max_val * (1 - dezoom_factor)

    # Disable mark_points if too many points
    if len(df_plot) > DEFAULT_NB_PLOT_MAX_MARK_POINTS:
        is_mark_points = False

    # Declare chart_fields
    chart_fields = (
        alt.Chart(df_plot)
        .transform_fold(
            Baxis,
            as_=[color_param, y_param],
        )
        .mark_line(point=is_mark_points)
        .encode(
            x=alt.X(x_param + ":Q", title=dict_graph_legends[x_param]),
            y=alt.Y(
                y_param + ":Q",
                title=dict_graph_legends[y_param],
                scale=alt.Scale(zero=False, domain=(y_min_plot, y_max_plot)),
            ),
            color=alt.Color(
                "color_param_display:O",
                title="Baxis/Coil",
                scale=alt.Scale(
                    scheme=ALT_CATEGORY_COLOR_SCHEME,
                    range=MLX_COLORS,
                ),
            ),
            tooltip=[
                x_param + ":Q",
                y_param + ":Q",
                alt.Tooltip("color_param_display:O", title="Baxis/Coil"),
            ],
        )
        .transform_calculate(
            color_param_display=f"{dict_color_legend}[datum.{color_param}]",
        )
        .properties(
            width=CHART_WIDTH,
            height=CHART_HEIGHT,
            title={
                "text": list_graphtitles,
                "subtitle": list_graphsubtitles,
                "color": "black",
                "subtitleColor": "black",
                "fontSize": 19,
                "subtitleFontSize": 17,
            },
        )
        .interactive()
    )

    return chart_fields


def generate_chart_rules_and_labels(
    axis: str,
    dict_pos_mm_vs_label: dict,
) -> alt.Chart:
    df_plot_rules = pd.DataFrame(columns=[axis])
    for label, pos_mm in dict_pos_mm_vs_label.items():
        label = str(label)
        pos_mm = round(float(pos_mm), 2)
        df_plot_rules.loc[label] = pos_mm
    df_plot_rules = df_plot_rules.reset_index().rename(columns={"index": "label"})

    chart_rules = (
        alt.Chart(df_plot_rules)
        .mark_rule(color="red")
        .encode(
            alt.X(axis + ":Q"),
            # color = alt.Color(opacity=0.1),
        )
    )
    chart_labels = chart_rules.mark_text(
        align="left",
        baseline="bottom",
        dx=2,
        dy=CHART_HEIGHT / 2 - 2,
        color="red",
    ).encode(
        text="label:N",
    )

    return chart_rules + chart_labels
