#!/usr/bin/env python3
"""
Matplotlib Bar Chart with Error Bars Example

This script demonstrates how to create a bar chart with error bars using matplotlib.
Error bars are useful for showing uncertainty, variability, or confidence intervals in data.
"""

import matplotlib.pyplot as plt
import numpy as np

# Sample data: Performance metrics for different algorithms
categories = ["Prompt 1", "Prompt 2", "Prompt 2 + Regras 1"]

# Mean values (e.g., average accuracy or performance scores)
mean_values = [85, 78, 92]

# Error values (e.g., standard deviation or confidence intervals)
# These represent the uncertainty or variability in the measurements
error_values = [5, 7, 4]

# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

# Create bar chart with error bars
# Scientific paper style: grayscale colors, patterns, and clear contrast
# yerr: adds vertical error bars
# capsize: adds horizontal caps at the end of error bars
# edgecolor: black border for better definition in B&W
# linewidth: border thickness
# error_kw: dictionary of error bar properties (color, linewidth, capthick)
bars = ax.bar(
    categories,
    mean_values,
    yerr=error_values,
    capsize=8,
    color="white",
    edgecolor="black",
    linewidth=1.5,
    error_kw={"ecolor": "black", "linewidth": 1.5, "capthick": 1.5},
)

# Add hatching pattern to bars for better distinction in B&W printing
for i, bar in enumerate(bars):
    # Different hatch patterns for visual distinction
    patterns = ["///", "\\\\\\", "|||", "---", "+++"]
    bar.set_hatch(patterns[i % len(patterns)])

# Customize the chart with scientific paper styling
ax.set_xlabel("Algorithms", fontsize=11)
ax.set_ylabel("Performance Score (%)", fontsize=11)
# ax.set_title('Algorithm Performance Comparison with Error Bars',
#  fontsize=12, pad=15)

# Add grid for better readability (subtle for scientific papers)
ax.grid(axis="y", alpha=0.4, linestyle=":", linewidth=0.8, color="gray")
ax.set_axisbelow(True)  # Place grid behind bars

# Remove top and right spines for cleaner look (common in scientific papers)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Set y-axis limits with some padding
ax.set_ylim(0, 110)

# Add value labels on top of each bar
for i, (bar, mean, error) in enumerate(zip(bars, mean_values, error_values)):
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2.0,
        height + error + 2,
        f"{mean}±{error}",
        ha="center",
        va="bottom",
        fontsize=10,
        fontweight="bold",
    )

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Display the chart
plt.show()

# Optional: Save the figure to a file
# Uncomment the line below to save the chart as a PNG file
# plt.savefig('bar_chart_with_error_bars.png', dpi=300, bbox_inches='tight')

print("Bar chart with error bars created successfully!")
print(f"Categories: {categories}")
print(f"Mean values: {mean_values}")
print(f"Error values: {error_values}")

# Made with Bob
