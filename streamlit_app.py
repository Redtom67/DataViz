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


# Graphe des accidents par jour sur l'année 2024
# Selon le PDF: 'jour' est le jour du mois (1-31), 'mois' est le mois (1-12), 'an' est l'année
# 'grav' est la gravité de l'accident avec les codes suivants:
# 1 = Indemne (non blessé)
# 2 = Tué
# 3 = Blessé hospitalisé
# 4 = Blessé léger

if 'jour' in df.columns and 'mois' in df.columns and 'grav' in df.columns and 'an' in df.columns:
    # Filtrer uniquement les données de 2024
    df_2024 = df[df['an'] == 2024].copy()
    
    if len(df_2024) > 0:
        # Créer une colonne date complète
        df_2024['date'] = pd.to_datetime(df_2024[['an', 'mois', 'jour']].rename(columns={'an': 'year', 'mois': 'month', 'jour': 'day'}), errors='coerce')
        
        # Mapper les codes de gravité vers leurs libellés
        gravite_labels = {
            1: 'Indemne',
            2: 'Tué',
            3: 'Blessé hospitalisé',
            4: 'Blessé léger'
        }

        # Définir les couleurs pour chaque gravité
        gravite_colors = {
            'Indemne': '#2ecc71',        # Vert
            'Tué': '#e74c3c',            # Rouge
            'Blessé hospitalisé': '#e67e22',  # Orange
            'Blessé léger': '#3498db'    # bleu
        }
        
        # Obtenir les gravités uniques
        gravites_disponibles = sorted(df_2024['grav'].unique())
        
        # Sélecteur multi-choix pour les gravités avec libellés
        gravites_selectionnees = st.multiselect(
            "Sélectionnez les gravités à afficher :",
            options=gravites_disponibles,
            default=gravites_disponibles,
            format_func=lambda x: f"{x} - {gravite_labels.get(x, 'Inconnu')}",
            help="1=Indemne, 2=Tué, 3=Blessé hospitalisé, 4=Blessé léger"
        )
        
        if gravites_selectionnees:
            # Filtrer selon les gravités sélectionnées
            df_filtre = df_2024[df_2024['grav'].isin(gravites_selectionnees)]
            
            # Mapper les codes dans les données pour le graphique
            df_filtre['gravite_label'] = df_filtre['grav'].map(gravite_labels)
            
            # Compter les accidents par jour et par gravité
            accidents_par_jour = df_filtre.groupby(['date', 'gravite_label']).size().reset_index(name='count')
            
            fig_yearly = px.line(accidents_par_jour, x='date', y='count', color='gravite_label',
                                color_discrete_map=gravite_colors,
                                title="Nombre d'accidents par jour en 2024 selon la gravité",
                                labels={'date': 'Date', 'count': 'Nombre d\'accidents', 'gravite_label': 'Gravité'})
            st.plotly_chart(fig_yearly)
        else:
            st.warning("Veuillez sélectionner au moins une gravité à afficher")
    else:
        st.warning("Aucune donnée disponible pour l'année 2024")
else:
    st.error("Les colonnes nécessaires pour cette analyse sont manquantes.")

# Calculer les statistiques globales
total_accidents = len(df)
total_morts = len(df[df['grav'] == 2])
total_blesses_hospitalises = len(df[df['grav'] == 3])
total_blesses_legers = len(df[df['grav'] == 4])

# Afficher le bilan global en chiffres
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total d'accidents", value=f"{total_accidents:,}")

with col2:
    st.metric(label="Morts", value=f"{total_morts:,}")

with col3:
    st.metric(label="Blessés hospitalisés", value=f"{total_blesses_hospitalises:,}")

with col4:
    st.metric(label="Blessés légers", value=f"{total_blesses_legers:,}")

st.markdown("---")

# Partie 2 : Qui sont les victimes ?
st.header("Partie 2 : Qui sont les victimes ?")
st.subheader("Usagers vulnérables et jeunes conducteurs")
# Graphe des usagers vulnérables
st.markdown("---")

# Graphes supplémentaires pour la Partie 2

# Graphe 1 : Répartition par tranches d'âge
st.subheader("Répartition des accidents par tranche d'âge")

