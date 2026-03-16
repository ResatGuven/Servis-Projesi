import streamlit as st
import pandas as pd

# 1. Sayfa Ayarları
st.set_page_config(
    page_title="Warmhaus | Servis Portalı",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Üst Seviye Premium Tasarım (CSS)
st.markdown("""
<style>
    /* Arka Plan: Modern Koyu/Gradyan Geçişi */
    .stApp {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: #f8fafc;
    }

    /* Ana Başlık Alanı */
    .header-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 30px;
        border-radius: 0 0 30px 30px;
        text-align: center;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 30px;
    }

    .main-title {
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 40px;
        font-weight: 900;
        letter-spacing: -1px;
    }

    /* Kart Tasarımı (Glassmorphism) */
    .glass-card {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        border-radius: 24px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
        margin-bottom: 25px;
        transition: transform 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(56, 189, 248, 0.5);
    }

    /* Şoför İsmi ve Detaylar */
    .driver-name {
        font-size: 28px;
        font-weight: 700;
        color: #38bdf8;
        margin-bottom: 15px;
    }

    .info-item {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
        font-size: 16px;
        color: #cbd5e1;
    }

    .info-item i {
        margin-right: 12px;
        color: #818cf8;
        width: 20px;
    }

    /* Selectbox ve Tablo Özelleştirme */
    .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
    }
    
    /* Tablo Tasarımı */
    div[data-testid="stDataFrame"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border-radius: 20px !important;
        padding: 10px;
    }

    /* Telefon Butonu */
    .phone-btn {
        display: block;
        background: linear-gradient(90deg, #0284c7, #0369a1);
        color: white !important;
        text-align: center;
        padding: 12px;
        border-radius: 12px;
        text-decoration: none;
        font-weight: 600;
        margin-top: 15px;
    }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
""", unsafe_allow_html=True)

# 3. Google Sheets Verileri
SHEET_ID = "1kWV5OgXsHprJro7O3zgb-wc8bzAnzUhdVReo2sheADI"
LISTE_GID = "1161773988"
PERSONEL_GID = "1207904188"

url_liste = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid={LISTE_GID}"
url_personel = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid={PERSONEL_GID}"

@st.cache_data(ttl=60)
def get_data(url):
    return pd.read_csv(url).dropna(how='all', axis=1)

# 4. Üst Başlık Alanı
st.markdown("""
    <div class="header-container">
        <div class="main-title">WARMHAUS</div>
        <div style="color: #94a3b8; font-weight: 500;">Dijital Servis Takip Portalı</div>
    </div>
""", unsafe_allow_html=True)

try:
    df_liste = get_data(url_liste)
    df_personel = get_data(url_personel)
    hatlar = sorted(df_liste['Servis Hat Seçiniz'].unique())

    # Seçim Alanı
    col_s, _ = st.columns([1, 1])
    with col_s:
        secilen_hat = st.selectbox("🚩 Hattınızı Seçin", ["Lütfen bir hat seçiniz..."] + list(hatlar))

    if secilen_hat != "Lütfen bir hat seçiniz...":
        st.markdown("---")
        
        filtreli_liste = df_liste[df_liste['Servis Hat Seçiniz'] == secilen_hat]
        filtreli_sofor = df_personel[df_personel['Servis Hattı'] == secilen_hat]

        col1, col2 = st.columns([1, 1.5])

        with col1:
            if not filtreli_sofor.empty:
                sofor = filtreli_sofor.iloc[0]
                # Modern Şoför Kartı
                st.markdown(f"""
                    <div class="glass-card">
                        <div style="color: #38bdf8; font-size: 14px; font-weight: 700; margin-bottom: 5px;">SERVİS SORUMLUSU</div>
                        <div class="driver-name">{sofor['Şoför']}</div>
                        <div class="info-item"><i class="fas fa-bus"></i> <b>Güzergah:</b> {secilen_hat}</div>
                        <div class="info-item"><i class="fas fa-barcode"></i> <b>Araç Plaka:</b> {sofor['Plaka']}</div>
                        <a href="tel:{sofor['Telefon']}" class="phone-btn"><i class="fas fa-phone"></i> Hemen Ara</a>
                    </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown(f'<div style="color: #f8fafc; font-size: 20px; font-weight: 600; margin-bottom: 15px;">👥 {secilen_hat} Yolcu Listesi</div>', unsafe_allow_html=True)
            # Tablo Stilini de içeren DataFrame
            st.dataframe(
                filtreli_liste[['AD-SOYAD', 'SERVİS DURAĞI']], 
                use_container_width=True, 
                hide_index=True,
                height=450
            )

    else:
        st.markdown("""
            <div style="text-align: center; margin-top: 50px; color: #64748b;">
                <i class="fas fa-chevron-up" style="font-size: 30px; margin-bottom: 10px;"></i>
                <p>Başlamak için yukarıdan bir servis hattı seçin.</p>
            </div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Veri bağlantısı kurulamadı. Hata: {e}")

# Footer
st.markdown(f"""
    <div style="text-align: center; padding: 40px; color: #475569; font-size: 12px;">
        WARMHAUS ISL. VE TES. CİH. SAN. TİC. A.Ş. <br> 
        © 2026 Dijital Dönüşüm Departmanı
    </div>
""", unsafe_allow_html=True)
