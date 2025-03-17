import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from  streamlit_vertical_slider import vertical_slider

# Make display wider
st.set_page_config(
    layout="wide",
)

st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
                .scrollable-col {
                    max-height: 500px;
                    overflow-y: scroll;
                }
                .fixed-col {
                position: fixed;
                width: 20%;
                height: 100vh;
                overflow: hidden;
                z-index: 100;
            }
        </style>
        """, unsafe_allow_html=True)

# Load example CPT data
@st.cache_data
def load_data():
    df = pd.read_excel("training data/EnBW training data_rev3.1_filtered.xlsx")
    return df

raw_df = load_data()


st.sidebar.subheader("CPT Layer Interpretation Tool")

bh = st.sidebar.selectbox(
"Borehole",
raw_df["BH"].unique(),
)

df = raw_df[raw_df["BH"] == bh]

num_layers = st.sidebar.number_input("Number of layers:", min_value=1, max_value=10, value=3, step=1)

layers = []
for i in range(num_layers):
    # User input (e.g., depth range selection)
    depth = st.sidebar.slider(f"Layer {i+1}", 0.0, df["Depth (m)"].max(), 1.0, step=0.1, format="%0.1f", key=i)
    layers.append(depth)

@st.dialog("Input your name:")
def save_data():
    user_name = st.text_input("Enter your name:")
    if st.button("Submit"):
        if user_name:
            st.success(f"Data saved as ...")
        else:
            st.error("Please enter your name.")

# User clicks Save Button
if st.sidebar.button("Save Data"):
    save_data()


# static col
st.markdown('<div class="fixed-col">Fixed Column</div>', unsafe_allow_html=True)

params = ["Qt", "Fr", "Bq", "Ic"]

fig = make_subplots(
rows=1, cols=4,          # Number of rows and columns
shared_yaxes=True,       # Share x-axis for all subplots
vertical_spacing=0.1,    # Spacing between rows
subplot_titles=(params)  # Titles for each subplot
)

# Plot Ic zones
fig.add_shape(type="rect", x0=0, x1=1.31, y0=0, y1=df["Depth (m)"].max(), fillcolor="crimson", opacity=0.2,
                layer="below", row=1, col=4)
fig.add_shape(type="rect", x0=1.31, x1=2.05, y0=0, y1=df["Depth (m)"].max(), fillcolor="LightSkyBlue", opacity=0.2,
                layer="below", row=1, col=4)
fig.add_shape(type="rect", x0=2.05, x1=2.6, y0=0, y1=df["Depth (m)"].max(), fillcolor="limegreen", opacity=0.2,
                layer="below", row=1, col=4)
fig.add_shape(type="rect", x0=2.6, x1=2.95, y0=0, y1=df["Depth (m)"].max(), fillcolor="tomato", opacity=0.2,
                layer="below", row=1, col=4)
fig.add_shape(type="rect", x0=2.95, x1=3.6, y0=0, y1=df["Depth (m)"].max(), fillcolor="gold", opacity=0.2,
                layer="below", row=1, col=4)

# Plot data
fig.add_trace(go.Scatter(x=df['Qt'], y=df['Depth (m)'], name="Qt", marker=dict(size=20, color="CornflowerBlue")), row=1, col=1)
fig.add_trace(go.Scatter(x=df['Fr'], y=df['Depth (m)'], name="Fr", marker=dict(size=20, color="MediumSeaGreen")), row=1, col=2)
fig.add_trace(go.Scatter(x=df['Bq'], y=df['Depth (m)'], name="Bq", marker=dict(size=20, color="Slateblue")), row=1, col=3)
fig.add_trace(go.Scatter(x=df['Ic'], y=df['Depth (m)'], name="Ic", marker=dict(size=20, color="Goldenrod")), row=1, col=4)

# Plot layer boundaries
for col in range(4):
    for layer in layers:
        if params[col] == "Ic":
            xmax, xmin = 0, 3.6
        else:
            xmax, xmin = df[params[col]].min(), df[params[col]].max()
        fig.add_trace((go.Scatter(x=[xmin, xmax], y=[layer, layer], mode='lines',
                                            line=dict(color='red', width=1, dash="dash"))) , row=1, col=col+1)

fig.update_yaxes(autorange="reversed")  # Depth increases downward
fig.update_layout(width=1000, height=700, showlegend=False,
                  margin=dict(t=50))
st.plotly_chart(fig, use_container_width=True)
