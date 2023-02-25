import streamlit as st


st.set_page_config(
    page_title="Accueil",
    page_icon=":house:",
)
css = """

<style>
        p{
            text-align:justify;
        }
        .css-10trblm.e16nr0p30{
            text-align:center;
            padding:20px;
        }
        .name-link{
            
            margin: 0 1em;
        }
        .title{
            text-align: none !important;
        }
        
    </style>

"""
st.markdown(css, unsafe_allow_html=True)

st.write("# Bienvenue sur notre Data app 👋")

st.image("img/NMwasUPmRFzY3ayztk55yS.jpeg")

st.header("Notre projet en quelques mots : ")
st.write(
    """Le domaine de l'aérospatiale est en constante évolution, et la réussite d'un projet dans ce domaine repose sur une planification minutieuse et une exécution précise. L'un des aspects cruciaux d'un projet de lancement spatial est l'établissement de la chronologie de vol, qui permet de déterminer les moments clés du vol, ainsi que les points critiques à surveiller pendant le décollage et le vol.

Dans le cadre de ce projet, l'établissement de la chronologie de vol sera accompagné de la création d'un schéma 2D/3D du lanceur. Cela permettra de visualiser le lancement de manière détaillée, ce qui facilitera la planification et l'exécution du projet.

Afin de prédire avec précision les propriétés aérodynamiques du lanceur, des méthodes rapides de prévision seront sélectionnées et mises en œuvre. Ces méthodes sont nécessaires pour obtenir des résultats rapidement et efficacement, ce qui est crucial dans un projet de lancement spatial où les délais sont très serrés.

Une fois la prévision des propriétés aérodynamiques réalisée, il sera nécessaire de caractériser l'écoulement et ses propriétés aérodynamiques pour les points de vol retenus. Cette caractérisation impliquera la réalisation de tracés de l'évolution de grandeurs physiques pertinentes, ainsi qu'une analyse critique des résultats obtenus. Ces analyses permettront de comprendre les comportements de l'écoulement autour du lanceur, ce qui aidera à améliorer la conception et l'exécution du projet.

En somme, ce projet implique des étapes cruciales pour la planification et l'exécution d'un lancement spatial réussi. L'utilisation de méthodes rapides de prévision des propriétés aérodynamiques et la caractérisation de l'écoulement sont deux aspects clés de ce projet, qui permettront d'améliorer la compréhension du comportement du lanceur et d'optimiser la conception pour un vol réussi."""
)

st.markdown(
    """    
   <p>Réalisé par : <a href="https://www.linkedin.com/in/arthur-r%C3%A9villion/" class="name-link">Arthur Révillion</a><a class="name-link" href="https://www.linkedin.com/in/hugo-pouteil-noble-003630222/">Hugo Pouteil-noble</a> <a class="name-link" href="https://www.linkedin.com/in/julien-nigou-7a277621a/">Julien Nigou</a></p>

"""
,unsafe_allow_html=True)