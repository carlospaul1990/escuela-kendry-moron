import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta
import urllib.parse
import base64
import os

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Escuela Nacional de Talento Kendry Morón | Ajedrez RD",
    page_icon="♟️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------
# LOGO EN ALTA CALIDAD (SOPORTA ARCHIVO LOCAL O VECTORIAL INTEGRADO)
# -----------------------------------------------------------------------------
def get_logo_html():
    # Si guardas la imagen del logo como 'logo.png' en la misma carpeta, la usará automáticamente
    if os.path.exists("logo.png"):
        with open("logo.png", "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        return f'<img src="data:image/png;base64,{data}" class="brand-logo" alt="Logo Kendry Morón">'
    
    # De lo contrario, renderiza una versión vectorial nítida inspirada en el emblema oficial
    return """
    <div class="logo-emblem-container">
        <svg viewBox="0 0 240 240" width="155" height="155" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                    <feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#C8102E" flood-opacity="0.45"/>
                </filter>
                <path id="topArc" d="M 32,125 A 88,88 0 1,1 208,125" />
                <path id="bottomArc" d="M 42,145 A 84,84 0 0,0 198,145" />
            </defs>
            <circle cx="120" cy="120" r="112" fill="#141820" stroke="#C8102E" stroke-width="3"/>
            <circle cx="120" cy="120" r="104" fill="none" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
            
            <!-- Texto Curvo Superior -->
            <text fill="#FFFFFF" font-size="14.5" font-weight="800" letter-spacing="2.2" font-family="Oswald, sans-serif">
                <textPath href="#topArc" startOffset="50%" text-anchor="middle">
                    ESCUELA NACIONAL DE TALENTO
                </textPath>
            </text>
            
            <!-- Torre Negra Superior -->
            <path d="M 92,68 L 102,68 L 102,75 L 112,75 L 112,68 L 128,68 L 128,75 L 138,75 L 138,68 L 148,68 L 148,84 L 140,90 L 143,115 C 128,107 112,107 97,115 L 100,90 L 92,84 Z" fill="#FFFFFF"/>
            
            <!-- Caballo Rojo Inferior -->
            <path d="M 97,158 L 102,118 C 115,112 135,116 141,132 C 145,143 134,154 118,158 L 146,158 L 146,163 L 95,163 Z" fill="#C8102E" filter="url(#glow)"/>
            <circle cx="111" cy="128" r="2.5" fill="#FFFFFF"/>
            
            <!-- Base Roja -->
            <rect x="88" y="167" width="64" height="9" rx="2" fill="#C8102E"/>
            
            <!-- Texto Curvo Inferior -->
            <text fill="#F5C518" font-size="16" font-weight="800" letter-spacing="2.5" font-family="Oswald, sans-serif">
                <textPath href="#bottomArc" startOffset="50%" text-anchor="middle">
                    KENDRY MORÓN
                </textPath>
            </text>
        </svg>
    </div>
    """

# -----------------------------------------------------------------------------
# ESTILOS CSS PERSONALIZADOS (ESTÉTICA TORNEO ÉLITE / DARK MODE)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --bg-dark: #0A0C10;
    --bg-card: #131720;
    --bg-card-hover: #1A202C;
    --crimson: #C8102E;
    --crimson-dark: #8E0B20;
    --gold: #F5C518;
    --text-main: #F8FAFC;
    --text-muted: #94A3B8;
}

