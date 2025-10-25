import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Location & Factors", page_icon="🗺️", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv('./data/df_dataset.csv')

df = load_data()

# Part 3: Where and Why?
st.header("Part 3: Where and Why?")

# Section 1: Location and Mapping
st.subheader("1. Location and Mapping")

# Graph 1.1: Map of departments with most deaths
st.write("### Map of departments with most deaths")

if 'dep' in df.columns and 'grav' in df.columns:
    # Filter only deaths (grav = 2)
    df_tues = df[df['grav'] == 2].copy()
    
    # Clean dep column (extract first 2 characters if it's a string)
    df_tues['dep_clean'] = df_tues['dep'].astype(str).str[:2]
    
    # Count deaths by department
    tues_par_dep = df_tues['dep_clean'].value_counts().reset_index()
    tues_par_dep.columns = ['dep', 'count']
    
    # Approximate coordinates of French department centers
    dep_coords = {
        '75': [48.8566, 2.3522],   # Paris
        '69': [45.7640, 4.8357],   # Rhône
        '13': [43.2965, 5.3698],   # Bouches-du-Rhône
        '59': [50.6292, 3.0573],   # Nord
        '33': [44.8378, -0.5792],  # Gironde
        '44': [47.2184, -1.5536],  # Loire-Atlantique
        '06': [43.7102, 7.2620],   # Alpes-Maritimes
        '31': [43.6047, 1.4442],   # Haute-Garonne
        '92': [48.8921, 2.2200],   # Hauts-de-Seine
        '34': [43.6108, 3.8767],   # Hérault
        '62': [50.5177, 2.6347],   # Pas-de-Calais
        '93': [48.9362, 2.5180],   # Seine-Saint-Denis
        '91': [48.6313, 2.2852],   # Essonne
        '78': [48.8048, 2.1204],   # Yvelines
        '94': [48.7923, 2.4800],   # Val-de-Marne
        '95': [49.0389, 2.0900],   # Val-d'Oise
        '77': [48.6047, 2.9996],   # Seine-et-Marne
        '38': [45.1885, 5.7245],   # Isère
        '83': [43.1242, 6.0094],   # Var
        '67': [48.5734, 7.7521],   # Bas-Rhin
        '97': [16.2650, -61.5510],  # DOM-TOM
    }
    
    # Prepare data for graph
    map_data = []
    for idx, row in tues_par_dep.iterrows():
        dep_code = row['dep']
        count = row['count']
        
        if dep_code in dep_coords:
            coords = dep_coords[dep_code]
            map_data.append({
                'dep': dep_code,
                'lat': coords[0],
                'lon': coords[1],
                'count': count
            })
    
    df_map = pd.DataFrame(map_data)
    
    # Create map with orange-red gradient
    fig_3d = px.scatter_mapbox(df_map,
                                lat='lat',
                                lon='lon',
                                size='count',
                                color='count',
                                hover_name='dep',
                                hover_data={'lat': False, 'lon': False, 'count': True},
                                color_continuous_scale=['#FFA500', '#FF6B00', '#FF4500', '#FF0000', '#8B0000'],  # Orange to Dark Red
                                size_max=40,
                                zoom=4,
                                height=600,
                                title="Map of departments with most deaths")
    
    fig_3d.update_layout(
        mapbox_style="open-street-map",
        coloraxis_colorbar=dict(
            title="Number of deaths",
            tickvals=[df_map['count'].min(), df_map['count'].median(), df_map['count'].max()],
        )
    )
    
    st.plotly_chart(fig_3d, use_container_width=True)
    
else:
    st.error("Columns 'dep' or 'grav' are not available.")

st.markdown("---")

# Section 2: Analysis of Environmental and Contextual Factors
st.subheader("2. Analysis of Environmental and Contextual Factors")

# Graph 2.1: Atmospheric Conditions
st.write("### Accident distribution by atmospheric conditions")

if 'atm' in df.columns:
    # Map atm codes according to PDF
    atm_labels = {
        -1: 'Not specified',
        1: 'Normal',
        2: 'Light rain',
        3: 'Heavy rain',
        4: 'Snow - hail',
        5: 'Fog - smoke',
        6: 'Strong wind - storm',
        7: 'Dazzling weather',
        8: 'Overcast weather',
        9: 'Other'
    }
    
    accidents_par_atm = df['atm'].value_counts().reset_index()
    accidents_par_atm.columns = ['atm', 'count']
    accidents_par_atm['atm_label'] = accidents_par_atm['atm'].map(atm_labels)
    
    fig_atm = px.bar(accidents_par_atm,
                     x='atm_label',
                     y='count',
                     title="Accidents by atmospheric conditions",
                     labels={'atm_label': 'Atmospheric condition', 'count': 'Number of accidents'},
                     color='count',
                     color_continuous_scale='Blues')
    
    fig_atm.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_atm)
