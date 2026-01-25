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
    initial_sidebar_state="expanded"
)

# 2. ULTRA SMOOTH CSS (YENİ TASARIM)
# ---------------------------------------------------------
st.markdown("""
    <style>
        /* IMPORT GOOGLE FONT 'INTER' */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* --- GENERAL SETTINGS --- */
        * { font-family: 'Inter', sans-serif !important; }
        
        .stApp { 
            background-color: #0B0E11; 
            color: #E0E0E0; 
        }
        
        /* --- SMOOTH TABS (YUMUŞAK SEKME TASARIMI) --- */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: transparent;
            padding-bottom: 5px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 55px;
            background-color: #151A21;
            border-radius: 16px 16px 0px 0px; /* Üst köşeler yuvarlak */
            border: 1px solid #2A2F3A;
            border-bottom: none;
            color: #9CA3AF;
            font-size: 15px;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #1F252E;
            color: #4ADE80; /* Neon Yeşil Yazı */
            font-weight: 600;
            border-top: 2px solid #4ADE80;
        }

        /* --- SMOOTH CARDS & METRICS --- */
        div[data-testid="stMetric"] {
            background-color: #1F252E;
            border: 1px solid #2F3642;
            padding: 20px;
            border-radius: 16px; /* Daha yuvarlak */
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        }
        
        /* --- INPUT FIELDS (SEÇİM KUTULARI) --- */
        .stSelectbox div[data-baseweb="select"] > div,
        .stMultiSelect div[data-baseweb="select"] > div {
            background-color: #151A21;
            border-color: #2F3642;
            border-radius: 12px; /* Inputlar da yuvarlak */
            color: white;
        }
        
        /* --- SIDEBAR --- */
        [data-testid="stSidebar"] { 
            background-color: #0F1216; 
            border-right: 1px solid #1F252E; 
        }

        /* --- HEADERS --- */
        .main-title {
            font-size: 2.8rem;
            font-weight: 800;
            letter-spacing: -1px;
            background: linear-gradient(90deg, #4ADE80, #3B82F6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* HIDE DEFAULT STREAMLIT HEADER */
        header {visibility: hidden;}
        .block-container { padding-top: 2rem; padding-bottom: 3rem; }

        /* --- TABLE STYLING --- */
        td { font-size: 14px !important; padding: 12px !important; }
        thead tr th:first-child { display:none }
        tbody th { display:none }

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

# HIGH CONTRAST COLOR MAP
role_color_map = {
    "Inverted Winger / Dribbler": "#EF4444",       # Red
    "Elite Speedster / Direct Winger": "#EC4899",  # Pink
    "Poacher / Penalty Box Striker": "#F97316",    # Orange
    "Versatile Forward / Second Striker": "#EAB308", # Yellow
    "Target Man / Aerial Threat": "#A855F7",       # Purple
    "Pressing Forward": "#84CC16",                 # Lime
    "Technical Hub / Deep Playmaker": "#06B6D4",   # Cyan
    "Progressive Passer / Controller": "#3B82F6",  # Blue
    "Physical Ball Carrier": "#6366F1",            # Indigo
    "Defensive Midfielder / Anchor": "#78350F",    # Amber
    "Wide Midfielder / Defensive Winger": "#10B981", # Emerald
    "Utility Player / Workhorse": "#6B7280",       # Gray
    "Deep Distributor / Ball Playing CB": "#14B8A6", # Teal
    "Stopper / No-Nonsense Defender": "#991B1B",   # Dark Red
    "Central Defender (Standard)": "#1E3A8A",      # Dark Blue
    "Commanding Center Back": "#F3F4F6"            # White
}

# 4. SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("<h2 style='color: #4ADE80; margin:0; font-weight:800; letter-spacing:-1px;'>EYEBALL.</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #6B7280; font-size: 0.8rem; margin-bottom: 20px;'>AI SCOUTING ANALYTICS</p>", unsafe_allow_html=True)
    
    # Filters
    all_seasons = sorted(df['Season'].unique(), reverse=True)
    selected_seasons = st.multiselect("📅 Season", all_seasons, default=all_seasons[:1])

    if selected_seasons:
        df_filtered_season = df[df['Season'].isin(selected_seasons)]
    else:
        df_filtered_season = df.copy()

    teams = sorted(df_filtered_season['Squad'].unique())
    selected_teams = st.multiselect("🛡️ Squad", teams)

    positions = sorted(df_filtered_season['General_Position'].unique())
    selected_pos = st.multiselect("📍 Position", positions)

    if selected_pos:
        roles = sorted(df_filtered_season[df_filtered_season['General_Position'].isin(selected_pos)]['Role_Name'].unique())
    else:
        roles = sorted(df_filtered_season['Role_Name'].unique())
    selected_roles = st.multiselect("🧠 Role", roles)

    # Apply Filters
    final_df = df_filtered_season.copy()
    if selected_teams: final_df = final_df[final_df['Squad'].isin(selected_teams)]
    if selected_pos: final_df = final_df[final_df['General_Position'].isin(selected_pos)]
    if selected_roles: final_df = final_df[final_df['Role_Name'].isin(selected_roles)]
    
    st.markdown("---")
    st.caption(f"📊 Players Loaded: **{len(final_df)}**")


# 5. MAIN LAYOUT
# ---------------------------------------------------------
st.markdown('<div class="main-title">Scouting Intelligence</div>', unsafe_allow_html=True)
st.markdown('<p style="color:#9CA3AF; margin-bottom: 30px;">Advanced 3D clustering & head-to-head analysis platform.</p>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🌍 3D EXPLORATION", "⚔️ PLAYER COMPARISON"])

# --- TAB 1: 3D EXPLORATION ---
with tab1:
    col_search, col_space = st.columns([1, 3])
    with col_search:
        search_list = ["Select..."] + sorted(final_df['Display_Name'].unique().tolist())
        selected_player_search = st.selectbox("Zoom to Player", search_list, label_visibility="collapsed")
        
        # Player Quick Info Card
        if selected_player_search != "Select...":
            p_info = df[df['Display_Name'] == selected_player_search].iloc[0]
            st.markdown(f"""
            <div style="background-color: #1F252E; padding: 20px; border-radius: 16px; border: 1px solid #2F3642; margin-top: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.2);">
                <h3 style="color: #4ADE80; margin:0; font-size: 1.4rem; font-weight: 700;">{p_info['Player']}</h3>
                <p style="color: #9CA3AF; margin:0; font-size: 0.9rem;">{p_info['Squad']}</p>
                <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #2F3642;">
                    <span style="color: #E0E0E0; font-size: 0.9rem;">Role: <br><b style="color: #FFFFFF;">{p_info['Role_Name']}</b></span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    if not final_df.empty:
        fig = px.scatter_3d(
            final_df, x='x', y='y', z='z',
            color='Role_Name', color_discrete_map=role_color_map,
            hover_name='Display_Name',
            hover_data=['Age', 'Goals', 'Assists', 'Minutes'],
            opacity=0.8, size_max=14, 
            title=""
        )
        # Clean Plotly Layout
        fig.update_layout(
            scene=dict(
                xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, b=0, t=0),
            height=650,
            legend=dict(
                x=0, y=1, 
                font=dict(color="white", size=11, family="Inter"),
                bgcolor="rgba(0,0,0,0.5)"
            )
        )
        
        if selected_player_search != "Select...":
            p_data = df[df['Display_Name'] == selected_player_search]
            if not p_data.empty:
                fig.add_trace(go.Scatter3d(
                    x=p_data['x'], y=p_data['y'], z=p_data['z'],
                    mode='markers', 
                    marker=dict(size=30, color='#4ADE80', symbol='diamond', line=dict(width=3, color='white')),
                    name='SELECTED', hoverinfo='text', hovertext=selected_player_search
                ))
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No players found with current filters.")

# --- TAB 2: PLAYER COMPARISON ---
with tab2:
    col_sel1, col_sel2 = st.columns(2)
    
    all_players = sorted(df['Display_Name'].unique().tolist())
    
    with col_sel1:
        p1_name = st.selectbox("1st Player", all_players, index=0)
    with col_sel2:
        p2_name = st.selectbox("2nd Player", all_players, index=min(10, len(all_players)-1))

    if p1_name and p2_name:
        p1 = df[df['Display_Name'] == p1_name].iloc[0]
        p2 = df[df['Display_Name'] == p2_name].iloc[0]
        
        st.markdown("---")

        # 1. INFO CARDS
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Player 1", p1['Player'], f"{int(p1['Age'])} yo")
        c2.metric("Team", p1['Squad'], p1['Season'])
        c3.metric("Player 2", p2['Player'], f"{int(p2['Age'])} yo")
        c4.metric("Team", p2['Squad'], p2['Season'])

        st.markdown("<br>", unsafe_allow_html=True)

        # 2. RADAR & TABLE
        col_radar, col_table = st.columns([2, 3])
        
        with col_radar:
            st.markdown("##### ⚡ Skill Profile (Relative)")
            radar_metrics = ['Goals', 'Assists', 'Shots', 'SoT', 'Dribbles_Succ', 'Prg_Pass_Dist', 'Tackles', 'Interceptions', 'Blocks']
            
            # Normalization
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
                line_color='#4ADE80', fillcolor='rgba(74, 222, 128, 0.2)'
            ))
            fig_radar.add_trace(go.Scatterpolar(
                r=v2_norm, theta=radar_metrics, fill='toself', name=p2['Player'],
                text=v2_raw, hoverinfo="text+theta+name", 
                line_color='#3B82F6', fillcolor='rgba(59, 130, 246, 0.2)'
            ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=False),
                    bgcolor='#151A21' # Radar background match
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=20, b=20, l=20, r=20),
                height=400,
                showlegend=True,
                legend=dict(font=dict(color="white"), orientation="h")
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        with col_table:
            st.markdown("##### 📋 Detailed Comparison")
            
            # Data Preparation
            compare_metrics = {
                'Attacking': ['Goals', 'Assists', 'Shots', 'SoT', 'npxG_p90', 'xA_p90'],
                'Playmaking': ['Prg_Pass_Dist', 'Prg_Carry_Dist', 'GCA', 'SCA', 'Pass_Cmp_Pct'],
                'Defencing': ['Tackles', 'Interceptions', 'Blocks'],
                'General': ['Minutes', 'Age', 'Role_Probability']
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
            
            # Formatter
            def smart_format(x):
                try:
                    if isinstance(x, (int, float)):
                        return f"{x:.0f}" if x % 1 == 0 else f"{x:.2f}"
                    return x
                except: return x

            # Highlight
            def highlight(row):
                c1, c2 = row.index[2], row.index[3]
                v1, v2 = row[c1], row[c2]
                styles = ['' for _ in row]
                
                win_css = 'color: #4ADE80; font-weight: 700; background-color: rgba(74, 222, 128, 0.05); border-radius: 6px;'
                lose_css = 'color: #6B7280; font-weight: 400; opacity: 0.6;'
                
                try:
                    val1, val2 = float(v1), float(v2)
                    if val1 > val2:
                        styles[2], styles[3] = win_css, lose_css
                    elif val2 > val1:
                        styles[2], styles[3] = lose_css, win_css
                except: pass
                return styles

            st.dataframe(
                comp_df.style.apply(highlight, axis=1).format(smart_format, subset=comp_df.columns[2:]),
                use_container_width=True,
                height=500,
                hide_index=True
            )

# FOOTER
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; font-size: 0.9rem;">
    Eyeball Scout | 
    <span style="color: #4ADE80;">Position & Role Analysis</span> | 
    UMAP & CA
</div>
""", unsafe_allow_html=True)