/* Fondo general y tipografía */
.stApp {
    background-color: var(--bg-dark);
    background-image: 
        radial-gradient(circle at 15% 15%, rgba(200, 16, 46, 0.14) 0%, transparent 45%),
        radial-gradient(circle at 85% 80%, rgba(245, 197, 24, 0.08) 0%, transparent 45%);
    color: var(--text-main);
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Ocultar elementos por defecto de Streamlit */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

h1, h2, h3, .oswald {
    font-family: 'Oswald', sans-serif !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* HERO BANNER */
.hero-wrapper {
    background: linear-gradient(135deg, #11151E 0%, #1C0B10 55%, #0D1017 100%);
    border: 1px solid rgba(200, 16, 46, 0.45);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.65);
    position: relative;
    overflow: hidden;
}

.hero-badge {
    display: inline-block;
    background: rgba(200, 16, 46, 0.2);
    border: 1px solid #C8102E;
    color: #FF4D6D;
    padding: 5px 14px;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}

.hero-title {
    font-size: 3.1rem;
    font-weight: 700;
    line-height: 1.05;
    margin: 0;
    color: #FFFFFF;
}

.hero-title span {
    color: var(--crimson);
}

.hero-slogan {
    font-size: 1.15rem;
    color: var(--gold);
    font-weight: 600;
    letter-spacing: 2px;
    margin-top: 0.6rem;
    text-transform: uppercase;
}

.brand-logo {
    width: 155px;
    height: 155px;
    border-radius: 50%;
    border: 3px solid var(--crimson);
    background: #FFFFFF;
    padding: 6px;
    box-shadow: 0 0 30px rgba(200, 16, 46, 0.4);
}

/* TARJETAS KPI / CONTADOR */
.countdown-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-top: 1.2rem;
}

.count-box {
    background: rgba(10, 12, 16, 0.85);
    border: 1px solid rgba(245, 197, 24, 0.35);
    border-radius: 12px;
    padding: 12px 8px;
    text-align: center;
}

.count-num {
    font-family: 'Oswald', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--gold);
    line-height: 1;
}

.count-label {
    font-size: 0.72rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 4px;
}

