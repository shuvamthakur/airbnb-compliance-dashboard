import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Sydney Airbnb Compliance", layout="wide", page_icon="🏢")

# Title and Introduction
st.title("🏢 Sydney Airbnb Compliance Dashboard")
st.markdown("This tool allows local councils to filter out casual home-sharers and identify large-scale commercial 'mega-hosts' operating in priority zones. Adjust the filters on the left to uncover the data.")

# Load Data
@st.cache_data
def load_data():
    # Using low_memory=False to avoid DtypeWarnings
    df = pd.read_csv('listings_clean.csv', low_memory=False)
    
    # Clean up columns we need
    df['estimated_revenue_l365d'] = pd.to_numeric(df['estimated_revenue_l365d'], errors='coerce').fillna(0)
    df['estimated_occupancy_l365d'] = pd.to_numeric(df['estimated_occupancy_l365d'], errors='coerce').fillna(0)
    df['calculated_host_listings_count'] = pd.to_numeric(df['calculated_host_listings_count'], errors='coerce').fillna(1)
    
    # Create categories for filtering
    df['is_multi_host'] = df['calculated_host_listings_count'] > 1
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Could not find 'listings_clean.csv'. Please ensure the data file is in the same folder as this script.")
    st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔍 Filter Criteria")
st.sidebar.markdown("Use these filters to recreate the '726 Priority Listings' search from the story.")

# 1. Area (LGA)
all_lgas = sorted(df['lga'].dropna().unique().tolist())
selected_lgas = st.sidebar.multiselect("Select Area (LGA)", options=all_lgas, default=[])

# 2. Host Scale
host_scale = st.sidebar.radio(
    "Host Scale", 
    ["All Hosts", "Single-Listing (Mom & Pop)", "Multi-Listing (Commercial)"],
    index=2 # Default to Multi-listing as per the story
)

# 3. License Status
license_options = ["All", "Has License (PID-STRA)", "Exempt", "Missing/Unlicensed"]
selected_license = st.sidebar.selectbox("License Status", options=license_options, index=0)

# 4. Availability 
min_avail = st.sidebar.slider("Minimum Calendar Availability (Days)", 0, 365, 180)

# --- APPLY FILTERS ---
filtered_df = df.copy()

if selected_lgas:
    filtered_df = filtered_df[filtered_df['lga'].isin(selected_lgas)]

if host_scale == "Single-Listing (Mom & Pop)":
    filtered_df = filtered_df[~filtered_df['is_multi_host']]
elif host_scale == "Multi-Listing (Commercial)":
    filtered_df = filtered_df[filtered_df['is_multi_host']]

if selected_license == "Exempt":
    filtered_df = filtered_df[filtered_df['license'].astype(str).str.contains('Exempt', case=False, na=False)]
elif selected_license == "Missing/Unlicensed":
    filtered_df = filtered_df[filtered_df['license'].isna() | (filtered_df['license'].astype(str).str.strip() == '')]
elif selected_license == "Has License (PID-STRA)":
    filtered_df = filtered_df[filtered_df['license'].astype(str).str.contains('PID-STRA', case=False, na=False)]

filtered_df = filtered_df[filtered_df['availability_365'] >= min_avail]


# --- KPI METRICS ---
st.markdown("### 📊 High-Level Metrics")
col1, col2, col3, col4 = st.columns(4)

total_listings = len(filtered_df)
unique_hosts = filtered_df['host_id'].nunique()

# Calculate top 20 hosts concentration in this filtered view
if total_listings > 0:
    top_20_hosts_listings = filtered_df['host_id'].value_counts().head(20).sum()
    concentration_pct = (top_20_hosts_listings / total_listings) * 100
else:
    top_20_hosts_listings = 0
    concentration_pct = 0

col1.metric("Priority Listings Found", f"{total_listings:,}")
col2.metric("Unique Hosts", f"{unique_hosts:,}")
col3.metric("Listings controlled by Top 20 Hosts", f"{top_20_hosts_listings:,}")
col4.metric("Top 20 Concentration", f"{concentration_pct:.1f}%")

st.divider()

# --- MAIN VISUALS ---
col_map, col_data = st.columns([3, 2])

with col_map:
    st.markdown("### 📍 Commercial Clusters Map")
    st.markdown("Visualizing the geographic concentration of the filtered priority listings.")
    if total_listings > 0:
        map_data = filtered_df[['latitude', 'longitude']].dropna()
        st.map(map_data)
    else:
        st.warning("No listings match the current filters.")

with col_data:
    st.markdown("### 🏢 Top 20 Mega-Hosts to Audit")
    st.markdown("Starting compliance checks with these host IDs will cover the largest portion of the market.")
    if total_listings > 0:
        top_hosts = filtered_df['host_id'].value_counts().reset_index()
        top_hosts.columns = ['Host ID', 'Number of Listings']
        # Formatting Host ID as string so it doesn't get commas
        top_hosts['Host ID'] = top_hosts['Host ID'].astype(str)
        st.dataframe(top_hosts.head(20), use_container_width=True, hide_index=True)
    else:
        st.write("No data available.")
