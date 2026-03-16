import streamlit as st
import pandas as pd

# Sayfa Ayarları (Mobil Odaklı)
st.set_page_config(page_title="Warmhaus Servis Portalı", page_icon="🚐", layout="wide")

# Tasarım CSS (Sadelik ve Şıklık)
st.markdown("""
<style>
    .stApp { background-color: #f1f5f9; }
    .main-title { color: #1e3a8a; text-align: center; font-weight: 800; font-size: 30px; padding: 15px; }
    .info-card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-top: 5px solid #0284c7; }
    .driver-name { font-size: 20px; font-weight: 700; color: #1e293b; }
    .action-button { 
        display: inline-block; padding: 12px 24px; background-color: #0284c7; color: white !important; 
        text-decoration: none; border-radius: 10px; font-weight: 600; text-align: center; width: 100%; margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Veri Kaynakları
SHEET_ID = "1kWV5OgXsHprJro7O3zgb-wc8bzAnzUhdVReo2sheADI"
LISTE_GID = "1161773988"
PERSONEL_GID = "1207904188"

url_liste = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid={LISTE_GID}"
url_personel = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid={PERSONEL_GID}"

@st.cache_data(ttl=30) # 30 saniyede bir veriyi tazeler
def get_data(url):
    return pd.read_csv(url).dropna(how='all', axis=1)

st.markdown('<div class="main-title">🚐 Warmhaus Servis Takip</div>', unsafe_allow_html=True)

try:
    df_liste = get_data(url_liste)
    df_personel = get_data(url_personel)
    hatlar = sorted(df_liste['Servis Hat Seçiniz'].unique())

    # Hat Seçimi
    secilen_hat = st.selectbox("🚩 Lütfen servis hattınızı seçin:", ["Hat Seçiniz..."] + list(hatlar))

    if secilen_hat != "Hat Seçiniz...":
        st.markdown("---")
        
        filtreli_liste = df_liste[df_liste['Servis Hat Seçiniz'] == secilen_hat]
        filtreli_sofor = df_personel[df_personel['Servis Hattı'] == secilen_hat]

        col1, col2 = st.columns([1, 1.2])

        with col1:
            if not filtreli_sofor.empty:
                sofor = filtreli_sofor.iloc[0]
                # Şoför ve Konum Kartı
                st.markdown(f"""
                <div class="info-card">
                    <div class="driver-name">👤 {sofor['Şoför']}</div>
                    <p style="color: #475569; margin-bottom: 15px;">
                        <b>🚗 Plaka:</b> {sofor['Plaka']}<br>
                        <b>📞 Tel:</b> <a href="tel:{sofor['Telefon']}">{sofor['Telefon']}</a>
                    </p>
                    <hr style="border: 0.5px solid #e2e8f0;">
                    <p style="font-weight: 600; color: #0284c7; margin-bottom: 5px;">📍 Canlı Takip Sistemi</p>
                    <p style="font-size: 14px; color: #64748b;">Servisin nerede olduğunu canlı haritada görmek için aşağıdaki butona basın.</p>
                    <a href="Https://maps.app.goo.gl/ShdXPrweM7dTrXx29" target="_blank" class="action-button">🗺️ Haritada Canlı İzle</a>
                </div>
                """, unsafe_allow_html=True)
                
        with col2:
            st.markdown(f"#### 👥 {secilen_hat} Yolcu Listesi")
            st.dataframe(
                filtreli_liste[['AD-SOYAD', 'SERVİS DURAĞI']], 
                use_container_width=True, 
                hide_index=True,
                height=400
            )
    else:
        st.info("Bilgileri görmek için yukarıdan bir güzergah seçin.")

except Exception as e:
    st.error("Veriler yüklenirken bir hata oluştu. Google Sheets ayarlarını kontrol edin.")

st.markdown("---")
st.caption("Warmhaus Dijital - Veriler otomatik olarak güncellenmektedir.")
