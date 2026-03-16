import streamlit as st
import pandas as pd

# 1. Sayfa Ayarları (Tam Mobil Odaklı)
st.set_page_config(page_title="Warmhaus Portal", page_icon="🚐", layout="centered")

# 2. Üst Düzey Mobil App Tasarımı (CSS) - Daha Ferah ve Modern
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    .stApp { background-color: #f8fafc; font-family: 'Inter', sans-serif; }
    
    /* Mobil Header */
    .app-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 35px 20px;
        border-radius: 0 0 25px 25px;
        text-align: center;
        color: white;
        margin-bottom: 20px;
    }
    
    .app-title { font-size: 26px; font-weight: 800; letter-spacing: -1px; margin: 0; }
    
    /* Modern Kart Yapısı */
    .mobile-card {
        background: white;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        margin-bottom: 15px;
        border: 1px solid #f1f5f9;
    }
    
    .driver-name { font-size: 20px; font-weight: 700; color: #0f172a; }
    
    /* Şık Telefon Butonu */
    .call-btn {
        background: #22c55e;
        color: white !important;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 12px;
        border-radius: 12px;
        text-decoration: none;
        font-weight: 700;
        margin-top: 15px;
        gap: 8px;
    }

    /* Admin Badge */
    .admin-badge {
        background: #fee2e2;
        color: #ef4444;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 10px;
    }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
""", unsafe_allow_html=True)

# 3. Veri Kaynakları
SHEET_ID = "1kWV5OgXsHprJro7O3zgb-wc8bzAnzUhdVReo2sheADI"
LISTE_GID = "1161773988"
PERSONEL_GID = "1207904188"

@st.cache_data(ttl=10)
def get_data(gid):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
    return pd.read_csv(url).dropna(how='all', axis=1)

# Header
st.markdown('<div class="app-header"><div class="app-title">WARMHAUS</div><div style="opacity:0.8; font-size:12px;">Personel Servis Yönetimi</div></div>', unsafe_allow_html=True)

# 4. Admin Girişi (Sidebar/Yan Menü)
with st.sidebar:
    st.subheader("🔐 Yönetici Girişi")
    admin_sifre = st.text_input("Şifre", type="password")
    # Şifreyi buradan istediğin gibi değiştirebilirsin
    is_admin = admin_sifre == "Admin16" 

    if is_admin:
        st.markdown('<div class="admin-badge">Yönetici Modu Aktif</div>', unsafe_allow_html=True)
        mod = st.radio("İşlem Seçin:", ["Servis İzle", "Veri Yönetimi (Ekle/Sil)"])
    else:
        mod = "Servis İzle"

# 5. Ana Ekran Mantığı
try:
    df_liste = get_data(LISTE_GID)
    df_personel = get_data(PERSONEL_GID)

    if is_admin and mod == "Veri Yönetimi (Ekle/Sil)":
        st.subheader("🛠 Veri Yönetim Paneli")
        st.info("Aşağıdaki butona basarak Personel veya Şoför listesini anlık olarak düzenleyebilirsin. Değişiklikler bittiğinde bu sayfayı yenilemen yeterli olacaktır.")
        
        # Google Sheets Düzenleme Linki
        edit_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit"
        st.link_button("📊 Tabloyu Düzenle (Google Sheets)", edit_url)
        
        st.divider()
        st.write("Current Personel Listesi (Önizleme):")
        st.dataframe(df_liste, use_container_width=True)

    else:
        # PERSONEL EKRANI
        hatlar = sorted(df_liste['Servis Hat Seçiniz'].unique())
        secilen_hat = st.selectbox("📍 Hattınızı Seçin:", ["Seçiniz..."] + list(hatlar))

        if secilen_hat != "Seçiniz...":
            sofor_verisi = df_personel[df_personel['Servis Hattı'] == secilen_hat]
            yolcu_listesi = df_liste[df_liste['Servis Hat Seçiniz'] == secilen_hat]

            if not sofor_verisi.empty:
                s = sofor_verisi.iloc[0]
                st.markdown(f"""
                    <div class="mobile-card">
                        <div style="color: #3b82f6; font-size: 11px; font-weight: 700; text-transform: uppercase;">Servis Şoförü</div>
                        <div class="driver-name">{s['Şoför']}</div>
                        <div style="color: #64748b; font-size: 14px; margin-top: 5px;">
                            <i class="fas fa-shuttle-van"></i> Plaka: <b>{s['Plaka']}</b>
                        </div>
                        <a href="tel:{s['Telefon']}" class="call-btn">
                            <i class="fas fa-phone-alt"></i> Şoförü Ara
                        </a>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown(f"#### 👥 {secilen_hat} Listesi")
            st.dataframe(yolcu_listesi[['AD-SOYAD', 'SERVİS DURAĞI']], use_container_width=True, hide_index=True)

except Exception as e:
    st.error("Bir hata oluştu. Lütfen Google Sheets paylaşım ayarlarını kontrol et.")

st.markdown("<br><center style='color:#cbd5e1; font-size:10px;'>Warmhaus IT Solution © 2026</center>", unsafe_allow_html=True)