if 'age' in df.columns:
    # Définir les tranches d'âge
    bins = [10, 20, 30, 40, 50, 60, 70, 80, 120]
    labels = ['10-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-120']
    
    # Créer une colonne pour les tranches d'âge
    df['tranche_age'] = pd.cut(df['age'], bins=bins, labels=labels, include_lowest=True)
    
    # Compter les accidents par tranche d'âge
    accidents_par_age = df['tranche_age'].value_counts().sort_index().reset_index()
    accidents_par_age.columns = ['tranche_age', 'count']
    
    fig_age = px.bar(accidents_par_age, x='tranche_age', y='count',
                        title="Nombre d'accidents par tranche d'âge",
                        labels={'tranche_age': 'Tranche d\'âge', 'count': 'Nombre d\'accidents'},
                        color='count',
                        color_continuous_scale='Blues')
    st.plotly_chart(fig_age)
else:
    st.error("La colonne 'age' n'est pas disponible.")

# Graphe 2 : Répartition par catégorie de véhicule
st.subheader("Répartition des accidents par catégorie de véhicule")

if 'catv' in df.columns:
    # Mapper les codes catv selon le PDF
    catv_labels = {
        1: 'Bicyclette',
        2: 'Cyclomoteur <50cm3',
        3: 'Voiturette',
        4: 'Scooter immatriculé (SIV)',
        5: 'Motocyclette',
        6: 'Side-car',
        7: 'VL (Véhicule Léger, PTAC <= 3,5T) seul',
        10: 'VU (Véhicule Utilitaire) seul (1,5T <= PTAC <= 3,5T)',
        13: 'PL seul 3,5T <PTCA <= 7,5T',
        14: 'PL seul > 7,5T',
        15: 'PL > 3,5T + remorque',
        16: 'Tracteur routier seul',
        17: 'Tracteur routier + semi-remorque',
        20: 'Engin spécial',
        21: 'Tracteur agricole',
        30: 'Scooter < 50 cm3',
        31: 'Motocyclette > 50 cm3 et <= 125 cm3',
        32: 'Scooter > 50 cm3 et <= 125 cm3',
        33: 'Motocyclette > 125 cm3',
        34: 'Scooter > 125 cm3',
        35: 'Quad léger <= 50 cm3',
        36: 'Quad lourd > 50 cm3',
        37: 'Autobus',
        38: 'Autocar',
        39: 'Train',
        40: 'Tramway',
        99: 'Autre véhicule'
    }
    
    # Compter les accidents par catégorie et prendre le top 10
    accidents_par_catv = df['catv'].value_counts().head(5).reset_index()
    accidents_par_catv.columns = ['catv', 'count']
    
    # Mapper les codes vers leurs libellés
    accidents_par_catv['catv_label'] = accidents_par_catv['catv'].map(catv_labels)
    
    # Créer le graphique
    fig_catv = px.bar(accidents_par_catv, 
                      x='catv_label', 
                      y='count',
                      title="Top 10 des catégories de véhicules impliqués dans des accidents",
                      labels={'catv_label': 'Catégorie de véhicule', 'count': 'Nombre d\'accidents'},
                      color='count',
                      color_continuous_scale='Reds')
    
    # Rotation des labels pour meilleure lisibilité
    fig_catv.update_layout(xaxis_tickangle=-45)
    
    st.plotly_chart(fig_catv)
else:
    st.error("La colonne 'catv' n'est pas disponible.")

# Graphe 1 : Répartition par type de trajet
st.subheader("Répartition des accidents par type de trajet")

if 'trajet' in df.columns:
    # Mapper les codes trajet selon le PDF
    trajet_labels = {
        0: 'Non renseigné',
        1: 'Domicile – travail',
        2: 'Domicile – école',
        3: 'Courses – achats',
        4: 'Utilisation professionnelle',
        5: 'Promenade – loisirs',
        9: 'Autre'
    }
    
    # Compter les accidents par type de trajet
    accidents_par_trajet = df['trajet'].value_counts().reset_index()
    accidents_par_trajet.columns = ['trajet', 'count']
    
    # Mapper les codes vers leurs libellés
    accidents_par_trajet['trajet_label'] = accidents_par_trajet['trajet'].map(trajet_labels)
    
    # Créer le graphique
    fig_trajet = px.pie(accidents_par_trajet, 
                        names='trajet_label', 
                        values='count',
                        title="Répartition des accidents par type de trajet",
                        color_discrete_sequence=px.colors.qualitative.Set3)
    
    st.plotly_chart(fig_trajet)
