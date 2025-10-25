import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="The Victims", page_icon="", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv('./data/df_dataset.csv')

df = load_data()

st.title("Part 2: Who are the victims?")
st.subheader("Vulnerable road users and young drivers")

# Graph of vulnerable users
st.markdown("---")

# Additional graphs for Part 2

# Graph 1: Distribution by age group
st.subheader("Distribution of accidents by age group")

if 'age' in df.columns:
    # Define age groups
    bins = [10, 20, 30, 40, 50, 60, 70, 80, 120]
    labels = ['10-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-120']
    
    # Create a column for age groups
    df['tranche_age'] = pd.cut(df['age'], bins=bins, labels=labels, include_lowest=True)
    
    # Count accidents by age group
    accidents_par_age = df['tranche_age'].value_counts().sort_index().reset_index()
    accidents_par_age.columns = ['tranche_age', 'count']
    
    fig_age = px.bar(accidents_par_age, x='tranche_age', y='count',
                        title="Number of accidents by age group",
                        labels={'tranche_age': 'Age group', 'count': 'Number of accidents'},
                        color='count',
                        color_continuous_scale='Blues')
    st.plotly_chart(fig_age)
else:
    st.error("The 'age' column is not available.")

st.markdown("The riskiest age range for accidents is the 21-30 group, with nearly 60,000 accidents. Involvement generally goes " \
"down as people get older, though the 31-40 and 41-50 groups are also heavily involved.")

# Graph 2: Distribution by vehicle category
st.subheader("Distribution of accidents by vehicle category")

if 'catv' in df.columns:
    # Map catv codes according to PDF
    catv_labels = {
        1: 'Bicycle',
        2: 'Moped <50cm3',
        3: 'Microcar',
        4: 'Registered scooter (SIV)',
        5: 'Motorcycle',
        6: 'Side-car',
        7: 'Light vehicle (GVWR <= 3.5T) alone',
        10: 'Utility vehicle alone (1.5T <= GVWR <= 3.5T)',
        13: 'Heavy goods vehicle alone 3.5T <GVWR <= 7.5T',
        14: 'Heavy goods vehicle alone > 7.5T',
        15: 'Heavy goods vehicle > 3.5T + trailer',
        16: 'Road tractor alone',
        17: 'Road tractor + semi-trailer',
        20: 'Special equipment',
        21: 'Agricultural tractor',
        30: 'Scooter < 50 cm3',
        31: 'Motorcycle > 50 cm3 and <= 125 cm3',
        32: 'Scooter > 50 cm3 and <= 125 cm3',
        33: 'Motorcycle > 125 cm3',
        34: 'Scooter > 125 cm3',
        35: 'Light quad <= 50 cm3',
        36: 'Heavy quad > 50 cm3',
        37: 'Bus',
        38: 'Coach',
        39: 'Train',
        40: 'Tram',
        99: 'Other vehicle'
    }
    
    # Count accidents by category and take top 5
    accidents_par_catv = df['catv'].value_counts().head(6).reset_index()
    accidents_par_catv.columns = ['catv', 'count']
    
    # Map codes to their labels
    accidents_par_catv['catv_label'] = accidents_par_catv['catv'].map(catv_labels)
    
    # Create the graph
    fig_catv = px.bar(accidents_par_catv, 
                      x='catv_label', 
                      y='count',
                      title="Top 5 vehicle categories involved in accidents",
                      labels={'catv_label': 'Vehicle category', 'count': 'Number of accidents'},
                      color='count',
                      color_continuous_scale='Reds')
    
    # Rotate labels for better readability
    fig_catv.update_layout(xaxis_tickangle=-45)
    
    st.plotly_chart(fig_catv)
else:
    st.error("The 'catv' column is not available.")

st.markdown("Ordinary Light vehicles (cars under 3.5T) are involved in by far the most accidents, over 150,000. All other vehicle " \
"types, such as utility vehicles, motorcycles, and bicycles, are involved much less frequently.")

# Graph 1: Distribution by trip type
st.subheader("Distribution of accidents by trip type")

if 'trajet' in df.columns:
    # Map trip codes according to PDF
    trajet_labels = {
        0: 'Not specified',
        1: 'Home - work',
        2: 'Home - school',
        3: 'Shopping - purchases',
        4: 'Professional use',
        5: 'Walk - leisure',
        9: 'Other'
    }
    
    # Count accidents by trip type
    accidents_par_trajet = df['trajet'].value_counts().reset_index()
    accidents_par_trajet.columns = ['trajet', 'count']
    
    # Map codes to their labels
    accidents_par_trajet['trajet_label'] = accidents_par_trajet['trajet'].map(trajet_labels)
    
    # Create the graph
    fig_trajet = px.pie(accidents_par_trajet, 
                        names='trajet_label', 
                        values='count',
                        title="Distribution of accidents by trip type",
                        color_discrete_sequence=px.colors.qualitative.Set3)
    
    st.plotly_chart(fig_trajet)
