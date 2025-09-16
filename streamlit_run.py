# ---
# lambda-test: false  # auxiliary-file
# ---
# ## Demo Streamlit application.
#
# This application is the example from https://docs.streamlit.io/library/get-started/create-an-app.
#
# Streamlit is designed to run its apps as Python scripts, not functions, so we separate the Streamlit
# code into this module, away from the Modal application code.

def main():
    import os
    from dotenv import load_dotenv
    from supabase import create_client, Client

    import numpy as np
    import pandas as pd
    import streamlit as st
    import pydeck as pdk
    import folium
    from streamlit_folium import st_folium

   


    st.title("Uber pickups in NYC!")

    DATE_COLUMN = "date/time"
    DATA_URL = (
        "https://s3-us-west-2.amazonaws.com/"
        "streamlit-demo-data/uber-raw-data-sep14.csv.gz"
    )

    @st.cache_data
    def load_data(nrows):
        data = pd.read_csv(DATA_URL, nrows=nrows)

        def lowercase(x):
            return str(x).lower()

        data.rename(lowercase, axis="columns", inplace=True)
        data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
        return data

    data_load_state = st.text("Loading data...")
    data = load_data(10000)
    data_load_state.text("Done! (using st.cache_data)")

    if st.checkbox("Show raw data"):
        st.subheader("Raw data")
        st.write(data)

    st.subheader("Number of pickups by hour")
    hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
    st.bar_chart(hist_values)

    # Some number in the range 0-23
    hour_to_filter = st.slider("hour", 0, 23, 17)
    filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

    st.subheader("Map of all pickups at %s:00" % hour_to_filter)
    st.map(filtered_data)

    st.subheader("Pydeck map of pickups at %s:00" % hour_to_filter)

    if not filtered_data.empty:
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=filtered_data,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=100,
        )

        view_state = pdk.ViewState(
            latitude=filtered_data["lat"].mean(),
            longitude=filtered_data["lon"].mean(),
            zoom=11,
            pitch=50,
        )

        deck = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={"text": "Pickup at ({lat}, {lon})"},
        )

        st.pydeck_chart(deck, use_container_width=True)
    else:
        st.info("No data available for this hour to display on Pydeck chart.")

        st.subheader(f"Folium map of pickups at {hour_to_filter}:00")

    if not filtered_data.empty:
        # Calculate center of map as mean of lat/lon
        center_lat = filtered_data["lat"].mean()
        center_lon = filtered_data["lon"].mean()

        # Create Folium map centered on mean location
        m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

        # Add a marker for each pickup (you can customize popups/tooltips)
        for idx, row in filtered_data.iterrows():
            folium.CircleMarker(
                location=[row["lat"], row["lon"]],
                radius=3,
                color="red",
                fill=True,
                fill_opacity=0.6,
                popup=f"Pickup at {row['date/time']}",
            ).add_to(m)

        # Display map in Streamlit app, width can be adjusted
        map_data = st_folium(m, width=700, height=500)

        # Optional: Show info about last clicked point
        if map_data and map_data.get("last_clicked"):
            st.write("You clicked at:", map_data["last_clicked"])

    else:
        st.info("No pickups available for this hour to display on Folium map.")


    def get_client() -> Client:
        load_dotenv()
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if not url or not key:
            raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY in .env")
        return create_client(url, key)


    supabase = get_client()

    # Replace "your_table" with a real table in your Supabase project
    # For demo purposes: SELECT * LIMIT 5
    response = supabase.table("eagles_offense").select("*").limit(5).execute()

    # # response.data is a list of dict rows
    # print("Rows:")
    # for row in response.data:
    #     print(row)
# Display data in Streamlit
    st.subheader("Supabase Data (First 5 rows)")
    if response.data:
        st.write(pd.DataFrame(response.data))
    else:
        st.info("No data found in Supabase table.")
if __name__ == "__main__":
    main()