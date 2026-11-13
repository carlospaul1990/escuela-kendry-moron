import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timezone, timedelta
import urllib.parse
import base64
import os

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA (MOBILE-FIRST)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Escuela Kendry Morón | Torneos de Ajedrez",
    page_icon="♟️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------
# LOGO INSTITUCIONAL (CARGA LOCAL O VECTORIAL DE ALTA NITIDEZ)
# -----------------------------------------------------------------------------
def get_logo_html():
    if os.path.exists("logo.png"):
        with open("logo.png", "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        return f'<img src="data:image/png;base64,{data}" class="brand-logo" alt="Logo Escuela Kendry Morón">'
    
    return """
    <svg class="brand-logo-svg" viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <path id="topArc" d="M 32,125 A 88,88 0 1,1 208,125" />
            <path id="bottomArc" d="M 42,145 A 84,84 0 0,0 198,145" />
        </defs>
        <circle cx="120" cy="120" r="112" fill="#141820" stroke="#C8102E" stroke-width="4"/>
        <text fill="#FFFFFF" font-size="14.5" font-weight="800" letter-spacing="2.2" font-family="Oswald, sans-serif">
            <textPath href="#topArc" startOffset="50%" text-anchor="middle">ESCUELA NACIONAL DE TALENTO</textPath>
        </text>
        <path d="M 92,68 L 102,68 L 102,75 L 112,75 L 112,68 L 128,68 L 128,75 L 138,75 L 138,68 L 148,68 L 148,84 L 140,90 L 143,115 C 128,107 112,107 97,115 L 100,90 L 92,84 Z" fill="#FFFFFF"/>
        <path d="M 97,158 L 102,118 C 115,112 135,116 141,132 C 145,143 134,154 118,158 L 146,158 L 146,163 L 95,163 Z" fill="#C8102E"/>
        <circle cx="111" cy="128" r="2.5" fill="#FFFFFF"/>
        <rect x="88" y="167" width="64" height="9" rx="2" fill="#C8102E"/>
        <text fill="#F5C518" font-size="16" font-weight="800" letter-spacing="2.5" font-family="Oswald, sans-serif">
            <textPath href="#bottomArc" startOffset="50%" text-anchor="middle">KENDRY MORÓN</textPath>
        </text>
    </svg>
    """

# -----------------------------------------------------------------------------
# CSS RESPONSIVO (DISEÑO APP NATIVA PARA CELULAR Y DESKTOP)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --bg-dark: #090B0F;
    --bg-card: #131722;
    --crimson: #C8102E;
    --gold: #F5C518;
    --text-main: #F8FAFC;
    --text-muted: #94A3B8;
}

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 5.5rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    max-width: 1100px !important;
}

.stApp {
    background-color: var(--bg-dark);
    background-image: radial-gradient(circle at 50% 0%, rgba(200, 16, 46, 0.18) 0%, transparent 55%);
    color: var(--text-main);
    font-family: 'Plus Jakarta Sans', sans-serif;
}

#MainMenu, footer, header {visibility: hidden;}

h1, h2, h3, .oswald {
    font-family: 'Oswald', sans-serif !important;
    text-transform: uppercase;
}

/* HERO SECTION */
.hero-card {
    background: linear-gradient(160deg, #161B26 0%, #1F0B11 55%, #0D1017 100%);
    border: 1px solid rgba(200, 16, 46, 0.5);
    border-radius: 20px 20px 0 0;
    border-bottom: none;
    padding: 1.6rem 1.6rem 1rem 1.6rem;
    margin-bottom: 0;
    display: flex;
    align-items: center;
    gap: 20px;
}

.brand-logo, .brand-logo-svg {
    width: 125px;
    height: 125px;
    border-radius: 50%;
    border: 3px solid var(--crimson);
    background: #FFFFFF;
    padding: 4px;
    box-shadow: 0 0 25px rgba(200, 16, 46, 0.45);
    flex-shrink: 0;
}

.brand-logo-svg {
    background: transparent;
    padding: 0;
}

.hero-badge {
    display: inline-block;
    background: rgba(200, 16, 46, 0.22);
    border: 1px solid var(--crimson);
    color: #FF6B81;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.hero-title {
    font-size: 2.35rem;
    line-height: 1.08;
    margin: 0;
    color: #FFFFFF;
}

.hero-title span { color: var(--crimson); }

.hero-slogan {
    color: var(--gold);
    font-weight: 700;
    font-size: 0.9rem;
    letter-spacing: 1.5px;
    margin-top: 6px;
}

/* NAVEGACIÓN TÁCTIL TIPO APP */
div[data-testid="stRadio"] > div {
    display: flex;
    flex-direction: row;
    gap: 8px;
    width: 100%;
    background: #131722;
    padding: 6px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-top: 0.6rem;
}

div[data-testid="stRadio"] label {
    flex: 1;
    text-align: center;
    justify-content: center;
    background: transparent;
    border-radius: 10px;
    padding: 10px 6px !important;
    margin: 0 !important;
    cursor: pointer;
    transition: all 0.2s;
}

div[data-testid="stRadio"] label[data-checked="true"] {
    background: var(--crimson) !important;
    color: #FFFFFF !important;
    font-weight: 800 !important;
    box-shadow: 0 4px 14px rgba(200, 16, 46, 0.45);
}

div[data-testid="stRadio"] label > div:first-child {
    display: none !important;
}

/* TARJETAS DE CONTENIDO */
.mobile-card {
    background: var(--bg-card);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.2rem;
    margin-bottom: 12px;
}

.cat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #FFFFFF;
    color: #090B0F;
    padding: 12px 14px;
    border-radius: 12px;
    margin-bottom: 8px;
    border-left: 6px solid var(--crimson);
}

