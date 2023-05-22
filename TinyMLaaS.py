import streamlit as st
import pandas as pd
import plotly.express as px

st.write(":red[This page does not contain any use, everything is hard coded]")

device_locations = pd.DataFrame({
    'device_id': ['device1', 'device2', 'device3', 'device4'],
    'latitude': [60.203978, 60.208609, 60.207861, 60.201926],
    'longitude': [24.961129, 24.966743, 24.965956, 24.968977],
    'last_update': ['2022-03-01 12:30:00', '2022-03-01 14:45:00', '2022-03-01 13:00:00', '2022-03-01 11:00:00']
})
num_registered = 4
num_connected = 3
num_transactions = 1000
total_hours = 5000

st.title("TinyMLaaS Overview")
st.subheader("Alert Panel")

low_battery_devices = ["device1", "device3"]
if low_battery_devices:
    st.warning("Warning: The following devices have low battery: " +
               ", ".join(low_battery_devices))

poor_connectivity_devices = ["device2"]
if poor_connectivity_devices:
    st.warning("Warning: The following devices have poor connectivity: " +
               ", ".join(poor_connectivity_devices))

unresponsive_devices = ["device4"]
if unresponsive_devices:
    st.error("Error: The following devices are unresponsive: " +
             ", ".join(unresponsive_devices))

if not (low_battery_devices or poor_connectivity_devices or unresponsive_devices):
    st.write("No alerts at the moment.")


st.subheader("Device Location Map")

device_locations_24h = device_locations[device_locations['last_update']
                                        > '2022-02-28 00:00:00']
fig = px.scatter_mapbox(device_locations_24h, lat="latitude", lon="longitude", hover_name="device_id",
                        zoom=14, height=400, size_max=15, color_discrete_sequence=['red'])

fig.update_layout(mapbox_style="stamen-toner",
                  margin={"r": 0, "t": 0, "l": 0, "b": 0})
st.plotly_chart(fig)

st.subheader("Statistical Data")
st.write("Number of registered devices:", num_registered)
st.write("Number of connected devices:", num_connected)
st.write("Number of data transactions:", num_transactions)
st.write("Total hours of whole connected devices:", total_hours)