else:
    st.error("La colonne 'trajet' n'est pas disponible.")

# Graphe 2 : Répartition par catégorie d'usager
st.subheader("Répartition des accidents par catégorie d'usager")

if 'catu' in df.columns:
    # Mapper les codes catu selon le PDF
    catu_labels = {
        1: 'Conducteur',
        2: 'Passager',
        3: 'Piéton',
        4: 'Piéton en roller ou trottinette'
    }
    
    # Compter les accidents par catégorie d'usager
    accidents_par_catu = df['catu'].value_counts().reset_index()
    accidents_par_catu.columns = ['catu', 'count']
    
    # Mapper les codes vers leurs libellés
    accidents_par_catu['catu_label'] = accidents_par_catu['catu'].map(catu_labels)
    
    # Créer le graphique
    fig_catu = px.bar(accidents_par_catu, 
                      x='catu_label', 
                      y='count',
                      title="Répartition des accidents par catégorie d'usager",
                      labels={'catu_label': 'Catégorie d\'usager', 'count': 'Nombre d\'accidents'},
                      color='count',
                      color_continuous_scale='Blues')
    
    st.plotly_chart(fig_catu)
else:
    st.error("La colonne 'catu' n'est pas disponible.")

# Graphe 3 : Répartition par place dans le véhicule
st.subheader("Répartition des accidents par place dans le véhicule")

if 'place' in df.columns:
    # Mapper les codes place selon le PDF
    place_labels = {
        1: '1. Avant gauche (conducteur)',
        2: '2. Avant droit',
        3: '3. Arrière droit',
        4: '4. Arrière gauche',
        5: '5. Arrière centre',
        6: '6. Arrière droit',
        7: '7. Passager latéral gauche',
        8: '8. Passager latéral droit',
        9: '9. Sur le véhicule',
        10: '10. Autre place'
    }
    
    # Compter les accidents par place
    accidents_par_place = df['place'].value_counts().head(5).reset_index()
    accidents_par_place.columns = ['place', 'count']
    
    # Mapper les codes vers leurs libellés
    accidents_par_place['place_label'] = accidents_par_place['place'].map(place_labels)
    
    # Créer le graphique
    fig_place = px.bar(accidents_par_place, 
                       x='place_label', 
                       y='count',
                       title="Top 10 des places dans le véhicule lors d'accidents",
                       labels={'place_label': 'Place dans le véhicule', 'count': 'Nombre d\'accidents'},
                       color='count',
                       color_continuous_scale='Greens')
    
    # Rotation des labels pour meilleure lisibilité
    fig_place.update_layout(xaxis_tickangle=-45)
    
    st.plotly_chart(fig_place)
else:
    st.error("La colonne 'place' n'est pas disponible.")

st.image("./images/place_vehicule.png", caption="Référence des places dans le véhicule", use_container_width=True)
st.markdown("---")

# Partie 3 : Où et Pourquoi ?
st.header("Partie 3 : Où et Pourquoi ?")

# Section 1 : Localisation et Cartographie
st.subheader("1. Localisation et Cartographie")

# Graphe 1.1 : Top 20 des départements avec le plus de tués
st.write("### Top 20 des départements avec le plus de tués")

if 'dep' in df.columns and 'grav' in df.columns:
    # Filtrer uniquement les tués (grav = 2)
    df_tues = df[df['grav'] == 2].copy()
    
    # Nettoyer la colonne dep (extraire les 2 premiers caractères si c'est une chaîne)
    df_tues['dep_clean'] = df_tues['dep'].astype(str).str[:2]
    
    # Compter les tués par département
    tues_par_dep = df_tues['dep_clean'].value_counts().head(20).reset_index()
    tues_par_dep.columns = ['dep', 'count']
    
    fig_dep = px.bar(tues_par_dep,
                     x='dep',
                     y='count',
                     title="Top 20 des départements avec le plus de tués",
                     labels={'dep': 'Département', 'count': 'Nombre de tués'},
                     color='count',
                     color_continuous_scale='Reds')
    
    st.plotly_chart(fig_dep)
else:
    st.error("Les colonnes 'dep' ou 'grav' ne sont pas disponibles.")

# Graphe 1.2 : Carte interactive avec filtre de gravité
st.write("### Carte interactive des accidents")

