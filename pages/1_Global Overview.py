import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Global Overview", page_icon="📊", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv('./data/df_dataset.csv')

df = load_data()

st.title("Part 1: Global Overview")

# Global statistics with color coding
# Calculate global statistics
total_accidents = len(df)
total_deaths = len(df[df['grav'] == 2])
total_hospitalized = len(df[df['grav'] == 3])
total_minor = len(df[df['grav'] == 4])

# Display global overview with color coding
col1, col2, col3, col4 = st.columns(4)

# Define colors for severity
gravite_colors = {
    'Unharmed': '#2ecc71',        # Green
    'Killed': '#e74c3c',          # Red
    'Hospitalized injured': '#e67e22',  # Orange
    'Minor injuries': '#3498db'   # Blue
}

with col1:
    st.markdown(f"""
    <div style='background-color: {gravite_colors.get('Killed', '#e74c3c')}; padding: 20px; border-radius: 10px; text-align: center;'>
        <h3 style='color: white; margin: 0;'>Deaths</h3>
        <h1 style='color: white; margin: 10px 0;'>{total_deaths:,}</h1>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style='background-color: {gravite_colors.get('Hospitalized injured', '#e67e22')}; padding: 20px; border-radius: 10px; text-align: center;'>
        <h3 style='color: white; margin: 0;'>Hospitalized injured</h3>
        <h1 style='color: white; margin: 10px 0;'>{total_hospitalized:,}</h1>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style='background-color: {gravite_colors.get('Minor injuries', '#f39c12')}; padding: 20px; border-radius: 10px; text-align: center;'>
        <h3 style='color: white; margin: 0;'>Minor injuries</h3>
        <h1 style='color: white; margin: 10px 0;'>{total_minor:,}</h1>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style='background-color: #34495e; padding: 20px; border-radius: 10px; text-align: center;'>
        <h3 style='color: white; margin: 0;'>Total accidents</h3>
        <h1 style='color: white; margin: 10px 0;'>{total_accidents:,}</h1>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.subheader("Annual evolution of fatal and injury accidents")

# Graph of accidents by day over the year 2024
# According to PDF: 'jour' is day of month (1-31), 'mois' is month (1-12), 'an' is year
# 'grav' is accident severity
if 'jour' in df.columns and 'mois' in df.columns and 'grav' in df.columns and 'an' in df.columns:
    # Filter only 2024 data
    df_2024 = df[df['an'] == 2024].copy()
    st.write("Number of rows for 2024:", len(df_2024))
    
    if len(df_2024) > 0:
        # Create complete date column
        df_2024['date'] = pd.to_datetime(df_2024[['an', 'mois', 'jour']].rename(columns={'an': 'year', 'mois': 'month', 'jour': 'day'}), errors='coerce')
        
        # Map severity codes to their labels
        gravite_labels = {
            1: 'Unharmed',
            2: 'Killed',
            3: 'Hospitalized injured',
            4: 'Minor injuries'
        }
        
        # Get unique severities
        gravites_disponibles = sorted(df_2024['grav'].unique())
        
        # Multi-select for severities with labels
        gravites_selectionnees = st.multiselect(
            "Select severities to display:",
            options=gravites_disponibles,
            default=gravites_disponibles,
            format_func=lambda x: f"{x} - {gravite_labels.get(x, 'Unknown')}",
            help="1=Unharmed, 2=Killed, 3=Hospitalized injured, 4=Minor injuries"
        )
        
        if gravites_selectionnees:
            # Filter according to selected severities
            df_filtre = df_2024[df_2024['grav'].isin(gravites_selectionnees)]
            
            # Map codes in data for graph
            df_filtre['gravite_label'] = df_filtre['grav'].map(gravite_labels)
            
            # Count accidents per day and severity
            accidents_par_jour = df_filtre.groupby(['date', 'gravite_label']).size().reset_index(name='count')
            
            fig_yearly = px.line(accidents_par_jour, x='date', y='count', color='gravite_label',
                                color_discrete_map=gravite_colors,
                                title="Number of accidents per day in 2024 by severity",
                                labels={'date': 'Date', 'count': 'Number of accidents', 'gravite_label': 'Severity'})
            st.plotly_chart(fig_yearly)
        else:
            st.warning("Please select at least one severity to display")
    else:
        st.warning("No data available for year 2024")
else:
    st.error("Required columns for this analysis are missing.")

st.markdown("""
The country sees a high number of accidents every day, usually falling between 100 and 
            600 total accidents. The total number of incidents for the year 2024 is 243,030.
""")

st.markdown("---")

# Interactive map with severity filter
st.subheader("Interactive accident map")

if 'lat' in df.columns and 'long' in df.columns and 'grav' in df.columns:
    # Map severity codes
    gravite_labels_carte = {
        1: 'Unharmed',
        2: 'Killed',
        3: 'Hospitalized injured',
        4: 'Minor injuries'
    }
    
    # Severity filter
    gravites_carte = st.multiselect(
        "Select severities to display on map:",
        options=sorted(df['grav'].unique()),
        default=sorted(df['grav'].unique()),
        format_func=lambda x: f"{x} - {gravite_labels_carte.get(x, 'Unknown')}",
        key="carte_gravite"
    )
    
    if gravites_carte:
        # Filter data
        df_carte = df[df['grav'].isin(gravites_carte)].copy()
        
        # Try to clean and convert coordinates
        # Replace commas with dots if necessary
        if df_carte['lat'].dtype == 'object':
            df_carte['lat'] = df_carte['lat'].astype(str).str.replace(',', '.')
        if df_carte['long'].dtype == 'object':
            df_carte['long'] = df_carte['long'].astype(str).str.replace(',', '.')
        
        # Convert to numeric
        df_carte['lat'] = pd.to_numeric(df_carte['lat'], errors='coerce')
        df_carte['long'] = pd.to_numeric(df_carte['long'], errors='coerce')
        
        # Filter valid coordinates (metropolitan France approximately)
        # Latitude: 41 to 51, Longitude: -5 to 10
        df_carte = df_carte[
            (df_carte['lat'].between(41, 51)) & 
            (df_carte['long'].between(-5, 10))
        ]
        
        st.write(f"Number of valid coordinates found: {len(df_carte)}")
        
        # Check if data remains
        if len(df_carte) == 0:
            st.warning("No valid geographic coordinates found in the data. The 'lat' and 'long' columns may be empty "
            "or in an incorrect format.")
        else:
            # Limit to 5000 points for performance
            if len(df_carte) > 10000:
                df_carte = df_carte.sample(10000)
                st.info("Displaying a sample of 10000 accidents to optimize performance")
            
            # Map severity
            df_carte['gravite_label'] = df_carte['grav'].map(gravite_labels_carte)
            
            # Create map with Plotly
            fig_map = px.scatter_mapbox(df_carte,
                                         lat='lat',
                                         lon='long',
                                         color='gravite_label',
                                         color_discrete_map={
                                             'Unharmed': '#2ecc71',
                                             'Killed': '#e74c3c',
                                             'Hospitalized injured': '#e67e22',
                                             'Minor injuries': '#f39c12'
                                         },
                                         hover_data=['grav', 'dep'],
                                         zoom=5,
                                         height=600,
                                         title="Accident location by severity")
            
            fig_map.update_layout(mapbox_style="open-street-map")
            st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning("Please select at least one severity")
else:
    st.error("Columns 'lat', 'long' or 'grav' are not available.")

st.markdown("""
Accidents are spread out across the region, but they are clearly clumped together in and around 
big cities like Paris, Bordeaux, and Rennes. The map shows that accident problems are concentrated in highly populated areas.""")

st.markdown("---")