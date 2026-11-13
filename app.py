import streamlit as st
import streamlit.components.v1 as components
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

if "vista_actual" not in st.session_state:
    st.session_state.vista_actual = "nacional"

# -----------------------------------------------------------------------------
# LOGO INSTITUCIONAL
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
# CSS RESPONSIVO + ESTILIZACIÓN PROFESIONAL DEL FORMULARIO DARK MODE
# -----------------------------------------------------------------------------
CSS_ESTILOS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

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

.nav-header-label {
    text-align: center;
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 1.5px;
    color: #F5C518;
    text-transform: uppercase;
    margin: 0.4rem 0 0.5rem 0;
}

div.stButton > button[kind="secondary"] {
    background: #1A202E !important;
    color: #FFFFFF !important;
    border: 2px solid rgba(255, 255, 255, 0.28) !important;
    border-radius: 14px !important;
    padding: 0.85rem 0.5rem !important;
    font-family: 'Oswald', sans-serif !important;
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important;
    transition: all 0.2s ease !important;
}

div.stButton > button[kind="secondary"]:hover {
    border-color: #F5C518 !important;
    background: #232B3E !important;
    color: #F5C518 !important;
    transform: translateY(-2px);
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #E01133 0%, #A30B24 100%) !important;
    color: #FFFFFF !important;
    border: 2px solid #F5C518 !important;
    border-radius: 14px !important;
    padding: 0.85rem 0.5rem !important;
    font-family: 'Oswald', sans-serif !important;
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
    box-shadow: 0 0 22px rgba(200, 16, 46, 0.65) !important;
}

/* ==========================================================================
   ESTILOS DEL FORMULARIO DE INSCRIPCIÓN (DARK MODE ÉLITE + ALTO CONTRASTE)
   ========================================================================== */
[data-testid="stForm"] {
    background: linear-gradient(180deg, #131722 0%, #0E1119 100%) !important;
    border: 1px solid rgba(200, 16, 46, 0.45) !important;
    border-top: 4px solid #C8102E !important;
    border-radius: 18px !important;
    padding: 1.6rem !important;
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.55) !important;
}

/* Etiquetas de los inputs (100% visibles en blanco) */
[data-testid="stForm"] label,
[data-testid="stForm"] label p,
[data-testid="stSelectbox"] label p,
[data-testid="stTextInput"] label p {
    color: #F8FAFC !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.3px !important;
    margin-bottom: 4px !important;
}

/* Cajas de texto y desplegables en modo oscuro elegante */
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    background-color: #090B0F !important;
    border: 1.5px solid rgba(255, 255, 255, 0.22) !important;
    border-radius: 12px !important;
    color: #FFFFFF !important;
    min-height: 46px !important;
    transition: border-color 0.2s ease !important;
}

div[data-baseweb="input"] > div:focus-within,
div[data-baseweb="select"] > div:focus-within {
    border-color: #F5C518 !important;
    box-shadow: 0 0 0 2px rgba(245, 197, 24, 0.2) !important;
}

div[data-baseweb="input"] input {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    font-weight: 500 !important;
}

div[data-baseweb="input"] input::placeholder {
    color: #64748B !important;
    -webkit-text-fill-color: #64748B !important;
}

div[data-baseweb="select"] span,
div[data-baseweb="select"] div {
    color: #FFFFFF !important;
}

