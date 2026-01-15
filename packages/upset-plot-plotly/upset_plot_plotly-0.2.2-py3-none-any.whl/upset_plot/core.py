"""
Generic Upset Plot Generator
This module provides a reusable class for creating upset plots from categorical data.
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class UpsetPlotGenerator:
    """
    A generic class for generating upset plots from categorical data.

    An upset plot visualizes the intersection of multiple sets/categories,
    showing both individual set sizes and intersection counts.
    """

    def __init__(self, df, categories_dict, total_n=None):
        """
        Initialize the UpsetPlotGenerator.

        Parameters:
        -----------
        df : pd.DataFrame
            The input dataframe
        categories_dict : dict
            Dictionary mapping category names to boolean Series.
            Example: {"Category A": df["col_a"] == True, "Category B": df["col_b"] > 0}
        total_n : int, optional
            Total count for percentage calculations. If None, uses len(df)
        """
        self.df = df.copy()
        self.categories_dict = categories_dict
        self.total_n = total_n if total_n is not None else len(df)
        self.intersection_df = None
        self.set_sizes = None

    def compute_combinations(self):
        """
        Compute the combinations and set sizes.

        Returns:
        --------
        tuple: (intersection_df, set_sizes)
            - intersection_df: DataFrame with columns ['combination', 'count']
            - set_sizes: Dictionary mapping category names to their total counts
        """
        # Add category columns to dataframe
        for name, series in self.categories_dict.items():
            self.df[name] = series

        # Calculate set sizes (total count for each category)
        self.set_sizes = {
            name: series.sum() for name, series in self.categories_dict.items()
        }

        # Create combination string for each row
        def get_combo(row):
            combo = []
            for name in self.categories_dict.keys():
                if row[name]:
                    combo.append(name)
            if not combo:
                return "None"
            # Sort to ensure consistent naming
            return " & ".join(sorted(combo))

        self.df["combination"] = self.df.apply(get_combo, axis=1)

        # Filter out 'None' and count combinations
        counts = (
            self.df[self.df["combination"] != "None"]["combination"]
            .value_counts()
            .sort_values(ascending=False)
        )

        # Convert to DataFrame
        self.intersection_df = counts.reset_index()
        self.intersection_df.columns = ["combination", "count"]

        return self.intersection_df, self.set_sizes

    def plot(
        self,
        title="Upset Plot",
        bar_color="#D32F2F",
        active_color="black",
        inactive_color="#F0F0F0",
        connection_color="red",
        height=None,
        combinations_range=None,
        min_sets=1,
    ):
        """
        Generate the upset plot visualization.

        Parameters:
        -----------
        title : str
            Plot title
        bar_color : str
            Color for the bar chart
        active_color : str
            Color for active category markers
        inactive_color : str
            Color for inactive category markers
        connection_color : str
            Color for connection lines between categories
        height : int, optional
            Height of the plot in pixels. If None, it's auto-calculated.
        combinations_range : tuple, optional
            (start, end) indices of combinations to display.
        min_sets : int, optional
            Minimum number of sets in a combination to be displayed.

        Returns:
        --------
        plotly.graph_objects.Figure or None
            The upset plot figure, or None if no data
        """
        if self.intersection_df is None or self.intersection_df.empty:
            self.compute_combinations()

        if self.intersection_df is None or self.intersection_df.empty:
            return None

        # Filter by minimum number of sets
        intersection_df = self.intersection_df.copy()
        if min_sets > 1:
            intersection_df = intersection_df[
                intersection_df["combination"].apply(
                    lambda x: len([c for c in x.split("&") if c.strip() != "None"])
                    >= min_sets
                )
            ]

        # Filter combinations if range is provided
        if combinations_range is not None:
            start, end = combinations_range
            intersection_df = intersection_df.iloc[start:end]

        if intersection_df.empty:
            return None

        # Identify categories that are present in the filtered combinations
        active_combinations = intersection_df["combination"].tolist()
        relevant_categories = set()
        for combo in active_combinations:
            relevant_categories.update([c.strip() for c in combo.split("&")])

        # Prepare data
        # Sort relevant categories by set size (ascending in list, so largest is at the top of plot)
        categories = sorted(
            [cat for cat in relevant_categories if cat in self.set_sizes],
            key=lambda x: self.set_sizes[x],
            reverse=False,
        )

        combinations = intersection_df["combination"].tolist()
        counts = intersection_df["count"].tolist()
        percentages = [(c / self.total_n) * 100 for c in counts]
        bar_text = [f"{c}<br>({p:.1f}%)" for c, p in zip(counts, percentages)]

        # Auto-calculate height if not provided
        if height is None:
            bar_area_min_height = 400
            matrix_area_height = len(categories) * 50
            height = max(800, bar_area_min_height + matrix_area_height)

        # Calculate row ratios
        matrix_ratio = (len(categories) * 50) / height
        matrix_ratio = max(0.3, min(0.7, matrix_ratio))
        row_heights = [1 - matrix_ratio, matrix_ratio]

        # Create matrix coordinates
        matrix_x = []
        matrix_y = []
        matrix_color = []

        for i, combo in enumerate(combinations):
            included = [c.strip() for c in combo.split("&")]
            for row_idx, cat in enumerate(categories):
                matrix_x.append(i)
                matrix_y.append(row_idx)
                if cat in included:
                    matrix_color.append(active_color)
                else:
                    matrix_color.append(inactive_color)

        # Create subplots: 2x2 grid
        # [1, 1] Empty  | [1, 2] Intersection Bar
        # [2, 1] Set Bar| [2, 2] Matrix
        fig = make_subplots(
            rows=2,
            cols=2,
            shared_xaxes=True,
            shared_yaxes=True,
            horizontal_spacing=0.05,
            vertical_spacing=0.05,
            row_heights=row_heights,
            column_widths=[0.25, 0.75],
            specs=[[None, {"type": "bar"}], [{"type": "bar"}, {"type": "scatter"}]],
        )

        # Add bar chart (Intersection Sizes) - Top Right
        fig.add_trace(
            go.Bar(
                x=list(range(len(combinations))),
                y=counts,
                text=bar_text,
                textposition="auto",
                marker_color=bar_color,
                showlegend=False,
            ),
            row=1,
            col=2,
        )

        # Add horizontal bar chart (Set Sizes) - Bottom Left
        cat_counts = [self.set_sizes[cat] for cat in categories]
        fig.add_trace(
            go.Bar(
                x=cat_counts,
                y=list(range(len(categories))),
                orientation="h",
                marker_color="#424242",
                text=cat_counts,
                textposition="auto",
                showlegend=False,
            ),
            row=2,
            col=1,
        )

        # Add matrix background lines - Bottom Right
        for i in range(len(categories)):
            fig.add_trace(
                go.Scatter(
                    x=[-0.5, len(combinations) - 0.5],
                    y=[i, i],
                    mode="lines",
                    line=dict(color="#EEEEEE", width=1),
                    hoverinfo="skip",
                    showlegend=False,
                ),
                row=2,
                col=2,
            )

        # Add connection lines - Bottom Right
        for i, combo in enumerate(combinations):
            included_indices = []
            included = [c.strip() for c in combo.split("&")]
            for idx, cat in enumerate(categories):
                if cat in included:
                    included_indices.append(idx)

            if len(included_indices) > 1:
                fig.add_trace(
                    go.Scatter(
                        x=[i, i],
                        y=[min(included_indices), max(included_indices)],
                        mode="lines",
                        line=dict(color=connection_color, width=3),
                        hoverinfo="skip",
                        showlegend=False,
                    ),
                    row=2,
                    col=2,
                )

        # Add scatter dots - Bottom Right
        fig.add_trace(
            go.Scatter(
                x=matrix_x,
                y=matrix_y,
                mode="markers",
                marker=dict(size=18, color=matrix_color),
                hoverinfo="skip",
                showlegend=False,
            ),
            row=2,
            col=2,
        )

        # Add checkmarks - Bottom Right
        fig.add_trace(
            go.Scatter(
                x=matrix_x,
                y=matrix_y,
                mode="text",
                text=["✓"] * len(matrix_x),
                textfont=dict(color="#F0F0F0", size=14),
                hoverinfo="skip",
                showlegend=False,
            ),
            row=2,
            col=2,
        )

        # Update layout
        fig.update_layout(
            title={
                "text": title,
                "x": 0.5,
                "xanchor": "center",
            },
            height=height,
            plot_bgcolor="white",
            margin=dict(l=50, r=50, t=80, b=50),
        )

        # Update Axes
        # Intersection Sizes Bar Chart (Top Right)
        fig.update_xaxes(
            showticklabels=False,
            range=[-0.5, len(combinations) - 0.5],
            zeroline=False,
            showgrid=False,
            row=1,
            col=2,
        )
        fig.update_yaxes(title="Intersection Size", gridcolor="#F0F0F0", row=1, col=2)

        # Set Sizes Bar Chart (Bottom Left)
        fig.update_xaxes(
            title="Set Size",
            autorange="reversed",
            gridcolor="#F0F0F0",
            row=2,
            col=1,
        )
        fig.update_yaxes(
            tickmode="array",
            tickvals=list(range(len(categories))),
            ticktext=categories,
            range=[-0.5, len(categories) - 0.5],
            showgrid=False,
            zeroline=False,
            row=2,
            col=1,
        )

        # Matrix (Bottom Right)
        fig.update_xaxes(
            showticklabels=False,
            zeroline=False,
            showgrid=False,
            range=[-0.5, len(combinations) - 0.5],
            row=2,
            col=2,
        )
        fig.update_yaxes(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            range=[-0.5, len(categories) - 0.5],
            row=2,
            col=2,
        )

        return fig


# ... (existing content)


class ColoredUpsetPlotGenerator(UpsetPlotGenerator):
    """
    Subclass of UpsetPlotGenerator that colors the plot elements based on the composition
    of the combinations (e.g. Followup vs Additional tests).
    """

    def __init__(self, df, categories_dict, total_n=None, category_colors=None):
        """
        Initialize with category_colors mapping.

        Parameters:
        -----------
        category_colors : dict
            Dictionary mapping category names to their color (e.g. '#D32F2F', '#1976D2', 'purple')
        """
        super().__init__(df, categories_dict, total_n)
        self.category_colors = category_colors or {}

    def plot(
        self,
        title="Upset Plot",
        bar_color="#D32F2F",
        active_color="black",
        inactive_color="#F0F0F0",
        connection_color="red",
        height=None,
        combinations_range=None,
        min_sets=1,
    ):
        if self.intersection_df is None or self.intersection_df.empty:
            return None

        # Filter by minimum number of sets
        intersection_df = self.intersection_df.copy()
        if min_sets > 1:
            intersection_df = intersection_df[
                intersection_df["combination"].apply(
                    lambda x: len([c for c in x.split("&") if c.strip() != "None"])
                    >= min_sets
                )
            ]

        # Filter combinations if range is provided
        if combinations_range is not None:
            start, end = combinations_range
            intersection_df = intersection_df.iloc[start:end]

        if intersection_df.empty:
            return None

        # Identify categories that are present in the filtered combinations
        active_combinations = intersection_df["combination"].tolist()
        relevant_categories = set()
        for combo in active_combinations:
            relevant_categories.update([c.strip() for c in combo.split("&")])

        # Prepare data
        categories = sorted(
            [cat for cat in relevant_categories if cat in self.set_sizes],
            key=lambda x: self.set_sizes[x],
            reverse=False,
        )

        combinations = intersection_df["combination"].tolist()
        counts = intersection_df["count"].tolist()
        percentages = [(c / self.total_n) * 100 for c in counts]
        bar_text = [f"{c}<br>({p:.1f}%)" for c, p in zip(counts, percentages)]

        # Auto-calculate height if not provided
        if height is None:
            bar_area_min_height = 400
            matrix_area_height = len(categories) * 50
            height = max(800, bar_area_min_height + matrix_area_height)

        # Calculate row ratios
        matrix_ratio = (len(categories) * 50) / height
        matrix_ratio = max(0.3, min(0.7, matrix_ratio))
        row_heights = [1 - matrix_ratio, matrix_ratio]

        # Create matrix coordinates
        matrix_x = []
        matrix_y = []
        matrix_color = []

        for i, combo in enumerate(combinations):
            included = [c.strip() for c in combo.split("&")]
            for row_idx, cat in enumerate(categories):
                matrix_x.append(i)
                matrix_y.append(row_idx)
                if cat in included:
                    # ROW-BASED COLORING: Use the specific color for this category (test)
                    matrix_color.append(self.category_colors.get(cat, active_color))
                else:
                    matrix_color.append(inactive_color)

        # Create subplots
        fig = make_subplots(
            rows=2,
            cols=2,
            shared_xaxes=True,
            shared_yaxes=True,
            horizontal_spacing=0.05,
            vertical_spacing=0.05,
            row_heights=row_heights,
            column_widths=[0.25, 0.75],
            specs=[[None, {"type": "bar"}], [{"type": "bar"}, {"type": "scatter"}]],
        )

        # Add bar chart (Intersection Sizes) - Top Right
        # Revert to standard bar_color
        fig.add_trace(
            go.Bar(
                x=list(range(len(combinations))),
                y=counts,
                text=bar_text,
                textposition="auto",
                marker_color=bar_color,
                showlegend=False,
            ),
            row=1,
            col=2,
        )

        # Add horizontal bar chart (Set Sizes) - Bottom Left
        cat_counts = [self.set_sizes[cat] for cat in categories]
        fig.add_trace(
            go.Bar(
                x=cat_counts,
                y=list(range(len(categories))),
                orientation="h",
                marker_color="#424242",
                text=cat_counts,
                textposition="auto",
                showlegend=False,
            ),
            row=2,
            col=1,
        )

        # Add matrix background lines - Bottom Right
        for i in range(len(categories)):
            fig.add_trace(
                go.Scatter(
                    x=[-0.5, len(combinations) - 0.5],
                    y=[i, i],
                    mode="lines",
                    line=dict(color="#EEEEEE", width=1),
                    hoverinfo="skip",
                    showlegend=False,
                ),
                row=2,
                col=2,
            )

        # Add connection lines - Bottom Right
        for i, combo in enumerate(combinations):
            included_indices = []
            included = [c.strip() for c in combo.split("&")]
            for idx, cat in enumerate(categories):
                if cat in included:
                    included_indices.append(idx)

            if len(included_indices) > 1:
                # For connection lines in row-based coloring, we can't easily have multi-colored lines.
                # Standard Upset plots use a single color for the connection line.
                # However, to facilitate the visual, maybe we use standard grey or the bar color?
                # User said "limited to the sactter only", so let's keep lines standard.
                fig.add_trace(
                    go.Scatter(
                        x=[i, i],
                        y=[min(included_indices), max(included_indices)],
                        mode="lines",
                        line=dict(color=connection_color, width=3),
                        hoverinfo="skip",
                        showlegend=False,
                    ),
                    row=2,
                    col=2,
                )

        # Add scatter dots - Bottom Right
        fig.add_trace(
            go.Scatter(
                x=matrix_x,
                y=matrix_y,
                mode="markers",
                marker=dict(size=18, color=matrix_color),  # Specific row/test colors
                hoverinfo="skip",
                showlegend=False,
            ),
            row=2,
            col=2,
        )

        # Add checkmarks - Bottom Right
        fig.add_trace(
            go.Scatter(
                x=matrix_x,
                y=matrix_y,
                mode="text",
                text=["✓"] * len(matrix_x),
                textfont=dict(color="#FFFFFF", size=14),
                hoverinfo="skip",
                showlegend=False,
            ),
            row=2,
            col=2,
        )

        # Update layout
        fig.update_layout(
            title={
                "text": title,
                "x": 0.5,
                "xanchor": "center",
            },
            height=height,
            plot_bgcolor="white",
            margin=dict(l=50, r=50, t=80, b=50),
        )

        # Update Axes (same as base)
        fig.update_xaxes(
            showticklabels=False,
            range=[-0.5, len(combinations) - 0.5],
            zeroline=False,
            showgrid=False,
            row=1,
            col=2,
        )
        fig.update_yaxes(title="Intersection Size", gridcolor="#F0F0F0", row=1, col=2)

        fig.update_xaxes(
            title="Set Size",
            autorange="reversed",
            gridcolor="#F0F0F0",
            row=2,
            col=1,
        )
        fig.update_yaxes(
            tickmode="array",
            tickvals=list(range(len(categories))),
            ticktext=categories,
            range=[-0.5, len(categories) - 0.5],
            showgrid=False,
            zeroline=False,
            row=2,
            col=1,
        )

        fig.update_xaxes(
            showticklabels=False,
            zeroline=False,
            showgrid=False,
            range=[-0.5, len(combinations) - 0.5],
            row=2,
            col=2,
        )
        fig.update_yaxes(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            range=[-0.5, len(categories) - 0.5],
            row=2,
            col=2,
        )

        return fig


def plot(
    df,
    categories_dict,
    title="Upset Plot",
    bar_color="#D32F2F",
    active_color="black",
    inactive_color="#F0F0F0",
    connection_color="red",
    height=None,
    combinations_range=None,
    min_sets=1,
    category_colors=None,
):
    """
    Simplified helper function to generate an Upset Plot directly.

    Parameters:
    -----------
    df : pd.DataFrame
        The input dataframe
    categories_dict : dict
        Dictionary mapping category names to boolean Series.
    title : str
        Plot title
    bar_color : str
        Color for the bar chart
    active_color : str
        Color for active category markers
    inactive_color : str
        Color for inactive category markers
    connection_color : str
        Color for connection lines between categories
    height : int, optional
        Height of the plot in pixels. If None, it's auto-calculated.
    combinations_range : tuple, optional
        (start, end) indices of combinations to display.
    min_sets : int, optional
        Minimum number of sets in a combination to be displayed.
    category_colors : dict, optional
        If provided, uses ColoredUpsetPlotGenerator with these colors.

    Returns:
    --------
    plotly.graph_objects.Figure
        The upset plot figure
    """
    if category_colors:
        generator = ColoredUpsetPlotGenerator(
            df, categories_dict, category_colors=category_colors
        )
    else:
        generator = UpsetPlotGenerator(df, categories_dict)

    # compute_combinations is now called automatically inside plot() if needed
    return generator.plot(
        title=title,
        bar_color=bar_color,
        active_color=active_color,
        inactive_color=inactive_color,
        connection_color=connection_color,
        height=height,
        combinations_range=combinations_range,
        min_sets=min_sets,
    )
