import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 1. SAYFA AYARLARI
# ---------------------------------------------------------
st.set_page_config(
    page_title="Eyeball Scout Pro",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. VERİ YÜKLEME VE HAZIRLIK
# ---------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("eyeball_streamlit_final.csv")
    
    # UI İÇİN ÖZEL SÜTUN: "Oyuncu Adı (Sezon) - Takım"
    # Bu sayede listede aynı isimli oyuncular karışmayacak.
    df['Display_Name'] = df['Player'] + " (" + df['Season'].astype(str) + ") - " + df['Squad']
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("HATA: 'Eyeball_Streamlit_Final.csv' dosyası bulunamadı.")
    st.stop()

# --- RENK HARİTASI (YÜKSEK KONTRAST) ---
role_color_map = {
    "Inverted Winger / Dribbler": "#FF0000",       
    "Elite Speedster / Direct Winger": "#FF00FF",  
    "Poacher / Penalty Box Striker": "#FFA500",    
    "Versatile Forward / Second Striker": "#FFFF00", 
    "Target Man / Aerial Threat": "#FF69B4",       
    "Pressing Forward": "#00FF00",                 
    "Technical Hub / Deep Playmaker": "#00FFFF",   
    "Progressive Passer / Controller": "#1E90FF",  
    "Physical Ball Carrier": "#9932CC",            
    "Defensive Midfielder / Anchor": "#8B4513",    
    "Wide Midfielder / Defensive Winger": "#7FFF00", 
    "Utility Player / Workhorse": "#A9A9A9",       
    "Deep Distributor / Ball Playing CB": "#008080", 
    "Stopper / No-Nonsense Defender": "#800000",   
    "Central Defender (Standard)": "#000080",      
    "Commanding Center Back": "#FFFFFF"            
}

# 3. YAN PANEL (SIDEBAR) - GLOBAL FİLTRELER
# ---------------------------------------------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/53/53283.png", width=50) # Temsili Logo
st.sidebar.title("🔍 Scout Kontrol")

# A. SEZON FİLTRESİ (EN ÖNEMLİSİ)
all_seasons = sorted(df['Season'].unique(), reverse=True)
selected_seasons = st.sidebar.multiselect("📅 Sezon Seç", all_seasons, default=all_seasons[:1])

# B. DİĞER FİLTRELER (Sezona göre daralacak)
# Önce sezon filtresini uygulayalım ki listeler temizlensin
if selected_seasons:
    df_filtered_season = df[df['Season'].isin(selected_seasons)]
else:
    df_filtered_season = df.copy()

# Takım
teams = sorted(df_filtered_season['Squad'].unique())
selected_teams = st.sidebar.multiselect("Takım", teams)

# Pozisyon
positions = sorted(df_filtered_season['General_Position'].unique())
selected_pos = st.sidebar.multiselect("Bölge", positions)

# Rol
if selected_pos:
    roles = sorted(df_filtered_season[df_filtered_season['General_Position'].isin(selected_pos)]['Role_Name'].unique())
else:
    roles = sorted(df_filtered_season['Role_Name'].unique())
selected_roles = st.sidebar.multiselect("Yapay Zeka Rolü", roles)

# FİLTRELEME MOTORU
final_df = df_filtered_season.copy()
if selected_teams:
    final_df = final_df[final_df['Squad'].isin(selected_teams)]
if selected_pos:
    final_df = final_df[final_df['General_Position'].isin(selected_pos)]
if selected_roles:
    final_df = final_df[final_df['Role_Name'].isin(selected_roles)]


# 4. ANA EKRAN - SEKMELER (TABS)
# ---------------------------------------------------------
tab1, tab2 = st.tabs(["🌍 3D Keşif", "⚖️ Oyuncu Karşılaştırma"])

# --- TAB 1: 3D KEŞİF MODU ---
with tab1:
    col_search, col_space = st.columns([1, 3])
    with col_search:
        st.markdown("### 👤 Hızlı Git")
        # Arama kutusu artık Display_Name kullanıyor (Sezon bilgisi dahil)
        search_list = ["Seçiniz..."] + sorted(final_df['Display_Name'].unique().tolist())
        selected_player_search = st.selectbox("Oyuncuya Zoom Yap:", search_list)

    if not final_df.empty:
        fig = px.scatter_3d(
            final_df,
            x='x', y='y', z='z',
            color='Role_Name',
            color_discrete_map=role_color_map,
            hover_name='Display_Name', # Hover'da sezonu da görelim
            hover_data=['Age', 'Goals', 'Assists', 'Minutes'],
            opacity=0.8,
            size_max=12,
            template='plotly_dark',
            title=f"Analiz Edilen Oyuncu Havuzu: {len(final_df)}"
        )
        
        fig.update_layout(
            scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False), bgcolor='rgba(0,0,0,0)'),
            margin=dict(l=0, r=0, b=0, t=40),
            height=650,
            legend=dict(x=0, y=1, font=dict(size=10))
        )

        # Seçili Oyuncuyu Vurgula
        if selected_player_search != "Seçiniz...":
            p_data = df[df['Display_Name'] == selected_player_search]
            if not p_data.empty:
                fig.add_trace(go.Scatter3d(
                    x=p_data['x'], y=p_data['y'], z=p_data['z'],
                    mode='markers',
                    marker=dict(size=25, color='white', symbol='diamond', line=dict(width=2, color='black')),
                    name='SEÇİLEN',
                    hoverinfo='text',
                    hovertext=selected_player_search
                ))

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Seçilen kriterlere uygun oyuncu bulunamadı. Lütfen filtreleri gevşetin.")

