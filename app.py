import streamlit as st
import pandas as pd

# 1. Sayfa Ayarları
st.set_page_config(
    page_title="Warmhaus | Servis Portalı",
    page_icon="🚐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Ferah ve Modern Tasarım (CSS)
st.markdown("""
<style>
    /* Arka Plan: Hafif Mavi/Beyaz Gradyan */
    .stApp {
        background: linear-gradient(180deg, #f0f9ff 0%, #ffffff 100%);
        color: #1e293b;
    }

    /* Üst Header */
    .header-container {
        background: white;
        padding: 40px 20px;
        text-align: center;
        border-bottom: 1px solid #e2e8f0;
        margin-bottom: 40px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }

    .main-title {
        color: #1e3a8a;
        font-size: 42px;
        font-weight: 900;
        letter-spacing: -1.5px;
        margin-bottom: 5px;
    }

    /* Premium Beyaz Kartlar */
    .premium-card {
        background: white;
        border: 1px solid #e2e8f0;
        padding: 30px;
        border-radius: 24px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.03);
        margin-bottom: 25px;
    }
    
    /* Şoför İsmi */
    .driver-label {
        color: #0ea5e9;
        font-size: 13px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .driver-name {
        font-size: 32px;
        font-weight: 800;
        color: #0f172a;
        margin: 10px 0 20px 0;
    }

    .info-line {
        display: flex;
        align-items: center;
        margin-bottom: 12px;
        font-size: 17px;
        color: #475569;
    }

    .info-line i {
        margin-right: 15px;
        color: #0ea5e9;
        font-size: 20px;
    }

    /* Telefon Butonu - Canlı Mavi */
    .phone-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        background: #0ea5e9;
        color: white !important;
        padding: 15px;
        border-radius: 16px;
        text-decoration: none;
        font-weight: 700;
        font-size: 18px;
        margin-top: 25px;
        transition: all 0.3s ease;
    }
    
    .phone-btn:hover {
        background: #0284c7;
        transform: scale(1.02);
    }

    /* Tablo Düzenlemeleri */
    div[data-testid="stDataFrame"] {
        border: 1px solid #e2e8f0;
        border-radius: 20px !important;
        background: white !important;
    }

    /* Selectbox Sadeleştirme */
    .stSelectbox label {
        font-weight: 700;
        color: #1e3a8a;
    }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
""", unsafe_allow_html=True)

# 3. Veri Çekme
SHEET_ID = "1kWV5OgXsHprJro7O3zgb-wc8bzAnzUhdVReo2sheADI"
LISTE_GID = "1161773988"
PERSONEL_GID = "1207904188"

url_liste = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid={LISTE_GID}"
url_personel = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid={PERSONEL_GID}"

@st.cache_data(ttl=60)
def get_data(url):
    return pd.read_csv(url).dropna(how='all', axis=1)

# 4. Header
st.markdown("""
    <div class="header-container">
        <div class="main-title">WARMHAUS</div>
        <div style="color: #64748b; font-size: 18px; font-weight: 500;">Personel Servis Bilgi Sistemi</div>
    </div>
""", unsafe_allow_html=True)

try:
    df_liste = get_data(url_liste)
    df_personel = get_data(url_personel)
    hatlar = sorted(df_liste['Servis Hat Seçiniz'].unique())

    # Seçim Alanı
    col_sel, _ = st.columns([1.5, 1])
    with col_sel:
        secilen_hat = st.selectbox("🚩 GÜZERGAH SEÇİNİZ", ["Lütfen bir hat seçiniz..."] + list(hatlar))

    if secilen_hat != "Lütfen bir hat seçiniz...":
        st.write("") # Boşluk
        
        filtreli_liste = df_liste[df_liste['Servis Hat Seçiniz'] == secilen_hat]
        filtreli_sofor = df_personel[df_personel['Servis Hattı'] == secilen_hat]

        col_left, col_right = st.columns([1, 1.3])

        with col_left:
            if not filtreli_sofor.empty:
                sofor = filtreli_sofor.iloc[0]
                st.markdown(f"""
                    <div class="premium-card">
                        <div class="driver-label">Servis Sorumlusu</div>
                        <div class="driver-name">{sofor['Şoför']}</div>
                        <div class="info-line"><i class="fas fa-route"></i> <b>Hat:</b> {secilen_hat}</div>
                        <div class="info-line"><i class="fas fa-shuttle-van"></i> <b>Plaka:</b> {sofor['Plaka']}</div>
                        <a href="tel:{sofor['Telefon']}" class="phone-btn"><i class="fas fa-phone-alt" style="margin-right:10px;"></i> Şoförü Ara</a>
                    </div>
                """, unsafe_allow_html=True)

        with col_right:
            st.markdown(f'<div style="color: #1e3a8a; font-size: 22px; font-weight: 800; margin-bottom: 20px; padding-left:10px;">👥 {secilen_hat} Yolcu Listesi</div>', unsafe_allow_html=True)
            st.dataframe(
                filtreli_liste[['AD-SOYAD', 'SERVİS DURAĞI']], 
                use_container_width=True, 
                hide_index=True,
                height=500
            )

except Exception as e:
    st.error("Veri güncellenirken bir hata oluştu.")

# Footer
st.markdown("""
    <div style="text-align: center; padding: 60px 0; color: #94a3b8; font-size: 13px; font-weight: 500;">
        WARMHAUS DİJİTAL DÖNÜŞÜM <br> 
        Servis takip bilgilerini bu ekran üzerinden anlık takip edebilirsiniz.
    </div>
""", unsafe_allow_html=True)
