import streamlit as st
import google.generativeai as genai
from datetime import datetime

# 1. Sayfa Ayarları
st.set_page_config(page_title="T.C. Akıllı Sağlık Sistemi", page_icon="🏥", layout="wide")

# Görsel Stil Ayarları
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; background-color: #d32f2f; color: white; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. API Bağlantısı
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    st.error("API Anahtarı bulunamadı!")

# 3. Yan Panel (Sidebar)
with st.sidebar:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    try:
        # Sağlık Bakanlığı Logo Denemesi
        st.image("https://www.saglik.gov.tr/Assets/images/logo.png", width=150)
    except:
        st.markdown("<h1>🏥</h1>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.write("---")
    st.info(f"Sistem Tarihi: {datetime.now().strftime('%d/%m/%Y')}")
    st.write("---")
    # Sidebar'a sabit link butonu
    st.link_button("🔗 MHRS Giriş Ekranı", "https://mhrs.gov.tr/vatandas/#/")

# 4. Ana Ekran
st.title("🩺 Akıllı Sağlık ve Yönlendirme Paneli")
st.caption("Yapay Zeka Destekli Triyaj ve Randevu Yönlendirme")

sikayet = st.text_area("Lütfen şikayetinizi detaylıca yazın:", 
                      placeholder="Örn: 3 gündür süren baş ağrısı ve halsizlik...",
                      height=150)

if st.button("🚀 Kapsamlı Analiz Yap"):
    if sikayet:
        try:
            with st.spinner('Yapay zeka analiz ediyor...'):
                prompt = f"Sen profesyonel bir triyaj asistanısın. Kullanıcının şu şikayetini analiz et: '{sikayet}'. Hangi tıbbi bölüme gitmesi gerektiğini ve durumun ciddiyetini açıkla."
                response = model.generate_content(prompt)
                
                st.subheader("📋 Analiz Raporu")
                st.success(response.text)
                
                # İŞTE O EKLEME: Analizden hemen sonra randevu butonu
                st.write("---")
                st.markdown("### 📅 Bir Sonraki Adım")
                st.info("Analiz sonucuna göre randevu almak için aşağıdaki MHRS butonunu kullanabilirsiniz.")
                st.link_button("👉 MHRS'den Randevu Al", "https://mhrs.gov.tr/vatandas/#/", type="primary")
                
        except Exception as e:
            st.error(f"Analiz sırasında bir sorun oluştu: {e}")
    else:
        st.warning("Lütfen önce bir şikayet yazın.")

# Footer
st.write("---")
st.markdown("<p style='text-align: center; font-size: 0.8rem; color: gray;'>Bu proje Karaman KMÜ Otomotiv öğrencisi tarafından bir örnek çalışma olarak geliştirilmiştir.</p>", unsafe_allow_html=True)