# --- TAB 2: KARŞILAŞTIRMA MODU (YENİ ÖZELLİK) ---
with tab2:
    st.markdown("## ⚔️ Head-to-Head Analiz")
    st.markdown("İki oyuncuyu (veya aynı oyuncunun iki farklı sezonunu) yan yana kıyaslayın.")
    
    # Karşılaştırma için tüm havuzdan seçim yapabilmeliyiz (Filtrelerden bağımsız olabilir)
    # Ama sezon filtresi burada da önemli olabilir. Biz tüm veriyi açalım.
    all_players_list = sorted(df['Display_Name'].unique().tolist())
    
    c1, c2 = st.columns(2)
    with c1:
        p1_name = st.selectbox("1. Oyuncu Seç", all_players_list, index=0)
    with c2:
        # İkinci oyuncu için listenin ortasından birini seçelim ki farklı olsun
        p2_name = st.selectbox("2. Oyuncu Seç", all_players_list, index=min(10, len(all_players_list)-1))

    if p1_name and p2_name:
        p1_data = df[df['Display_Name'] == p1_name].iloc[0]
        p2_data = df[df['Display_Name'] == p2_name].iloc[0]

        # 1. TEMEL KARTLAR
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"🔵 {p1_data['Player']}")
            st.caption(f"{p1_data['Squad']} | {p1_data['Season']} | {p1_data['Age']} Yaş")
            st.write(f"**Rol:** {p1_data['Role_Name']}")
        with col2:
            st.success(f"🟢 {p2_data['Player']}")
            st.caption(f"{p2_data['Squad']} | {p2_data['Season']} | {p2_data['Age']} Yaş")
            st.write(f"**Rol:** {p2_data['Role_Name']}")

        st.markdown("---")

        # 2. RADAR GRAFİĞİ (GÖRSEL KIYASLAMA)
        # Karşılaştırma için önemli metrikleri seçelim
        radar_metrics = ['Goals', 'Assists', 'Shots', 'SoT', 'Dribbles_Succ', 'Prg_Pass_Dist', 'Tackles', 'Interceptions', 'Blocks']
        
        # Değerleri normalize etmek gerekir ama şimdilik ham değerlerle basit radar yapalım
        # Görsellik için max değerleri bulup oranlayabiliriz ama basit tutalım.
        
        categories = radar_metrics
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=[p1_data.get(m, 0) for m in radar_metrics],
            theta=categories,
            fill='toself',
            name=p1_data['Player'],
            line_color='blue'
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=[p2_data.get(m, 0) for m in radar_metrics],
            theta=categories,
            fill='toself',
            name=p2_data['Player'],
            line_color='green'
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True)),
            showlegend=True,
            title="Performans Radarı (Toplam İstatistikler)",
            height=400
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        # 3. DETAYLI İSTATİSTİK TABLOSU (İSTEDİĞİN GİBİ AŞAĞIYA DOĞRU)
        st.subheader("📋 Detaylı İstatistik Karşılaştırması")
        
        # Karşılaştırılacak tüm sayısal sütunları belirle
        compare_cols = [
            'Minutes', 'Goals', 'Assists', 'npxG_p90', 'xA_p90', 
            'Shots', 'SoT', 'Pass_Cmp_Pct', 'Prg_Pass_Dist', 'Prg_Carry_Dist',
            'Dribbles_Succ', 'Touches', 'Tackles', 'Interceptions', 'Blocks',
            'GCA', 'SCA', 'Role_Probability'
        ]
        
        # Veriyi hazırla
        comp_data = {
            'İstatistik': compare_cols,
            f"{p1_data['Player']} ({p1_data['Season']})": [p1_data.get(c, 0) for c in compare_cols],
            f"{p2_data['Player']} ({p2_data['Season']})": [p2_data.get(c, 0) for c in compare_cols]
        }
        
        comp_df = pd.DataFrame(comp_data)
        
        # Tabloyu Göster (Renkli ve Geniş)
        st.dataframe(
            comp_df, 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "İstatistik": st.column_config.TextColumn("Metrik", width="medium"),
            }
        )

# ALTLIK
st.markdown("---")
st.caption("Eyeball AI Scout v2.0 | Powered by Spherical UMAP & GMM")

