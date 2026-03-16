import streamlit as st
import pandas as pd

# 1. Sayfa Ayarları (Mobil Uygulama Hissi)
st.set_page_config(page_title="Warmhaus Portal", page_icon="🚐", layout="centered")

# 2. Modern ve Canlı UI Tasarımı
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    .stApp { background-color: #f8fafc; font-family: 'Inter', sans-serif; }
    
    .app-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 35px 20px;
        border-radius: 0 0 30px 30px;
        text-align: center;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 10px 15px -3px rgba(30, 58, 138, 0.2);
    }
    .app-title { font-size: 26px; font-weight: 800; margin: 0; }
    
    /* Kartlar */
    .mobile-card {
        background: white;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border: 1px solid #f1f5f9;
    }
    
    .call-btn {
        background: #10b981;
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
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
""", unsafe_allow_html=True)

# 3. Veri Kaynakları (Yeni Linkinle Güncellendi)
SHEET_ID = "1kWV5OgXsHprJro7O3zgb-wc8bzAnzUhdVReo2sheADI"
LISTE_GID = "1161773988"
PERSONEL_GID = "1207904188"

@st.cache_data(ttl=5) # Admin düzenlemesi için süreyi kısalttık
def get_data(gid):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
    return pd.read_csv(url).dropna(how='all', axis=1)

# Header
st.markdown('<div class="app-header"><div class="app-title">WARMHAUS</div><div style="opacity:0.8; font-size:12px;">Servis Yönetim Portalı</div></div>', unsafe_allow_html=True)

# 4. Yan Menü ve Admin Girişi
with st.sidebar:
    st.subheader("🔐 Yönetici Paneli")
    input_sifre = st.text_input("Şifre", type="password")
    is_admin = input_sifre == "Admin123"

    if is_admin:
        st.success("Admin Yetkisi Aktif ✅")
        islem = st.radio("Menü:", ["Servis Görüntüle", "Listeyi Düzenle (Anlık)"])
    else:
        islem = "Servis Görüntüle"

# 5. Ana Ekran
try:
    df_liste = get_data(LISTE_GID)
    df_personel = get_data(PERSONEL_GID)

    if is_admin and islem == "Listeyi Düzenle (Anlık)":
        st.subheader("📝 Uygulama İçinden Düzenleme")
        st.warning("Hücrelere tıklayarak veriyi değiştirebilirsiniz. (Not: Kalıcı kayıt için API yetkisi gerekir)")
        
        # Google Sheets'e gitmeden düzenleme aracı
        edited_df = st.data_editor(df_liste, use_container_width=True, num_rows="dynamic")
        
        if st.button("Değişiklikleri Onayla"):
            st.success("Değişiklikler işlendi! (Kalıcı kayıt için Service Account kurulmalıdır)")

    else:
        # KULLANICI EKRANI
        hatlar = sorted(df_liste['Servis Hat Seçiniz'].unique())
        secilen_hat = st.selectbox("🚩 Hattınızı Seçin:", ["Seçiniz..."] + list(hatlar))

        if secilen_hat != "Seçiniz...":
            sofor_info = df_personel[df_personel['Servis Hattı'] == secilen_hat]
            yolcular = df_liste[df_liste['Servis Hat Seçiniz'] == secilen_hat]

            if not sofor_info.empty:
                s = sofor_info.iloc[0]
                st.markdown(f"""
                    <div class="mobile-card">
                        <div style="color: #3b82f6; font-size: 11px; font-weight: 800; text-transform: uppercase;">Şoför Bilgisi</div>
                        <div style="font-size: 22px; font-weight: 700; color: #1e293b;">{s['Şoför']}</div>
                        <div style="color: #64748b; font-size: 14px; margin-top: 5px;">
                            <i class="fas fa-shuttle-van"></i> Plaka: <b>{s['Plaka']}</b>
                        </div>
                        <a href="tel:{s['Telefon']}" class="call-btn">
                            <i class="fas fa-phone-alt"></i> Şoförü Ara
                        </a>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown(f"#### 👥 {secilen_hat} Yolcu Listesi")
            st.dataframe(yolcular[['AD-SOYAD', 'SERVİS DURAĞI']], use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"Bağlantı Hatası: {e}")

st.markdown("<br><center style='color:#94a3b8; font-size:10px;'>Warmhaus IT Solution</center>", unsafe_allow_html=True)