else:
    st.error("Column 'atm' is not available.")

st.markdown("Most accidents, over 150,000, happen in 'Normal' (good) weather conditions. "
"'Light rain' is the next most common weather condition for accidents. This is a bit suprising but "
"is useful to know for road safety measures. Additionally, adverse weather conditions like " \
"'Heavy rain', 'Snow - hail', and 'Fog - smoke', are associated with less accidents. This " \
"could prove that people are not drving safely when the conditions are optimal ")

# Graph 2.4: Surface Condition
st.write("### Accident distribution by surface condition")

if 'surf' in df.columns:
    # Map surf codes according to PDF
    surf_labels = {
        -1: 'Not specified',
        1: 'Normal',
        2: 'Wet',
        3: 'Puddles',
        4: 'Flooded',
        5: 'Snowy',
        6: 'Mud',
        7: 'Icy',
        8: 'Greasy - oil',
        9: 'Other'
    }
    
    accidents_par_surf = df['surf'].value_counts().reset_index()
    accidents_par_surf.columns = ['surf', 'count']
    accidents_par_surf['surf_label'] = accidents_par_surf['surf'].map(surf_labels)
    
    fig_surf = px.bar(accidents_par_surf,
                      x='surf_label',
                      y='count',
                      title="Accidents by surface condition",
                      labels={'surf_label': 'Surface condition', 'count': 'Number of accidents'},
                      color='count',
                      color_continuous_scale='Greens')
    
    fig_surf.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_surf)
else:
    st.error("Column 'surf' is not available.")

st.markdown("Similar to atmospheric conditions, most accidents occur on 'Normal' (dry) surfaces. ")

# Graph 2.2: Light Conditions
st.write("### Accident distribution by light conditions")

if 'lum' in df.columns:
    # Map lum codes according to PDF
    lum_labels = {
        1: 'Full daylight',
        2: 'Twilight or dawn',
        3: 'Night without public lighting',
        4: 'Night with public lighting not lit',
        5: 'Night with public lighting lit'
    }
    
    accidents_par_lum = df['lum'].value_counts().reset_index()
    accidents_par_lum.columns = ['lum', 'count']
    accidents_par_lum['lum_label'] = accidents_par_lum['lum'].map(lum_labels)
    
    fig_lum = px.pie(accidents_par_lum,
                     names='lum_label',
                     values='count',
                     title="Accident distribution by light conditions",
                     color_discrete_sequence=px.colors.sequential.RdBu)
    
    st.plotly_chart(fig_lum)
else:
    st.error("Column 'lum' is not available.")

st.markdown("The chart shows that 65.8% of accidents happen during the most frequent lighting condition (likely daylight)." \
" The second most frequent lighting condition accounts for 16.5% of accidents.")

# Graph 2.3: Speed and Road Type for serious accidents
st.write("### Cross analysis: Maximum authorized speed and Road type (serious accidents)")

if 'vma' in df.columns and 'catr' in df.columns and 'grav' in df.columns:
    # Filter serious accidents (deaths and hospitalized injured)
    df_graves = df[df['grav'].isin([2, 3])].copy()
    
    # Convert vma to numeric and filter <= 200 km/h
    df_graves['vma'] = pd.to_numeric(df_graves['vma'], errors='coerce')
    df_graves = df_graves[df_graves['vma'] <= 200]
    
    # Map catr codes according to PDF
    catr_labels = {
        1: 'Highway',
        2: 'National road',
        3: 'Departmental road',
        4: 'Communal road',
        5: 'Outside public network',
        6: 'Parking lot',
        9: 'Other'
    }
    
    df_graves['catr_label'] = df_graves['catr'].map(catr_labels)
    
    # Create cross graph
    accidents_vma_catr = df_graves.groupby(['vma', 'catr_label']).size().reset_index(name='count')
    
    fig_vma = px.bar(accidents_vma_catr,
                     x='vma',
                     y='count',
                     color='catr_label',
                     title="Serious accidents by maximum speed and road type (≤ 200 km/h)",
                     labels={'vma': 'Maximum authorized speed (km/h)', 'count': 'Number of accidents', 'catr_label': 'Road type'},
                     barmode='stack')
    
    # Limit X axis to 200
    fig_vma.update_xaxes(range=[0, 150])
    
    st.plotly_chart(fig_vma)
else:
    st.error("Columns 'vma', 'catr' or 'grav' are not available.")

st.markdown("The two biggest problem speeds for serious accidents are the " \
"50 km/h and 80 km/h limits, with both showing close to 10,000 or more serious incidents" )

st.markdown("---")