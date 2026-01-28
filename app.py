import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 1. PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Eyeball Scout | Pro Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed" # Yan paneli kapalı başlatıyoruz, odak ana ekranda
)

# 2. ULTRA PREMIUM CSS (GRADIENT & GLASSMORPHISM)
# ---------------------------------------------------------
st.markdown("""
    <style>
        /* IMPORT FONT */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        
        /* GLOBAL RESET */
        * { font-family: 'Inter', sans-serif !important; }
        .stApp { background-color: #050505; color: #ffffff; }

        /* GRADIENT TEXT */
        .gradient-text {
            font-weight: 800;
            background: -webkit-linear-gradient(45deg, #00FFA3, #00D2FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        h1, h2, h3 {
            font-weight: 800 !important;
            background: -webkit-linear-gradient(45deg, #4ADE80, #3B82F6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
        }

        /* INPUT KUTULARI (Filtreler için) */
        .stSelectbox div[data-baseweb="select"] > div,
        .stMultiSelect div[data-baseweb="select"] > div {
            background-color: #111111 !important;
            border: 1px solid #333333 !important;
            border-radius: 12px !important;
            color: white !important;
        }
        
        /* Dropdown Menü */
        ul[data-baseweb="menu"] {
            background-color: #000 !important;
            border: 1px solid #333 !important;
        }

        /* METRIC CARDS */
        div[data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 15px;
            text-align: center;
        }
        div[data-testid="stMetricValue"] {
            color: #00FFA3 !important;
            font-weight: 800;
            font-size: 24px !important;
        }
        div[data-testid="stMetricLabel"] { color: #888; font-size: 13px; }

        /* TABS */
        .stTabs [data-baseweb="tab-list"] {
            gap: 20px;
            background-color: transparent;
            border-bottom: 1px solid #333;
            margin-bottom: 20px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            background-color: transparent;
            border: none;
            color: #666;
            font-size: 16px;
            font-weight: 600;
        }
        .stTabs [aria-selected="true"] {
            background-color: transparent;
            color: #00FFA3 !important;
            border-bottom: 3px solid #00FFA3;
        }

        /* SIDEBAR */
        [data-testid="stSidebar"] { 
            background-color: #000000; 
            border-right: 1px solid #222; 
        }
        
        header {visibility: hidden;}
        .block-container { padding-top: 2rem; }
        
        td { font-size: 14px !important; color: #ddd !important; border-bottom: 1px solid #222 !important; }

    </style>
""", unsafe_allow_html=True)

# 3. DATA LOADING
# ---------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("eyeball_streamlit_final.csv")
    df['Display_Name'] = df['Player'] + " (" + df['Season'].astype(str) + ") - " + df['Squad']
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("ERROR: CSV file not found.")
    st.stop()

# COLOR MAP
role_color_map = {
    "Inverted Winger / Dribbler": "#FF2A6D",       
    "Elite Speedster / Direct Winger": "#D300C5",  
    "Poacher / Penalty Box Striker": "#FF9600",    
    "Versatile Forward / Second Striker": "#F5D300", 
    "Target Man / Aerial Threat": "#B800F5",       
    "Pressing Forward": "#00F562",                 
    "Technical Hub / Deep Playmaker": "#05D9E8",   
    "Progressive Passer / Controller": "#0056F5",  
    "Physical Ball Carrier": "#6500F5",            
    "Defensive Midfielder / Anchor": "#8F4300",    
    "Wide Midfielder / Defensive Winger": "#00F5A0", 
    "Utility Player / Workhorse": "#777777",       
    "Deep Distributor / Ball Playing CB": "#00E0C6", 
    "Stopper / No-Nonsense Defender": "#8F001A",   
    "Central Defender (Standard)": "#00188F",      
    "Commanding Center Back": "#FFFFFF"            
}

# 4. SIDEBAR (SADECE LOGO)
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("<h1 style='font-size: 3rem; margin-bottom: 0;'>EYEBALL<span style='color:#00FFA3'>.</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666; font-size: 0.9rem; margin-top: -10px;'>AI SCOUTING ANALYTICS</p>", unsafe_allow_html=True)
    st.info("ℹ️ Filters are now located above the 3D map for easier access.")