/* Botón Submit del Formulario (Rojo Carmesí + Borde Dorado + Texto Blanco) */
[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(135deg, #E01133 0%, #9E0B22 100%) !important;
    color: #FFFFFF !important;
    border: 2px solid #F5C518 !important;
    border-radius: 12px !important;
    padding: 0.9rem 1.2rem !important;
    margin-top: 0.6rem !important;
    font-family: 'Oswald', sans-serif !important;
    font-size: 1.25rem !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    box-shadow: 0 8px 24px rgba(200, 16, 46, 0.5) !important;
    transition: all 0.2s ease !important;
}

[data-testid="stFormSubmitButton"] button p {
    color: #FFFFFF !important;
    font-family: 'Oswald', sans-serif !important;
    font-size: 1.25rem !important;
    font-weight: 700 !important;
}

[data-testid="stFormSubmitButton"] button:hover {
    background: linear-gradient(135deg, #FF173D 0%, #B80D29 100%) !important;
    transform: translateY(-2px);
    box-shadow: 0 10px 28px rgba(245, 197, 24, 0.35) !important;
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
    div.stButton > button[kind="secondary"],
    div.stButton > button[kind="primary"] {
        font-size: 1.05rem !important;
        padding: 0.8rem 0.6rem !important;
    }
    [data-testid="stForm"] {
        padding: 1.1rem !important;
    }
}
</style>
"""

st.markdown(CSS_ESTILOS, unsafe_allow_html=True)

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
        "icono": "⚔️"
    }
]

def generar_ics(titulo, fecha_str, descripcion):
    return (
        "BEGIN:VCALENDAR\n"
        "VERSION:2.0\n"
        "BEGIN:VEVENT\n"
        f"DTSTART;VALUE=DATE:{fecha_str}\n"
        f"SUMMARY:{titulo} - Escuela Kendry Morón\n"
        f"DESCRIPTION:{descripcion}\n"
        "LOCATION:Escuela Nacional de Talento Kendry Morón, Santo Domingo\n"
        "END:VEVENT\n"
        "END:VCALENDAR"
    )

# -----------------------------------------------------------------------------
# HERO BANNER + RELOJ EN VIVO
# -----------------------------------------------------------------------------
logo_actual = get_logo_html()

st.markdown(
    f"""
    <div class="hero-card">
        {logo_actual}
        <div style="flex: 1;">
            <div class="hero-badge">♟️ Santo Domingo • Válido Rating FIDE</div>
            <h1 class="hero-title">ESCUELA NACIONAL DE TALENTO <span>KENDRY MORÓN</span></h1>
            <div class="hero-slogan">★ FORMAMOS TALENTO, INSPIRAMOS CAMPEONES ★</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

RELOJ_HTML = """
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@700&family=Plus+Jakarta+Sans:wght@700;800&display=swap" rel="stylesheet">
<style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
        background: transparent;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .timer-wrapper {
        background: linear-gradient(180deg, #131722 0%, #0D1017 100%);
        border: 1px solid rgba(200, 16, 46, 0.5);
        border-top: 1px solid rgba(245, 197, 24, 0.25);
        border-radius: 0 0 20px 20px;
        padding: 14px 16px 16px 16px;
        box-shadow: 0 14px 30px rgba(0, 0, 0, 0.6);
    }
    .timer-header {
        font-size: 0.74rem;
        color: #F5C518;
        font-weight: 800;
        text-align: center;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    .grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        max-width: 540px;
        margin: 0 auto;
    }
    .box {
        background: #090B0F;
        border: 1px solid rgba(245, 197, 24, 0.35);
        border-radius: 12px;
        padding: 10px 4px;
        text-align: center;
    }
    .num {
        font-family: 'Oswald', sans-serif;
        font-size: 1.85rem;
        color: #F5C518;
        line-height: 1;
        font-variant-numeric: tabular-nums;
    }
    .num.sec { color: #FF4D6D; }
    .lbl {
        font-size: 0.65rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 4px;
        font-weight: 700;
    }
</style>
</head>
<body>
    <div class="timer-wrapper">
        <div class="timer-header">⏳ Cuenta Regresiva • Torneo Nacional Juvenil (27 Nov, 9:00 AM)</div>
        <div class="grid">
            <div class="box"><div class="num" id="d">--</div><div class="lbl">Días</div></div>
            <div class="box"><div class="num" id="h">--</div><div class="lbl">Horas</div></div>
            <div class="box"><div class="num" id="m">--</div><div class="lbl">Min</div></div>
            <div class="box"><div class="num sec" id="s">--</div><div class="lbl">Seg</div></div>
        </div>
    </div>

    <script>
        const targetDate = new Date("2026-11-27T09:00:00-04:00").getTime();

        function updateTimer() {
            const now = new Date().getTime();
            const distance = targetDate - now;

            if (distance <= 0) {
                document.getElementById("d").innerText = "00";
                document.getElementById("h").innerText = "00";
                document.getElementById("m").innerText = "00";
                document.getElementById("s").innerText = "00";
                return;
            }

            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            document.getElementById("d").innerText = String(days).padStart(2, '0');
            document.getElementById("h").innerText = String(hours).padStart(2, '0');
            document.getElementById("m").innerText = String(minutes).padStart(2, '0');
            document.getElementById("s").innerText = String(seconds).padStart(2, '0');
        }

        updateTimer();
        setInterval(updateTimer, 1000);
    </script>
</body>
</html>
"""

components.html(RELOJ_HTML, height=132)

# -----------------------------------------------------------------------------
# BARRA DE NAVEGACIÓN PRINCIPAL DE ALTO IMPACTO
# -----------------------------------------------------------------------------
st.markdown('<div class="nav-header-label">👇 Selecciona una sección 👇</div>', unsafe_allow_html=True)

nav1, nav2, nav3 = st.columns(3, gap="small")

with nav1:
    if st.button(
        "🏆 TORNEO NACIONAL (27 NOV)",
        type="primary" if st.session_state.vista_actual == "nacional" else "secondary",
        use_container_width=True
    ):
        st.session_state.vista_actual = "nacional"
        st.rerun()

with nav2:
    if st.button(
        "📅 CALENDARIO 2027",
        type="primary" if st.session_state.vista_actual == "calendario" else "secondary",
        use_container_width=True
    ):
        st.session_state.vista_actual = "calendario"
        st.rerun()

with nav3:
    if st.button(
        "📝 INSCRIBIRSE AHORA",
        type="primary" if st.session_state.vista_actual == "inscripcion" else "secondary",
        use_container_width=True
    ):
        st.session_state.vista_actual = "inscripcion"
        st.rerun()

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# =============================================================================
# VISTA 1: TORNEO NACIONAL POR CATEGORÍAS (27 AL 29 NOV)
# =============================================================================
if st.session_state.vista_actual == "nacional":
    st.markdown(
        """
        <div class="mobile-card" style="border-left: 5px solid #F5C518;">
            <span style="background:#F5C518; color:#090B0F; font-weight:800; padding:3px 10px; border-radius:6px; font-size:0.75rem;">
                27 AL 29 DE NOVIEMBRE • FIDE
            </span>
            <h2 style="font-size: 1.75rem; margin: 8px 0 6px 0; color: #FFFFFF;">
                TORNEO NACIONAL POR CATEGORÍAS
            </h2>
            <div style="color: #CBD5E1; font-size: 0.9rem; line-height: 1.5;">
                📍 <strong>Sede:</strong> Escuela Nacional de Talento Kendry Morón, Santo Domingo.<br>
                ⏱️ <strong>Ritmo:</strong> 1 hora 30 min + 30 seg de incremento.<br>
                ♟️ <strong>Sistema:</strong> Suizo a 5 Rondas.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown("#### 🎯 Categorías Juveniles")
        st.markdown(
            """
            <div class="cat-row"><div class="cat-name">♟️ SUB <span>17</span></div><div class="cat-tag">ABSOLUTO Y FEMENINO</div></div>
            <div class="cat-row"><div class="cat-name">♞ SUB <span>15</span></div><div class="cat-tag">ABSOLUTO</div></div>
            <div class="cat-row"><div class="cat-name">♝ SUB <span>13</span></div><div class="cat-tag">ABSOLUTO</div></div>
            <div class="cat-row"><div class="cat-name">♜ SUB <span>11</span></div><div class="cat-tag">ABSOLUTO</div></div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown("#### 🏅 Premiación Oficial")
        st.markdown(
            """
            <div class="prize-item prize-gold">
                <div style="font-weight: 800; color: #F5C518; font-size: 1rem;">🥇 1ER LUGAR: Trofeo + Viaje</div>
                <div style="color: #E2E8F0; font-size: 0.85rem; margin-top: 3px;">
                    Boletos aéreos ida y vuelta a los <strong>XXIII Juegos Centroamericanos y del Caribe de la Juventud 2027</strong>.
                </div>
            </div>
            <div class="prize-item">
                <div style="font-weight: 800; color: #FFFFFF; font-size: 0.95rem;">🥈 2DO LUGAR: Medalla + Tablero Staunton</div>
                <div style="color: #94A3B8; font-size: 0.83rem;">Tablero de madera preciosa con piezas Staunton.</div>
            </div>
            <div class="prize-item">
                <div style="font-weight: 800; color: #FFFFFF; font-size: 0.95rem;">🥉 3ER LUGAR: Medalla + Tablero DGT</div>
                <div style="color: #94A3B8; font-size: 0.83rem;">Tablero de madera preciosa con piezas DGT.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.info("🎓 **Entrenamiento continuo** incluido para todos los primeros lugares con miras al Centroamericano.")

# =============================================================================
# VISTA 2: CALENDARIO DE TORNEOS 2027
# =============================================================================
elif st.session_state.vista_actual == "calendario":
    st.markdown("#### 📅 Temporada Oficial 2027 (Enero – Junio)")
    
    mes_filtro = st.selectbox(
        "Filtrar por mes:",
        ["Todos los meses", "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO"],
        label_visibility="collapsed"
    )

    filtrados = [t for t in TORNEOS_2027 if mes_filtro == "Todos los meses" or t["mes"] == mes_filtro]

    for idx, ev in enumerate(filtrados):
        st.markdown(
            f"""
            <div class="mobile-card" style="border-left: 4px solid #C8102E;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="background:#C8102E; color:#FFF; font-weight:800; font-size:0.75rem; padding:3px 10px; border-radius:6px;">
                        {ev['mes']} 2027
                    </span>
                    <span style="font-size: 1.3rem;">{ev['icono']}</span>
                </div>
                <div style="color: #F5C518; font-weight: 700; font-size: 0.88rem; margin-top: 8px;">
                    🗓️ {ev['fechas']}
                </div>
                <div style="font-family: 'Oswald', sans-serif; font-size: 1.35rem; color: #FFFFFF; margin: 2px 0;">
                    {ev['titulo']}
                </div>
                <div style="color: #FF6B81; font-size: 0.78rem; font-weight: 700; text-transform: uppercase;">
                    {ev['modalidad']}
                </div>
                <div style="color: #94A3B8; font-size: 0.85rem; margin-top: 4px;">
                    {ev['detalle']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.download_button(
            label=f"➕ Guardar '{ev['titulo']}' en mi Calendario",
            data=generar_ics(ev["titulo"], ev["fecha_ics"], ev["detalle"]),
            file_name=f"torneo_{ev['mes'].lower()}_{idx}.ics",
            mime="text/calendar",
            key=f"btn_ics_{idx}",
            use_container_width=True
        )
        st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

# =============================================================================
# VISTA 3: FORMULARIO DE INSCRIPCIÓN OFICIAL (DARK MODE ÉLITE)
# =============================================================================
elif st.session_state.vista_actual == "inscripcion":
    st.markdown(
        """
        <div class="mobile-card" style="border-left: 5px solid #C8102E; margin-bottom: 14px;">
            <span style="background: rgba(200,16,46,0.25); border: 1px solid #C8102E; color: #FF6B81; font-weight: 800; padding: 3px 10px; border-radius: 6px; font-size: 0.75rem;">
                REGISTRO OFICIAL DE ATLETAS
            </span>
            <h2 style="font-size: 1.7rem; margin: 8px 0 4px 0; color: #FFFFFF;">
                📝 PRE-INSCRIPCIÓN EN LÍNEA
            </h2>
            <p style="color: #CBD5E1; font-size: 0.88rem; margin: 0;">
                Completa los datos del jugador para generar su ficha oficial y enviarla en un toque al WhatsApp de coordinación (<strong>CM Michel de Jesús</strong>).
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.form("form_movil"):
        f_col1, f_col2 = st.columns(2, gap="medium")

        with f_col1:
            nombre = st.text_input(
                "👤 Nombre Completo del Jugador *",
                placeholder="Ej. Ángel Sebastián Lara"
            )
            lista_torneos = ["Torneo Nacional por Categorías (27-29 Nov)"] + [
                f"{t['titulo']} ({t['mes']} 2027)" for t in TORNEOS_2027
            ]
            torneo = st.selectbox("🏆 Torneo a Participar *", lista_torneos)
            categoria = st.selectbox(
                "🎯 Categoría / Rama *",
                [
                    "Sub-17 Absoluto",
                    "Sub-17 Femenino",
                    "Sub-15 Absoluto",
                    "Sub-13 Absoluto",
                    "Sub-11 Absoluto",
                    "Abierto / Libre"
                ]
            )

        with f_col2:
            telefono = st.text_input(
                "📱 Teléfono / WhatsApp de Contacto *",
                placeholder="Ej. 809-555-0199"
            )
            id_fide = st.text_input(
                "🌐 ID FIDE (Opcional)",
                placeholder="Ej. 6401234 (Dejar vacío si no posee)"
            )
            club_escuela = st.text_input(
                "♟️ Club / Academia / Provincia (Opcional)",
                placeholder="Ej. Escuela Kendry Morón / Santo Domingo"
            )

        submit = st.form_submit_button("✅ GENERAR FICHA DE INSCRIPCIÓN", use_container_width=True)

    if submit:
        if not nombre or not telefono:
            st.error("⚠️ Por favor escribe el nombre completo del jugador y un teléfono de contacto.")
        else:
            fide_texto = id_fide if id_fide else "Sin ID FIDE"
            club_texto = club_escuela if club_escuela else "No especificado"
            texto_wa = (
                f"*FICHA DE INSCRIPCIÓN - ESCUELA KENDRY MORÓN*%0A"
                f"• *Jugador:* {urllib.parse.quote(nombre)}%0A"
                f"• *Torneo:* {urllib.parse.quote(torneo)}%0A"
                f"• *Categoría:* {urllib.parse.quote(categoria)}%0A"
                f"• *ID FIDE:* {urllib.parse.quote(fide_texto)}%0A"
                f"• *Club/Prov:* {urllib.parse.quote(club_texto)}%0A"
                f"• *Contacto:* {urllib.parse.quote(telefono)}"
            )
            st.markdown(
                f"""
                <div style="background: rgba(16, 185, 129, 0.14); border: 1.5px solid #10B981; border-radius: 14px; padding: 14px; margin-top: 12px; margin-bottom: 12px;">
                    <div style="color: #34D399; font-weight: 800; font-size: 1rem;">✅ ¡FICHA GENERADA PARA {nombre.upper()}!</div>
                    <div style="color: #E2E8F0; font-size: 0.86rem; margin-top: 4px;">
                        Pulsa el botón dorado de abajo para enviar los datos directamente por WhatsApp al <strong>CM Michel de Jesús (829.773.2231)</strong>.
                    </div>
                </div>
                <a href="https://wa.me/18297732231?text={texto_wa}" target="_blank"
                   style="display: block; width: 100%; text-align: center; background: #F5C518; color: #090B0F !important;
                          font-family: 'Oswald', sans-serif; font-size: 1.25rem; font-weight: 700; padding: 14px 20px;
                          border-radius: 12px; text-decoration: none; text-transform: uppercase; letter-spacing: 0.8px;
                          box-shadow: 0 8px 25px rgba(245, 197, 24, 0.4);">
                    📲 ENVIAR INSCRIPCIÓN POR WHATSAPP AHORA
                </a>
                """,
                unsafe_allow_html=True
            )

# -----------------------------------------------------------------------------
# BARRA FLOTANTE INFERIOR PERSISTENTE
# -----------------------------------------------------------------------------
msg_directo = urllib.parse.quote("Hola CM Michel de Jesús, quiero información e inscribirme en los torneos de la Escuela Kendry Morón.")
st.markdown(
    f"""
    <div class="sticky-bottom-bar">
        <a href="https://wa.me/18297732231?text={msg_directo}" target="_blank" class="sticky-wa-btn">
            📲 INSCRIPCIÓN DIRECTA • CM MICHEL (829.773.2231)
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