if 'lat' in df.columns and 'long' in df.columns and 'grav' in df.columns:
    # Mapper les codes de gravité
    gravite_labels_carte = {
        1: 'Indemne',
        2: 'Tué',
        3: 'Blessé hospitalisé',
        4: 'Blessé léger'
    }
    
    # Filtre de gravité
    gravites_carte = st.multiselect(
        "Sélectionnez les gravités à afficher sur la carte :",
        options=sorted(df['grav'].unique()),
        default=sorted(df['grav'].unique()),
        format_func=lambda x: f"{x} - {gravite_labels_carte.get(x, 'Inconnu')}",
        key="carte_gravite"
    )
    
    if gravites_carte:
        # Filtrer les données
        df_carte = df[df['grav'].isin(gravites_carte)].copy()
        
        # Essayer de nettoyer et convertir les coordonnées
        # Remplacer les virgules par des points si nécessaire
        if df_carte['lat'].dtype == 'object':
            df_carte['lat'] = df_carte['lat'].astype(str).str.replace(',', '.')
        if df_carte['long'].dtype == 'object':
            df_carte['long'] = df_carte['long'].astype(str).str.replace(',', '.')
        
        # Convertir en numérique
        df_carte['lat'] = pd.to_numeric(df_carte['lat'], errors='coerce')
        df_carte['long'] = pd.to_numeric(df_carte['long'], errors='coerce')
        
        # Filtrer les coordonnées valides (France métropolitaine approximativement)
        # Latitude: 41 à 51, Longitude: -5 à 10
        df_carte = df_carte[
            (df_carte['lat'].between(41, 51)) & 
            (df_carte['long'].between(-5, 10))
        ]
        
        st.write(f"Nombre de coordonnées valides trouvées : {len(df_carte)}")
        
        # Vérifier qu'il reste des données
        if len(df_carte) == 0:
            st.warning("Aucune coordonnée géographique valide trouvée dans les données. Les colonnes 'lat' et 'long' peuvent être vides ou dans un format incorrect.")
        else:
            # Limiter à 5000 points pour performance
            if len(df_carte) > 5000:
                df_carte = df_carte.sample(5000)
                st.info("Affichage d'un échantillon de 5000 accidents pour optimiser les performances")
            
            # Mapper la gravité
            df_carte['gravite_label'] = df_carte['grav'].map(gravite_labels_carte)
            
            # Créer la carte avec Plotly
            fig_map = px.scatter_mapbox(df_carte,
                                         lat='lat',
                                         lon='long',
                                         color='gravite_label',
                                         color_discrete_map={
                                             'Indemne': '#2ecc71',
                                             'Tué': '#e74c3c',
                                             'Blessé hospitalisé': '#e67e22',
                                             'Blessé léger': '#f39c12'
                                         },
                                         hover_data=['grav', 'dep'],
                                         zoom=5,
                                         height=600,
                                         title="Localisation des accidents par gravité")
            
            fig_map.update_layout(mapbox_style="open-street-map")
            st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning("Veuillez sélectionner au moins une gravité")
else:
    st.error("Les colonnes 'lat', 'long' ou 'grav' ne sont pas disponibles.")

st.markdown("---")

# Section 2 : Analyse des Facteurs Environnementaux et Contextuels
st.subheader("2. Analyse des Facteurs Environnementaux et Contextuels")

# Graphe 2.1 : Conditions Atmosphériques
st.write("### Répartition des accidents selon les conditions atmosphériques")

if 'atm' in df.columns:
    # Mapper les codes atm selon le PDF
    atm_labels = {
        -1: 'Non renseigné',
        1: 'Normale',
        2: 'Pluie légère',
        3: 'Pluie forte',
        4: 'Neige - grêle',
        5: 'Brouillard - fumée',
        6: 'Vent fort - tempête',
        7: 'Temps éblouissant',
        8: 'Temps couvert',
        9: 'Autre'
    }
    
    accidents_par_atm = df['atm'].value_counts().reset_index()
    accidents_par_atm.columns = ['atm', 'count']
    accidents_par_atm['atm_label'] = accidents_par_atm['atm'].map(atm_labels)
    
    fig_atm = px.bar(accidents_par_atm,
                     x='atm_label',
                     y='count',
                     title="Accidents selon les conditions atmosphériques",
                     labels={'atm_label': 'Condition atmosphérique', 'count': 'Nombre d\'accidents'},
                     color='count',
                     color_continuous_scale='Blues')
    
    fig_atm.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_atm)