/* TARJETA TORNEO NACIONAL DESTACADO */
.featured-card {
    background: linear-gradient(145deg, #161B26 0%, #10131A 100%);
    border-left: 6px solid var(--gold);
    border-top: 1px solid rgba(255,255,255,0.08);
    border-right: 1px solid rgba(255,255,255,0.08);
    border-bottom: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1.5rem;
}

.cat-pill {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #FFFFFF;
    color: #0B0D10;
    padding: 10px 16px;
    border-radius: 10px;
    margin-bottom: 10px;
    font-weight: 800;
    border-left: 6px solid var(--crimson);
}

.cat-pill .sub {
    font-family: 'Oswald', sans-serif;
    font-size: 1.35rem;
    color: #0B0D10;
}

.cat-pill .sub span {
    color: var(--crimson);
}

.cat-pill .mod {
    font-size: 0.85rem;
    background: #0B0D10;
    color: var(--gold);
    padding: 4px 10px;
    border-radius: 6px;
}

.prize-box {
    background: rgba(245, 197, 24, 0.08);
    border: 1px solid rgba(245, 197, 24, 0.3);
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 10px;
}

/* TARJETAS CALENDARIO 2027 */
.event-card {
    background: var(--bg-card);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 1.4rem;
    height: 100%;
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
}

.event-card:hover {
    transform: translateY(-4px);
    border-color: var(--crimson);
    background: var(--bg-card-hover);
    box-shadow: 0 12px 30px rgba(200, 16, 46, 0.2);
}

.event-month-badge {
    background: var(--crimson);
    color: #FFFFFF;
    font-family: 'Oswald', sans-serif;
    font-weight: 700;
    font-size: 0.9rem;
    padding: 4px 12px;
    border-radius: 6px;
    display: inline-block;
    letter-spacing: 1px;
}

.event-date {
    color: var(--gold);
    font-weight: 700;
    font-size: 0.95rem;
    margin-top: 10px;
}

.event-title {
    font-family: 'Oswald', sans-serif;
    font-size: 1.45rem;
    color: #FFFFFF;
    margin: 6px 0;
    line-height: 1.15;
}

.event-detail {
    color: var(--text-muted);
    font-size: 0.9rem;
    margin-bottom: 12px;
}

/* BOTÓN WHATSAPP */
.wa-btn {
    display: inline-block;
    width: 100%;
    text-align: center;
    background: linear-gradient(90deg, #C8102E 0%, #9B0B22 100%);
    color: #FFFFFF !important;
    text-decoration: none;
    font-weight: 700;
    padding: 12px 20px;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.15);
    transition: 0.2s;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.wa-btn:hover {
    background: linear-gradient(90deg, #E01435 0%, #B30D27 100%);
    box-shadow: 0 6px 20px rgba(200, 16, 46, 0.45);
}

.wa-btn-gold {
    display: inline-block;
    width: 100%;
    text-align: center;
    background: var(--gold);
    color: #0A0C10 !important;
    text-decoration: none;
    font-weight: 800;
    padding: 13px 20px;
    border-radius: 10px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATOS OFICIALES DE TORNEOS (EXTRAÍDOS DE LOS FLYERS OFICIALES)
# -----------------------------------------------------------------------------
TORNEOS_2027 = [
    {
        "mes": "ENERO",
        "orden_mes": 1,
        "fechas": "Domingo 10 de Enero, 2027",
        "fecha_ics": "20270110",
        "titulo": "Torneo Blitz en Parejas",
        "modalidad": "Blitz",
        "detalle": "Dinámica rápida por duplas. Ideal para abrir la temporada competitiva.",
        "icono": "⚡"
    },
    {
        "mes": "ENERO",
        "orden_mes": 1,
        "fechas": "29, 30 y 31 de Enero, 2027",
        "fecha_ics": "20270129",
        "titulo": "Metropolitano Regional",
        "modalidad": "Clásico / Estándar",
        "detalle": "Clasificatorio regional de alto nivel en Santo Domingo.",
        "icono": "📍"
    },
    {
        "mes": "FEBRERO",
        "orden_mes": 2,
        "fechas": "27 y 28 de Febrero, 2027",
        "fecha_ics": "20270227",
        "titulo": "Nacional x Equipos Regional",
        "modalidad": "Multiritmo (3x3)",
        "detalle": "Formato 3x3 (Clásica, Rápida y Blitz) — 3 rondas por cada ritmo.",
        "icono": "🛡️"
    },
    {
        "mes": "MARZO",
        "orden_mes": 3,
        "fechas": "26, 27 y 28 de Marzo, 2027",
        "fecha_ics": "20270326",
        "titulo": "Torneo Abierto Femenino",
        "modalidad": "Femenino",
        "detalle": "Evento exclusivo para impulsar el talento femenino nacional.",
        "icono": "👑"
    },
    {
        "mes": "ABRIL",
        "orden_mes": 4,
        "fechas": "18 de Abril, 2027",
        "fecha_ics": "20270418",
        "titulo": "Torneo Nacional de Rápidas",
        "modalidad": "Rápidas",
        "detalle": "Campeonato nacional de ajedrez activo a una sola jornada intensiva.",
        "icono": "⏱️"
    },
    {
        "mes": "MAYO",
        "orden_mes": 5,
        "fechas": "07, 08, 09 y 14, 15, 16 de Mayo, 2027",
        "fecha_ics": "20270507",
        "titulo": "Gran Torneo Abierto",
        "modalidad": "Clásico / Estándar",
        "detalle": "Dos fines de semana de competencia abierta para todas las categorías.",
        "icono": "🏁"
    },
    {
        "mes": "JUNIO",
        "orden_mes": 6,
        "fechas": "Junio 2027 (Fecha por confirmar)",
        "fecha_ics": "20270615",
        "titulo": "Torneo Leyendas vs. Prodigios",
        "modalidad": "Match Especial 10 vs. 10",
        "detalle": "Duelo generacional de exhibición y alto rendimiento: 10 maestros contra 10 talentos juveniles.",
        "icono": "⚔️"
    }
]

def generar_archivo_ics(titulo, fecha_str, descripcion):
    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Escuela Nacional de Talento Kendry Moron//ES
BEGIN:VEVENT
DTSTART;VALUE=DATE:{fecha_str}
SUMMARY:{titulo} - Escuela Kendry Morón
DESCRIPTION:{descripcion} | Sede: Escuela Nacional de Talento Kendry Morón, Santo Domingo.
LOCATION:Escuela Nacional de Talento Kendry Morón, Santo Domingo, República Dominicana
END:VEVENT
END:VCALENDAR"""
    return ics_content

# -----------------------------------------------------------------------------
# CÁLCULO DE CUENTA REGRESIVA AL TORNEO NACIONAL (27 NOV 2026)
# -----------------------------------------------------------------------------
tz_rd = timezone(timedelta(hours=-4))
ahora_rd = datetime.now(tz_rd)
fecha_objetivo = datetime(2026, 11, 27, 9, 0, 0, tzinfo=tz_rd)
diferencia = fecha_objetivo - ahora_rd

if diferencia.total_seconds() > 0:
    dias = diferencia.days
    horas, rem = divmod(diferencia.seconds, 3600)
    minutos, segundos = divmod(rem, 60)
else:
    dias, horas, minutos, segundos = 0, 0, 0, 0

# -----------------------------------------------------------------------------
# SECCIÓN 1: HERO BANNER INSTITUCIONAL
# -----------------------------------------------------------------------------
logo_html = get_logo_html()

st.markdown(f"""
<div class="hero-wrapper">
    <div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 24px;">
        <div style="flex: 0 0 auto; text-align: center;">
            {logo_html}
        </div>
        <div style="flex: 1 1 420px;">
            <div class="hero-badge">♟️ Santo Domingo, República Dominicana • Válido Rating FIDE</div>
            <h1 class="hero-title">ESCUELA NACIONAL DE TALENTO <span>KENDRY MORÓN</span></h1>
            <div class="hero-slogan">★ FORMAMOS TALENTO, INSPIRAMOS CAMPEONES ★</div>
            <p style="color: #CBD5E1; margin-top: 12px; font-size: 1rem; max-width: 720px;">
                Plataforma oficial de torneos, formación competitiva de alto rendimiento y calendario institucional. 
                Preparación continua rumbo a los <strong>XXIII Juegos Centroamericanos y del Caribe de la Juventud 2027</strong>.
            </p>
        </div>
        <div style="flex: 1 1 280px; background: rgba(0,0,0,0.45); border: 1px solid rgba(255,255,255,0.1); padding: 18px; border-radius: 16px;">
            <div style="font-size: 0.8rem; color: #F5C518; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; text-align: center;">
                ⏳ Próximo Gran Evento: Nacional Juvenil
            </div>
            <div class="countdown-grid">
                <div class="count-box">
                    <div class="count-num">{dias}</div>
                    <div class="count-label">Días</div>
                </div>
                <div class="count-box">
                    <div class="count-num">{horas}</div>
                    <div class="count-label">Horas</div>
                </div>
                <div class="count-box">
                    <div class="count-num">{minutos}</div>
                    <div class="count-label">Min</div>
                </div>
                <div class="count-box">
                    <div class="count-num">{segundos}</div>
                    <div class="count-label">Seg</div>
                </div>
            </div>
            <div style="text-align: center; font-size: 0.82rem; color: #94A3B8; margin-top: 10px;">
                📅 27 al 29 de Noviembre • Sede Kendry Morón
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# NAVEGACIÓN POR PESTAÑAS DE ALTO IMPACTO
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "🏆 TORNEO NACIONAL JUVENIL (27-29 NOV)",
    "📅 CALENDARIO DE TORNEOS 2027",
    "📝 INSCRIPCIÓN Y CONTACTO DIRECTO"
])

# =============================================================================
# PESTAÑA 1: TORNEO NACIONAL POR CATEGORÍAS (27 AL 29 DE NOVIEMBRE)
# =============================================================================
with tab1:
    st.markdown("""
    <div class="featured-card">
        <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 12px;">
            <div>
                <span style="background:#F5C518; color:#0B0D10; font-weight:800; padding:4px 12px; border-radius:6px; font-size:0.85rem;">
                    EVENTO INSIGNIA • VÁLIDO PARA RATING FIDE
                </span>
                <h2 style="font-size: 2.3rem; margin: 10px 0 4px 0; color: #FFFFFF;">
                    TORNEO NACIONAL POR CATEGORÍAS JUVENILES
                </h2>
                <p style="color: #CBD5E1; margin: 0;">
                    📍 <strong>Lugar de Juego:</strong> Escuela Nacional de Talento Kendry Morón, Santo Domingo.
                </p>
            </div>
            <div style="text-align: right; background: rgba(200,16,46,0.18); border: 1px solid #C8102E; padding: 12px 18px; border-radius: 12px;">
                <div style="font-family: 'Oswald', sans-serif; font-size: 1.5rem; color: #F5C518;">27 AL 29 DE NOVIEMBRE</div>
                <div style="font-size: 0.9rem; color: #FFFFFF;">⏱️ Ritmo: 1h 30m + 30s • 5 Rondas</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_cat, col_prem = st.columns([1.05, 1.15], gap="large")

    with col_cat:
        st.markdown("### 🎯 Categorías Oficiales")
        st.markdown("""
        <div class="cat-pill">
            <div class="sub">♟️ SUB <span>17</span></div>
            <div class="mod">ABSOLUTO Y FEMENINO</div>
        </div>
        <div class="cat-pill">
            <div class="sub">♞ SUB <span>15</span></div>
            <div class="mod">ABSOLUTO</div>
        </div>
        <div class="cat-pill">
            <div class="sub">♝ SUB <span>13</span></div>
            <div class="mod">ABSOLUTO</div>
        </div>
        <div class="cat-pill">
            <div class="sub">♜ SUB <span>11</span></div>
            <div class="mod">ABSOLUTO</div>
        </div>
        """, unsafe_allow_html=True)

        st.info("🎓 **Beneficio Especial:** Entrenamiento continuo incluido para todos los primeros lugares con miras al Campeonato Centroamericano.")

    with col_prem:
        st.markdown("### 🏅 Premiación Oficial")
        st.markdown("""
        <div class="prize-box">
            <div style="font-size: 1.15rem; font-weight: 800; color: #F5C518;">🥇 1ER LUGAR — TROFEO + VIAJE INTERNACIONAL</div>
            <div style="color: #E2E8F0; font-size: 0.92rem; margin-top: 4px;">
                Boletos aéreos de ida y vuelta para los <strong>XXIII Juegos Centroamericanos y del Caribe de la Juventud 2027</strong>.
            </div>
        </div>
        <div class="prize-box" style="border-color: rgba(255,255,255,0.2); background: rgba(255,255,255,0.04);">
            <div style="font-size: 1.1rem; font-weight: 800; color: #FFFFFF;">🥈 2DO LUGAR — MEDALLA + TABLERO PROFESIONAL</div>
            <div style="color: #CBD5E1; font-size: 0.92rem; margin-top: 4px;">
                Tablero de madera preciosa con piezas oficiales <strong>Staunton</strong>.
            </div>
        </div>
        <div class="prize-box" style="border-color: rgba(255,255,255,0.2); background: rgba(255,255,255,0.04);">
            <div style="font-size: 1.1rem; font-weight: 800; color: #FFFFFF;">🥉 3ER LUGAR — MEDALLA + TABLERO DGT</div>
            <div style="color: #CBD5E1; font-size: 0.92rem; margin-top: 4px;">
                Tablero de madera preciosa con piezas electrónicas <strong>DGT</strong>.
            </div>
        </div>
        """, unsafe_allow_html=True)

        msg_nacional = urllib.parse.quote("Hola CM Michel de Jesús, deseo inscribir a un jugador en el Torneo Nacional por Categorías (27-29 de Noviembre) en la Escuela Kendry Morón.")
        st.markdown(f"""
        <a href="https://wa.me/18297732231?text={msg_nacional}" target="_blank" class="wa-btn-gold">
            📲 INSCRIBIRSE VÍA WHATSAPP — CM MICHEL DE JESÚS (829.773.2231)
        </a>
        """, unsafe_allow_html=True)

# =============================================================================
# PESTAÑA 2: CALENDARIO DE TORNEOS 2027
# =============================================================================
with tab2:
    st.markdown("### 📅 Temporada Oficial 2027 — Primer Semestre")
    
    f1, f2, f3 = st.columns([1, 1, 1])
    with f1:
        mes_sel = st.selectbox("Filtrar por Mes", ["Todos"] + sorted(list(set(t["mes"] for t in TORNEOS_2027)), key=lambda x: ["ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO"].index(x)))
    with f2:
        mod_sel = st.selectbox("Filtrar por Modalidad", ["Todas"] + sorted(list(set(t["modalidad"] for t in TORNEOS_2027))))
    with f3:
        st.metric("Torneos Programados (Ene-Jun 2027)", f"{len(TORNEOS_2027)} Eventos", "Sede Santo Domingo")

    eventos_filtrados = [
        t for t in TORNEOS_2027
        if (mes_sel == "Todos" or t["mes"] == mes_sel)
        and (mod_sel == "Todas" or t["modalidad"] == mod_sel)
    ]

    cols = st.columns(3, gap="medium")
    for idx, ev in enumerate(eventos_filtrados):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="event-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="event-month-badge">{ev['mes']} 2027</span>
                    <span style="font-size:1.5rem;">{ev['icono']}</span>
                </div>
                <div class="event-date">🗓️ {ev['fechas']}</div>
                <div class="event-title">{ev['titulo']}</div>
                <div style="color:#FF4D6D; font-size:0.8rem; font-weight:700; text-transform:uppercase; margin-bottom:6px;">
                    Modalidad: {ev['modalidad']}
                </div>
                <div class="event-detail">{ev['detalle']}</div>
            </div>
            """, unsafe_allow_html=True)

            # Botón para agendar en el calendario del usuario
            ics_data = generar_archivo_ics(ev["titulo"], ev["fecha_ics"], ev["detalle"])
            st.download_button(
                label=f"➕ Agendar {ev['titulo'][:22]}...",
                data=ics_data,
                file_name=f"kendry_moron_{ev['mes'].lower()}_{idx}.ics",
                mime="text/calendar",
                key=f"ics_{idx}",
                use_container_width=True
            )
            st.markdown("<div style='margin-bottom:14px;'></div>", unsafe_allow_html=True)

# =============================================================================
# PESTAÑA 3: FORMULARIO DE PRE-INSCRIPCIÓN RÁPIDA
# =============================================================================
with tab3:
    st.markdown("### 📝 Registro Rápido de Jugadores")
    st.write("Completa los datos del atleta para generar automáticamente tu ficha de inscripción directa con la coordinación del torneo.")

    with st.form("form_inscripcion"):
        c1, c2 = st.columns(2)
        with c1:
            nombre = st.text_input("Nombre Completo del Jugador *", placeholder="Ej. Ángel Sebastián Lara")
            fecha_nac = st.date_input("Fecha de Nacimiento", value=datetime(2012, 5, 15))
            id_fide = st.text_input("ID FIDE (Opcional)", placeholder="Ej. 6401234")
        with c2:
            torneo_interes = st.selectbox(
                "Torneo a Inscribir *",
                ["Torneo Nacional por Categorías (27-29 Noviembre)"] + [f"{t['titulo']} ({t['mes']} 2027)" for t in TORNEOS_2027]
            )
            categoria = st.selectbox(
                "Categoría / Rama *",
                ["Sub-17 Absoluto", "Sub-17 Femenino", "Sub-15 Absoluto", "Sub-13 Absoluto", "Sub-11 Absoluto", "Abierto / Libre"]
            )
            telefono = st.text_input("Teléfono / WhatsApp de Contacto *", placeholder="Ej. 809-555-0199")

        enviado = st.form_submit_button("✅ GENERAR FICHA DE INSCRIPCIÓN", use_container_width=True)

    if enviado:
        if not nombre or not telefono:
            st.error("⚠️ Por favor completa el nombre del jugador y un teléfono de contacto.")
        else:
            resumen_wa = (
                f"*NUEVA PRE-INSCRIPCIÓN - ESCUELA KENDRY MORÓN*%0A"
                f"• *Jugador:* {urllib.parse.quote(nombre)}%0A"
                f"• *Torneo:* {urllib.parse.quote(torneo_interes)}%0A"
                f"• *Categoría:* {urllib.parse.quote(categoria)}%0A"
                f"• *Nacimiento:* {fecha_nac}%0A"
                f"• *ID FIDE:* {urllib.parse.quote(id_fide if id_fide else 'Sin ID FIDE')}%0A"
                f"• *Contacto:* {urllib.parse.quote(telefono)}"
            )
            st.success(f"✅ Ficha generada para **{nombre}**. Haz clic abajo para confirmarla por WhatsApp con el **CM Michel de Jesús**:")
            st.markdown(f"""
            <a href="https://wa.me/18297732231?text={resumen_wa}" target="_blank" class="wa-btn">
                📲 ENVIAR INSCRIPCIÓN POR WHATSAPP AHORA (829.773.2231)
            </a>
            """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PIE DE PÁGINA INSTITUCIONAL
# -----------------------------------------------------------------------------
st.markdown("""
<hr style="border-color: rgba(255,255,255,0.1); margin-top: 3rem;">
<div style="text-align: center; color: #94A3B8; font-size: 0.85rem; padding-bottom: 1.5rem;">
    <strong>ESCUELA NACIONAL DE TALENTO KENDRY MORÓN</strong> • Santo Domingo, República Dominicana<br>
    Coordinación de Torneos: CM Michel de Jesús (829.773.2231) • <em>Formamos Talento, Inspiramos Campeones</em>
</div>
""", unsafe_allow_html=True)