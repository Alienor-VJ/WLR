import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display
from scipy.stats import linregress
from matplotlib.patches import Arc
import math

WLR = 0.3
Wmin = 5
L_arc = 15
W_arc = Wmin + L_arc * WLR
radius = math.sqrt(L_arc ** 2 + W_arc ** 2)


def generate_data(H, alpha, VC):
    np.random.seed(0)
    L1 = np.linspace(0, 200, 100)
    W1 = Wmin + L1 * WLR
    WCSA = np.pi * W1 * (W1 + L1)
    L2 = (100 - VC) / 100 * (L1 - alpha * H)
    W2 = np.sqrt(L2 ** 2 / 4 + WCSA / np.pi) - L2 / 2 + (1 - alpha) * H
    L1 = L1 + np.random.normal(scale=2, size=L1.shape)
    W1 = W1 + np.random.normal(scale=2, size=L1.shape)
    WCSA = WCSA + np.random.normal(scale=2, size=L1.shape)
    L2 = L2 + np.random.normal(scale=2, size=L1.shape)
    W2 = W2 + np.random.normal(scale=2, size=L1.shape)
    return L1, W1, L2, W2


def plot_scatter(H, alpha, VC, hypertrophia_checkbox, vasoconstriction_checkbox):
    L1, W1, L2, W2 = generate_data(H, alpha, VC)

    # Filter data to start from L = 20 (but we will plot the trend line from 0 to 20)
    L1_filtered, W1_filtered = L1[L1 >= 20], W1[L1 >= 20]
    L2_filtered, W2_filtered = L2[L1 >= 20], W2[L1 >= 20]

    # Fit trend lines
    slope1, intercept1, _, _, _ = linregress(L1, W1)
    slope2, intercept2, _, _, _ = linregress(L2, W2)

    # Create the plot
    plt.figure(figsize=(10, 6))

    # Trend line 1 (from 0 to 20, but no data points between)
    L1_trend = np.linspace(0, 20, 100)
    plt.plot(L1_trend, slope1 * L1_trend + intercept1, color='green', linestyle='dashed')

    # Trend line 1 (from 20 to 100, solid line)
    L1_trend_cont = np.linspace(20, 100, 100)
    plt.plot(L1_trend_cont, slope1 * L1_trend_cont + intercept1, color='green', linestyle='solid')

    # Scatter plot 1 (data points from 20 onward)
    plt.scatter(L1_filtered, W1_filtered, color='green', label='Normal')

    # Trend line 2 (from 0 to 20, but no data points between)
    L2_trend = np.linspace(0, 20, 100)
    plt.plot(L2_trend, slope2 * L2_trend + intercept2, color='red', linestyle='dashed')

    # Trend line 2 (from 20 to 100, solid line)
    L2_trend_cont = np.linspace(20, 100, 100)
    plt.plot(L2_trend_cont, slope2 * L2_trend_cont + intercept2, color='red', linestyle='solid')

    # Scatter plot 2 (data points from 20 onward)
    if hypertrophia_checkbox and vasoconstriction_checkbox:
        label_data_2 = 'Hypertrophia + Vasoconstriction'
        plt.scatter(L2_filtered, W2_filtered, color='red', label=label_data_2)
    elif hypertrophia_checkbox:
        label_data_2 = 'Hypertrophia'
        plt.scatter(L2_filtered, W2_filtered, color='red', label=label_data_2)
    elif vasoconstriction_checkbox:
        label_data_2 = 'Vasoconstriction'
        plt.scatter(L2_filtered, W2_filtered, color='red', label=label_data_2)

    # Define points for the arc (around L = 15)
    y1 = slope1 * L_arc + intercept1  # y-coordinate on the green line
    y2 = slope2 * L_arc + intercept2  # y-coordinate on the red line

    # Find the intersection of the two lines
    x_intersection = (intercept2 - intercept1) / (slope1 - slope2)
    y_intersection = slope1 * x_intersection + intercept1

    # Calculate the angle between the two lines at the intersection
    angle_start = np.arctan(slope1)  # Angle for the first trend line (green)
    angle_end = np.arctan(slope2)  # Angle for the second trend line (red)
    angle_diff = np.abs(angle_start - angle_end)  # Angle difference between the lines

    # Define the radius for the arc
    radius = 20  # You can adjust this based on your needs

    # Create an arc between the two trendlines at the intersection
    arc = Arc((x_intersection, y_intersection), 2 * radius, 2 * radius, angle=0,
              theta1=np.degrees(angle_start), theta2=np.degrees(angle_end),
              color='black', lw=2)
    plt.gca().add_patch(arc)

    # Add the label for the angle (ω)
    angle_deg = np.degrees(angle_diff)
    plt.text(20, 20, f'ω = {angle_deg:.2f}°', color='black', fontsize=12)

    # Draw double-ended arrow between the y-intercepts of the trend lines
    plt.annotate('', xy=(0, intercept1), xytext=(0, intercept2),
                 arrowprops=dict(arrowstyle='<->', color='black', lw=2))

    # Add label to show the distance
    distance = abs(intercept1 - intercept2)
    plt.text(2, (intercept1 + intercept2) / 2, f'H = {distance:.2f} um', color='black', fontsize=12)

    # Fix the axis limits
    plt.xlim(0, 100)
    plt.ylim(0, 60)

    # Titles and labels
    plt.title('W versus L (Combined Plot)')
    plt.xlabel('L (um)')
    plt.ylabel('W (um)')
    plt.legend()

    # Show the plot
    plt.show()


# Interactive widgets
H_widget = widgets.FloatSlider(min=0, max=20.0, step=0.5, value=0.0, description='Hypertrophia (H)')
alpha_widget = widgets.FloatSlider(min=0, max=1, step=0.05, value=0,
                                   description='Internal hypertrophia component Alpha (α)')
VC_widget = widgets.FloatSlider(min=0, max=100, step=1, value=0, description='Vasoconstriction (VC)')

# Checkbox widgets
hypertrophia_checkbox = widgets.Checkbox(value=False, description='Hypertrophia')
vasoconstriction_checkbox = widgets.Checkbox(value=False, description='Vasoconstriction')


# Function to update the widget's enabled state based on checkbox state
def update_widgets(change):
    H_widget.disabled = not hypertrophia_checkbox.value
    alpha_widget.disabled = not hypertrophia_checkbox.value
    VC_widget.disabled = not vasoconstriction_checkbox.value


# Observe the checkbox changes
hypertrophia_checkbox.observe(update_widgets, names='value')
vasoconstriction_checkbox.observe(update_widgets, names='value')

# Initial widget update based on default checkbox values
update_widgets(None)

# Layout with checkboxes below the legend
ui = widgets.VBox([
    H_widget, alpha_widget, VC_widget,
    hypertrophia_checkbox, vasoconstriction_checkbox
])
output = widgets.interactive_output(plot_scatter, {'H': H_widget, 'alpha': alpha_widget, 'VC': VC_widget,
                                                   'hypertrophia_checkbox': hypertrophia_checkbox,
                                                   'vasoconstriction_checkbox': vasoconstriction_checkbox})

display(ui, output)
