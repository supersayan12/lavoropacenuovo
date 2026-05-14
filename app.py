import streamlit as st
import folium
import requests
import polyline
from streamlit_folium import st_folium
from PIL import Image
import os

# ---------------------------------------------------
# CONFIG PAGINA
# ---------------------------------------------------

st.set_page_config(
    page_title="Monumenti della Memoria",
    page_icon="🕊️",
    layout="wide"
)

# ---------------------------------------------------
# CSS PERSONALIZZATO
# ---------------------------------------------------

st.markdown("""
<style>

/* SFONDO PRINCIPALE */
.main {
    background-color: var(--background-color);
}

/* TITOLI */
h1, h2, h3 {
    color: var(--text-color);
}

/* CARD */
.card {
    background-color: var(--secondary-background-color);
    color: var(--text-color);
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 20px;
    border: 1px solid rgba(128,128,128,0.15);
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: var(--secondary-background-color);
}

/* BOTTONI */
.stButton > button {
    background-color: var(--primary-color);
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
    transition: all 0.2s ease;
    font-weight: 600;
}

/* HOVER BOTTONI */
.stButton > button:hover {
    filter: brightness(1.1);
    transform: scale(1.02);
}

/* SELECTBOX */
.stSelectbox label {
    color: var(--text-color);
    font-weight: bold;
}

/* TESTO GENERALE */
p, li {
    color: var(--text-color);
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# DATI MONUMENTI
# ---------------------------------------------------

coordinate_monumenti = {
    "Monumento ai Partigiani": [9.6699656270115, 45.69479467330056],
    "Monumento ai Caduti in Cielo": [9.592063561703863, 45.524091321195705],
    "Monumento ai Cinque Martiri": [9.518603225152182, 45.52352438953796],
    "Binario 21": [9.208378942342174, 45.48826595076151],
    "Monumento alla Resistenza": [9.594868821115409, 45.52317780483042]
}

start = [9.592146713429965, 45.523298931107114]

descrizioni = {

    "Monumento ai Partigiani":
    "Realizzato da Giacomo Manzù e inaugurato nel 1977 a Bergamo in Piazza Matteotti. "
    "Questo monumento celebra la Resistenza e gli uomini e le donne che si opposero "
    "al nazifascismo per restituire all’Italia libertà e dignità.",

    "Monumento ai Caduti in Cielo":
    "Il Monumento ai Caduti in Cielo ricorda gli aviatori militari morti durante missioni "
    "di guerra e di servizio. È stato realizzato dall’Associazione Arma Aeronautica "
    "nel secondo dopoguerra (anni ’50). Il monumento si trova a Treviglio.",

    "Monumento ai Cinque Martiri":
    "Questo monumento commemora i cinque partigiani fucilati il 31 marzo 1945 "
    "in rappresaglia dai nazifascisti.",

    "Binario 21":
    "Dal Binario 21 della Stazione Centrale di Milano partirono treni diretti "
    "ai campi di sterminio durante la Shoah.",

    "Monumento alla Resistenza":
    "Monumento dedicato ai partigiani e ai cittadini che si opposero "
    "al nazifascismo."
}

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("🕊️ Monumenti")

pagina = st.sidebar.radio(
    "Navigazione",
    ["Home", "Lista Monumenti"]
)

st.sidebar.markdown("---")
st.sidebar.info("Progetto sulla memoria storica e la Resistenza")

# ---------------------------------------------------
# HOME
# ---------------------------------------------------

if pagina == "Home":

    st.title("🕊️ MONUMENTI DELLA MEMORIA")

    st.markdown("""
    <div class="card">
    Questo progetto racconta alcuni dei principali monumenti
    legati alla Resistenza, alla guerra e alla memoria storica.

    <br><br>

    Ogni luogo è accompagnato da:
    <ul>
        <li>descrizione storica</li>
        <li>immagini</li>
        <li>mappa interattiva</li>
        <li>percorso stradale</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    if os.path.exists("vittoriano-altare-della-patria.png"):
        image = Image.open("vittoriano-altare-della-patria.png")

        st.image(
            image,
            use_container_width=True,
            caption="Altare della Patria"
        )

# ---------------------------------------------------
# LISTA MONUMENTI
# ---------------------------------------------------

if pagina == "Lista Monumenti":

    st.title("📍 Lista Monumenti")

    monumento = st.selectbox(
        "Seleziona un monumento",
        list(coordinate_monumenti.keys())
    )

    end = coordinate_monumenti[monumento]

    # ---------------------------------------------------
    # LAYOUT A COLONNE
    # ---------------------------------------------------

    col1, col2 = st.columns([1, 1])

    # ---------------------------------------------------
    # COLONNA SINISTRA
    # ---------------------------------------------------

    with col1:

        st.markdown(f"""
        <div class="card">
        <h2>{monumento}</h2>
        <p>{descrizioni[monumento]}</p>
        </div>
        """, unsafe_allow_html=True)

        nome_file = monumento.lower().replace(" ", "_") + ".png"

        if os.path.exists(nome_file):
            image = Image.open(nome_file)

            st.image(
                image,
                use_container_width=True
            )

    # ---------------------------------------------------
    # COLONNA DESTRA
    # ---------------------------------------------------

    with col2:

        route_coords = []

        try:

            url = (
                f"http://router.project-osrm.org/route/v1/driving/"
                f"{start[0]},{start[1]};{end[0]},{end[1]}"
                f"?overview=full&geometries=polyline"
            )

            response = requests.get(url, timeout=5).json()

            route_coords = polyline.decode(
                response['routes'][0]['geometry']
            )

        except:
            st.warning("Percorso non disponibile")

        if route_coords:

            mappa = folium.Map(
                location=route_coords[0],
                zoom_start=12
            )

            folium.PolyLine(
                route_coords,
                color="red",
                weight=5
            ).add_to(mappa)

            folium.Marker(
                route_coords[0],
                popup="Partenza",
                icon=folium.Icon(color="green")
            ).add_to(mappa)

            folium.Marker(
                route_coords[-1],
                popup=monumento,
                icon=folium.Icon(color="red")
            ).add_to(mappa)

        else:

            mappa = folium.Map(
                location=end,
                zoom_start=13
            )

            folium.Marker(
                end,
                popup=monumento
            ).add_to(mappa)

        st.markdown("### 🗺️ Percorso")

        st_folium(
            mappa,
            width=700,
            height=500
        )