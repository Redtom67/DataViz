import streamlit as st
import pandas as pd

import plotly.express as px

# Charger les données
@st.cache_data
def load_data():
    return pd.read_csv('./data/df_dataset.csv')

df = load_data()

# Titre de l'application
st.title("La Route de la Sécurité : Les Facteurs et les Victimes des Accidents en France")

# Partie 1 : Le Bilan Global
st.header("Partie 1 : Le Bilan Global")
st.subheader("Évolution annuelle des accidents mortels et blessés")


# Graphe des accidents sur toute l'année divisés par jour de l'année
if 'jour' in df.columns and 'col' in df.columns:
    accidents_par_jour_annee = df.groupby(['jour', 'col']).size().reset_index(name='count')
    fig_yearly = px.bar(accidents_par_jour_annee, x='jour', y='count', color='col',
                        title="Répartition des accidents par jour de l'année")
    st.plotly_chart(fig_yearly)
else:
    st.error("Les colonnes nécessaires pour cette analyse sont manquantes.")

# Partie 2 : Qui sont les victimes ?
st.header("Partie 2 : Qui sont les victimes ?")
st.subheader("Usagers vulnérables et jeunes conducteurs")

# Filtrer les données pour les usagers vulnérables et jeunes conducteurs
if 'categorie_usager' in df.columns and 'age' in df.columns and 'lieu' in df.columns:
    usagers_vulnerables = df[df['categorie_usager'].isin(['piéton', 'cycliste'])]
    jeunes_conducteurs = df[df['age'] < 25]

    st.write("Accidents impliquant des usagers vulnérables (piétons, cyclistes) :")
    fig2 = px.histogram(usagers_vulnerables, x='lieu', color='categorie_usager',
                        title="Répartition des accidents par lieu pour les usagers vulnérables")
    st.plotly_chart(fig2)

    st.write("Accidents impliquant des jeunes conducteurs :")
    fig3 = px.histogram(jeunes_conducteurs, x='lieu', title="Répartition des accidents par lieu pour les jeunes conducteurs")
    st.plotly_chart(fig3)
else:
    st.error("Les colonnes nécessaires pour cette analyse sont manquantes.")

# Partie 3 : Où et Pourquoi ?
st.header("Partie 3 : Où et Pourquoi ?")
st.subheader("Cartographie des accidents mortels et analyse des facteurs")

# Cartographier les accidents mortels
if 'latitude' in df.columns and 'longitude' in df.columns and 'gravite' in df.columns:
    accidents_mortels = df[df['gravite'] == 'mortel']
    st.map(accidents_mortels[['latitude', 'longitude']])
else:
    st.error("Les colonnes nécessaires pour la cartographie sont manquantes.")

# Analyser les facteurs environnementaux et routiers
if 'facteur_environnement' in df.columns and 'type_route' in df.columns:
    facteurs = df.groupby(['facteur_environnement', 'type_route']).size().reset_index(name='count')
    fig4 = px.bar(facteurs, x='facteur_environnement', y='count', color='type_route',
                  title="Facteurs environnementaux et routiers les plus souvent en cause")
    st.plotly_chart(fig4)
else:
    st.error("Les colonnes nécessaires pour cette analyse sont manquantes.")