# 5. MAIN LAYOUT
# ---------------------------------------------------------
st.markdown('<h1 style="font-size: 3rem; margin-bottom: 0;">SCOUTING INTELLIGENCE</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#888; margin-bottom: 30px; font-size: 1.1rem;">Next-generation 3D clustering & performance analysis.</p>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🌍 3D EXPLORATION & FILTERS", "⚔️ PLAYER COMPARISON"])

# --- TAB 1: 3D EXPLORATION (FILTERS MOVED HERE) ---
with tab1:
    
    # --- A. CONTROL CENTER (Filtreler Buraya Taşındı) ---
    st.markdown("### 🎛️ DATA CONTROLS")
    
    # 4 Sütunlu Filtre Yapısı
    c1, c2, c3, c4 = st.columns(4)
    
    # 1. Sezon
    all_seasons = sorted(df['Season'].unique(), reverse=True)
    selected_seasons = c1.multiselect("📅 SEASON", all_seasons, default=all_seasons[:1])
    
    # Veriyi Sezona Göre Daralt
    if selected_seasons:
        df_season = df[df['Season'].isin(selected_seasons)]
    else:
        df_season = df.copy() # Seçim yoksa hepsi
        
    # 2. Takım
    teams = sorted(df_season['Squad'].unique())
    selected_teams = c2.multiselect("🛡️ SQUAD", teams)
    
    # 3. Mevki
    positions = sorted(df_season['General_Position'].unique())
    selected_pos = c3.multiselect("📍 POSITION", positions)
    
    # 4. Rol (Dinamik)
    if selected_pos:
        roles = sorted(df_season[df_season['General_Position'].isin(selected_pos)]['Role_Name'].unique())
    else:
        roles = sorted(df_season['Role_Name'].unique())
    selected_roles = c4.multiselect("🧠 ROLE", roles)

    # --- FİLTRE MOTORU ---
    final_df = df_season.copy()
    if selected_teams: final_df = final_df[final_df['Squad'].isin(selected_teams)]
    if selected_pos: final_df = final_df[final_df['General_Position'].isin(selected_pos)]
    if selected_roles: final_df = final_df[final_df['Role_Name'].isin(selected_roles)]

    st.markdown("---")

    # --- B. 3D VISUALIZATION ---
    col_search, col_stats = st.columns([1, 4])
    
    with col_search:
        # Arama kutusu sadece filtrelenen oyuncuları gösterir
        search_list = ["Select..."] + sorted(final_df['Display_Name'].unique().tolist())
        selected_player_search = st.selectbox("ZOOM TO PLAYER", search_list)
        
        # Filtre Sonucu Bilgi Kartı
        st.markdown(f"""
        <div style="background-color: #111; padding: 15px; border-radius: 12px; border: 1px solid #333; margin-top: 20px;">
            <span style="color: #888; font-size: 0.8rem;">ACTIVE PLAYERS</span><br>
            <b style="color: #00FFA3; font-size: 1.8rem;">{len(final_df)}</b>
        </div>
        """, unsafe_allow_html=True)

        if selected_player_search != "Select...":
            p_info = df[df['Display_Name'] == selected_player_search].iloc[0]
            st.markdown(f"""
            <div style="background-color: #111; padding: 20px; border-radius: 12px; border: 1px solid #333; margin-top: 10px;">
                <h3 style="margin:0; font-size: 1.2rem;">{p_info['Player']}</h3>
                <p style="color: #666; margin:0;">{p_info['Squad']}</p>
                <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #333;">
                    <span style="color: #888;">AI Role: <b style="color: #fff;">{p_info['Role_Name']}</b></span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_stats:
        if not final_df.empty:
            fig = px.scatter_3d(
                final_df, x='x', y='y', z='z',
                color='Role_Name', color_discrete_map=role_color_map,
                hover_name='Display_Name',
                hover_data=['Age', 'Goals', 'Assists', 'Minutes'],
                opacity=0.9, size_max=15, 
                title=""
            )
            fig.update_layout(
                scene=dict(
                    xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
                    bgcolor='rgba(0,0,0,0)'
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, b=0, t=0),
                height=600,
                legend=dict(
                    x=0, y=1, 
                    font=dict(color="#aaa", size=10),
                    bgcolor="rgba(0,0,0,0.5)"
                )
            )
            
            if selected_player_search != "Select...":
                p_data = df[df['Display_Name'] == selected_player_search]
                if not p_data.empty:
                    fig.add_trace(go.Scatter3d(
                        x=p_data['x'], y=p_data['y'], z=p_data['z'],
                        mode='markers', 
                        marker=dict(size=35, color='#00FFA3', symbol='diamond', line=dict(width=3, color='white')),
                        name='SELECTED', hoverinfo='text', hovertext=selected_player_search
                    ))
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No players match the selected filters.")

# --- TAB 2: PLAYER COMPARISON (UNCHANGED LOGIC) ---
with tab2:
    col_sel1, col_sel2 = st.columns(2)
    all_players = sorted(df['Display_Name'].unique().tolist())
    
    with col_sel1:
        p1_name = st.selectbox("PLAYER 1", all_players, index=0)
    with col_sel2:
        p2_name = st.selectbox("PLAYER 2", all_players, index=min(10, len(all_players)-1))

    if p1_name and p2_name:
        p1 = df[df['Display_Name'] == p1_name].iloc[0]
        p2 = df[df['Display_Name'] == p2_name].iloc[0]
        
        st.markdown("---")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("PLAYER 1", p1['Player'], f"{int(p1['Age'])}")
        c2.metric("TEAM", p1['Squad'], p1['Season'])
        c3.metric("PLAYER 2", p2['Player'], f"{int(p2['Age'])}")
        c4.metric("TEAM", p2['Squad'], p2['Season'])

        st.markdown("<br>", unsafe_allow_html=True)

        col_radar, col_table = st.columns([2, 3])
        
        with col_radar:
            st.markdown("<h3>SKILL RADAR</h3>", unsafe_allow_html=True)
            radar_metrics = ['Goals', 'Assists', 'Shots', 'SoT', 'Dribbles_Succ', 'Prg_Pass_Dist', 'Tackles', 'Interceptions', 'Blocks']
            
            v1_raw = [p1.get(m, 0) for m in radar_metrics]
            v2_raw = [p2.get(m, 0) for m in radar_metrics]
            v1_norm, v2_norm = [], []
            
            for val1, val2 in zip(v1_raw, v2_raw):
                mx = max(val1, val2)
                if mx == 0: mx = 1
                v1_norm.append(val1/mx)
                v2_norm.append(val2/mx)
                
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=v1_norm, theta=radar_metrics, fill='toself', name=p1['Player'],
                text=v1_raw, hoverinfo="text+theta+name", 
                line_color='#00FFA3', fillcolor='rgba(0, 255, 163, 0.1)'
            ))
            fig_radar.add_trace(go.Scatterpolar(
                r=v2_norm, theta=radar_metrics, fill='toself', name=p2['Player'],
                text=v2_raw, hoverinfo="text+theta+name", 
                line_color='#00D2FF', fillcolor='rgba(0, 210, 255, 0.1)'
            ))
            
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=False), bgcolor='#090909'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=20, b=20, l=20, r=20),
                height=400,
                showlegend=True,
                legend=dict(font=dict(color="white"), orientation="h")
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        with col_table:
            st.markdown("<h3>STATS MATRIX</h3>", unsafe_allow_html=True)
            compare_metrics = {
                'ATTACK': ['Goals', 'Assists', 'Shots', 'SoT', 'npxG_p90', 'xA_p90'],
                'PLAYMAKING': ['Prg_Pass_Dist', 'Prg_Carry_Dist', 'GCA', 'SCA', 'Pass_Cmp_Pct'],
                'DEFENSE': ['Tackles', 'Interceptions', 'Blocks'],
                'INFO': ['Minutes', 'Age', 'Role_Probability']
            }
            rows = []
            for cat, metrics in compare_metrics.items():
                for m in metrics:
                    rows.append({
                        "Category": cat, "Metric": m,
                        f"{p1['Player']}": p1.get(m, 0),
                        f"{p2['Player']}": p2.get(m, 0)
                    })
            comp_df = pd.DataFrame(rows)
            
            def smart_format(x):
                try: return f"{x:.0f}" if isinstance(x, (int, float)) and x % 1 == 0 else f"{x:.2f}"
                except: return x

            def highlight(row):
                c1, c2 = row.index[2], row.index[3]
                v1, v2 = row[c1], row[c2]
                styles = ['' for _ in row]
                win_css = 'color: #00FFA3; font-weight: 700; background-color: rgba(0, 255, 163, 0.05); border-radius: 4px;'
                lose_css = 'color: #555; font-weight: 400; opacity: 0.5;'
                try:
                    val1, val2 = float(v1), float(v2)
                    if val1 > val2: styles[2], styles[3] = win_css, lose_css
                    elif val2 > val1: styles[2], styles[3] = lose_css, win_css
                except: pass
                return styles

            st.dataframe(comp_df.style.apply(highlight, axis=1).format(smart_format, subset=comp_df.columns[2:]), use_container_width=True, height=500, hide_index=True)

# FOOTER
st.markdown("---")
st.markdown("""<div style="text-align: center; color: #444; font-size: 0.8rem;">EYEBALL INTELLIGENCE © 2026</div>""", unsafe_allow_html=True)