else:
    st.error("La colonne 'atm' n'est pas disponible.")

# Graphe 2.4 : État de Surface
st.write("### Répartition des accidents selon l'état de la surface")

if 'surf' in df.columns:
    # Mapper les codes surf selon le PDF
    surf_labels = {
        -1: 'Non renseigné',
        1: 'Normale',
        2: 'Mouillée',
        3: 'Flaques',
        4: 'Inondée',
        5: 'Enneigée',
        6: 'Boue',
        7: 'Verglacée',
        8: 'Corps gras - huile',
        9: 'Autre'
    }
    
    accidents_par_surf = df['surf'].value_counts().reset_index()
    accidents_par_surf.columns = ['surf', 'count']
    accidents_par_surf['surf_label'] = accidents_par_surf['surf'].map(surf_labels)
    
    fig_surf = px.bar(accidents_par_surf,
                      x='surf_label',
                      y='count',
                      title="Accidents selon l'état de la surface",
                      labels={'surf_label': 'État de la surface', 'count': 'Nombre d\'accidents'},
                      color='count',
                      color_continuous_scale='Greens')
    
    fig_surf.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_surf)
else:
    st.error("La colonne 'surf' n'est pas disponible.")

# Graphe 2.3 : Vitesse et Type de Route pour accidents graves
st.write("### Analyse croisée : Vitesse maximale autorisée et Type de route (accidents graves)")

if 'vma' in df.columns and 'catr' in df.columns and 'grav' in df.columns:
    # Filtrer les accidents graves (tués et blessés hospitalisés)
    df_graves = df[df['grav'].isin([2, 3])].copy()
    
    # Convertir vma en numérique et filtrer <= 200 km/h
    df_graves['vma'] = pd.to_numeric(df_graves['vma'], errors='coerce')
    df_graves = df_graves[df_graves['vma'] <= 200]
    
    # Mapper les codes catr selon le PDF
    catr_labels = {
        1: 'Autoroute',
        2: 'Route nationale',
        3: 'Route départementale',
        4: 'Voie communale',
        5: 'Hors réseau public',
        6: 'Parc de stationnement',
        9: 'Autre'
    }
    
    df_graves['catr_label'] = df_graves['catr'].map(catr_labels)
    
    # Créer un graphique croisé
    accidents_vma_catr = df_graves.groupby(['vma', 'catr_label']).size().reset_index(name='count')
    
    fig_vma = px.bar(accidents_vma_catr,
                     x='vma',
                     y='count',
                     color='catr_label',
                     title="Accidents graves selon la vitesse maximale et le type de route (≤ 200 km/h)",
                     labels={'vma': 'Vitesse maximale autorisée (km/h)', 'count': 'Nombre d\'accidents', 'catr_label': 'Type de route'},
                     barmode='stack')
    
    # Limiter l'axe X à 200
    fig_vma.update_xaxes(range=[0, 150])
    
    st.plotly_chart(fig_vma)
else:
    st.error("Les colonnes 'vma', 'catr' ou 'grav' ne sont pas disponibles.")


# Graphe 2.2 : Conditions de Lumière
st.write("### Répartition des accidents selon les conditions de lumière")

if 'lum' in df.columns:
    # Mapper les codes lum selon le PDF
    lum_labels = {
        1: 'Plein jour',
        2: 'Crépuscule ou aube',
        3: 'Nuit sans éclairage public',
        4: 'Nuit avec éclairage public non allumé',
        5: 'Nuit avec éclairage public allumé'
    }
    
    accidents_par_lum = df['lum'].value_counts().reset_index()
    accidents_par_lum.columns = ['lum', 'count']
    accidents_par_lum['lum_label'] = accidents_par_lum['lum'].map(lum_labels)
    
    fig_lum = px.pie(accidents_par_lum,
                     names='lum_label',
                     values='count',
                     title="Répartition des accidents selon les conditions de lumière",
                     color_discrete_sequence=px.colors.sequential.RdBu)
    
    st.plotly_chart(fig_lum)
else:
    st.error("La colonne 'lum' n'est pas disponible.")

st.markdown("---")