else:
    st.error("The 'trajet' column is not available.")

st.markdown("Nearly 30% of all accidents are linked to one specific trip : Walks-Leisure, this would point out the fact that we aren't"
"as receptive while driving for personnal reasons.")

# Graph 2: Distribution by user category
st.subheader("Distribution of accidents by user category")

if 'catu' in df.columns:
    # Map catu codes according to PDF
    catu_labels = {
        1: 'Driver',
        2: 'Passenger',
        3: 'Pedestrian',
        4: 'Pedestrian on rollerblades or scooter'
    }
    
    # Count accidents by user category
    accidents_par_catu = df['catu'].value_counts().reset_index()
    accidents_par_catu.columns = ['catu', 'count']
    
    # Map codes to their labels
    accidents_par_catu['catu_label'] = accidents_par_catu['catu'].map(catu_labels)
    
    # Create the graph
    fig_catu = px.bar(accidents_par_catu, 
                      x='catu_label', 
                      y='count',
                      title="Distribution of accidents by user category",
                      labels={'catu_label': 'User category', 'count': 'Number of accidents'},
                      color='count',
                      color_continuous_scale='Blues')
    
    st.plotly_chart(fig_catu)
else:
    st.error("The 'catu' column is not available.")

st.markdown("Drivers are by far the most involved in accidents, followed by passengers. Pedestrians and other vulnerable users ")

# Graph 3: Distribution by position in vehicle
st.subheader("Distribution of accidents by position in vehicle")

if 'place' in df.columns:
    # Map place codes according to PDF
    place_labels = {
        1: '1. Front left (driver)',
        2: '2. Front right',
        3: '3. Rear right',
        4: '4. Rear left',
        5: '5. Rear center',
        6: '6. Rear right',
        7: '7. Left side passenger',
        8: '8. Right side passenger',
        9: '9. On the vehicle',
        10: '10. Other position'
    }
    
    # Count accidents by position
    accidents_par_place = df['place'].value_counts().head(5).reset_index()
    accidents_par_place.columns = ['place', 'count']
    
    # Map codes to their labels
    accidents_par_place['place_label'] = accidents_par_place['place'].map(place_labels)
    
    # Create the graph
    fig_place = px.bar(accidents_par_place, 
                       x='place_label', 
                       y='count',
                       title="Top 10 positions in vehicle during accidents",
                       labels={'place_label': 'Position in vehicle', 'count': 'Number of accidents'},
                       color='count',
                       color_continuous_scale='Greens')
    
    # Rotate labels for better readability
    fig_place.update_layout(xaxis_tickangle=-45)
    
    st.plotly_chart(fig_place)
else:
    st.error("The 'place' column is not available.")

st.image("./images/place_vehicule.png", caption="Reference of positions in vehicle", use_container_width=True)

st.markdown("The driver position (front left) is by far the most involved in accidents, which "
"is logical since the driver is the one controlling the vehicle.")
st.markdown("---")


# Additional graph: Distribution of accidents by gender
st.subheader("Distribution of accidents by user gender")

if 'sexe' in df.columns:
    # Map gender codes according to PDF
    sexe_labels = {
        1: 'Male',
        2: 'Female'
    }
    
    # Count accidents by gender
    accidents_par_sexe = df['sexe'].value_counts().reset_index()
    accidents_par_sexe.columns = ['sexe', 'count']
    
    # Map codes to their labels
    accidents_par_sexe['sexe_label'] = accidents_par_sexe['sexe'].map(sexe_labels)
    
    # Create the histogram
    fig_sexe = px.bar(accidents_par_sexe,
                      x='sexe_label',
                      y='count',
                      title="Number of accidents by user gender",
                      labels={'sexe_label': 'Gender', 'count': 'Number of accidents'},
                      color='sexe_label',
                      color_discrete_map={'Male': '#3498db', 'Female': '#e74c3c'},
                      text='count')
    
    fig_sexe.update_traces(textposition='outside')
    fig_sexe.update_layout(showlegend=False)
    
    st.plotly_chart(fig_sexe)
    
    # Display percentages
    total = accidents_par_sexe['count'].sum()
    col1, col2 = st.columns(2)
    
    with col1:
        pct_masc = (accidents_par_sexe[accidents_par_sexe['sexe'] == 1]['count'].values[0] / total * 100) if 1 in accidents_par_sexe['sexe'].values else 0
        st.metric("Men", f"{pct_masc:.1f}%")
    
    with col2:
        pct_fem = (accidents_par_sexe[accidents_par_sexe['sexe'] == 2]['count'].values[0] / total * 100) if 2 in accidents_par_sexe['sexe'].values else 0
        st.metric("Women", f"{pct_fem:.1f}%")
else:
    st.error("The 'sexe' column is not available.")

st.markdown("Men are involved in double the quantity of accidents. This is useful to remind everyone that women are not the bad drivers")

st.markdown("---")