.cat-name {
    font-family: 'Oswald', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
}

.cat-name span { color: var(--crimson); }

.cat-tag {
    background: #090B0F;
    color: var(--gold);
    font-size: 0.75rem;
    font-weight: 800;
    padding: 4px 10px;
    border-radius: 6px;
}

.prize-item {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 12px 14px;
    margin-bottom: 8px;
}

.prize-gold {
    background: rgba(245, 197, 24, 0.1);
    border-color: rgba(245, 197, 24, 0.45);
}

/* BOTÓN FLOTANTE INFERIOR */
.sticky-bottom-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(13, 16, 23, 0.94);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-top: 1px solid rgba(200, 16, 46, 0.5);
    padding: 10px 16px;
    z-index: 9999;
    display: flex;
    justify-content: center;
}

.sticky-wa-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    width: 100%;
    max-width: 600px;
    background: linear-gradient(90deg, #C8102E 0%, #9E0B22 100%);
    color: #FFFFFF !important;
    text-decoration: none;
    font-weight: 800;
    font-size: 0.95rem;
    padding: 13px 18px;
    border-radius: 12px;
    box-shadow: 0 6px 20px rgba(200, 16, 46, 0.5);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* REGLAS EXCLUSIVAS MÓVIL */
@media (max-width: 768px) {
    .hero-card {
        flex-direction: column;
        text-align: center;
        padding: 1.3rem 1rem 0.8rem 1rem;
        gap: 12px;
    }
    .brand-logo, .brand-logo-svg {
        width: 100px;
        height: 100px;
    }
    .hero-title {
        font-size: 1.8rem;
    }
    .hero-slogan {
        font-size: 0.78rem;
    }
    div[data-testid="stRadio"] label p {
        font-size: 0.78rem !important;
        line-height: 1.2 !important;
    }
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATOS DE TORNEOS 2027
# -----------------------------------------------------------------------------
TORNEOS_2027 = [
    {
        "mes": "ENERO",
        "fechas": "Domingo 10 de Enero, 2027",
        "fecha_ics": "20270110",
        "titulo": "Torneo Blitz en Parejas",
        "modalidad": "Blitz • Duplas",
        "detalle": "Torneo rápido en parejas para abrir la temporada 2027.",
        "icono": "⚡"
    },
    {
        "mes": "ENERO",
        "fechas": "29, 30 y 31 de Enero, 2027",
        "fecha_ics": "20270129",
        "titulo": "Metropolitano Regional",
        "modalidad": "Clásico / Estándar",
        "detalle": "Clasificatorio regional en Santo Domingo.",
        "icono": "📍"
    },
    {
        "mes": "FEBRERO",
        "fechas": "27 y 28 de Febrero, 2027",
        "fecha_ics": "20270227",
        "titulo": "Nacional x Equipos Regional",
        "modalidad": "3x3 (Clásica, Rápida y Blitz)",
        "detalle": "Formato dinámico de 3 rondas por cada ritmo de juego.",
        "icono": "🛡️"
    },
    {
        "mes": "MARZO",
        "fechas": "26, 27 y 28 de Marzo, 2027",
        "fecha_ics": "20270326",
        "titulo": "Torneo Abierto Femenino",
        "modalidad": "Femenino",
        "detalle": "Competencia abierta dedicada al ajedrez femenino.",
        "icono": "👑"
    },
    {
        "mes": "ABRIL",
        "fechas": "18 de Abril, 2027",
        "fecha_ics": "20270418",
        "titulo": "Torneo Nacional de Rápidas",
        "modalidad": "Rápidas",
        "detalle": "Campeonato nacional activo a una sola jornada.",
        "icono": "⏱️"
    },
    {
        "mes": "MAYO",
        "fechas": "07-09 y 14-16 de Mayo, 2027",
        "fecha_ics": "20270507",
        "titulo": "Gran Torneo Abierto",
        "modalidad": "Clásico / Estándar",
        "detalle": "Dos fines de semana de competencia abierta.",
        "icono": "🏁"
    },
    {
        "mes": "JUNIO",
        "fechas": "Junio 2027",
        "fecha_ics": "20270615",
        "titulo": "Torneo Leyendas vs. Prodigios",
        "modalidad": "Match Especial 10 vs. 10",
        "detalle": "Duelo estelar de 10 maestros contra 10 jóvenes talentos.",
