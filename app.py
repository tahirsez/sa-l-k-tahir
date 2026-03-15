import streamlit as st
import google.generativeai as genai
from datetime import datetime

# 1. Sayfa Ayarları
st.set_page_config(page_title="MHRS Dijital Asistan", page_icon="🏥", layout="wide")

# MHRS "Beyaz Tema" ve Profesyonel CSS
st.markdown("""
    <style>
    /* Ana Arka Planı Bembeyaz Yap */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Sağ Tarafın İçeriğini Beyaz Tut */
    [data-testid="stVerticalBlock"] {
        background-color: #ffffff;
    }

    /* MHRS Kırmızısı ve Fontlar */
    h1, h2, h3 {
        color: #e30613 !important;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Giriş Kutusu (Text Area) Tasarımı */
    .stTextArea textarea {
        background-color: #fcfcfc !important;
        border: 2px solid #ddd !important;
        border-radius: 10px !important;
        color: #333 !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #e30613 !important;
    }

    /* Buton Tasarımı (MHRS Kırmızısı) */
    .stButton>button {
        background-color: #e30613 !important;
        color: white !important;
        border-radius: 5px !important;
        border: none !important;
        height: 3.5rem !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }

    /* Yan Panel (Sidebar) MHRS Tarzı */
    [data-testid="stSidebar"] {
        background-color: #f1f3f5 !important;
        border-right: 4px solid #e30613 !important;
    }

    /* Bilgi Kutularını (Success/Info) MHRS'ye Uyarlat */
    .stAlert {
        background-color: #ffffff !important;
        border: 1px solid #e30613 !important;
        color: #333 !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. API ve Model (Senin 2.5-flash)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    st.error("API Anahtarı bulunamadı!")

# 3. Yan Panel (Sidebar)
with st.sidebar:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    try:
        st.image("logo.png", width=170)
    except:
        st.markdown("<h1 style='color:#e30613; font-size: 60px;'>🏥</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#555;'>Dijital Sağlık Paneli</h4>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.write("---")
    st.markdown("### 📋 Menü")
    st.link_button("🏥 MHRS Randevu Sistemi", "https://mhrs.gov.tr/vatandas/#/")
    st.link_button("📑 E-Nabız Portalı", "https://enabiz.gov.tr/")
    
    st.write("---")
    st.caption(f"Sistem Tarihi: {datetime.now().strftime('%d.%m.%Y')}")
    st.caption("Konum: KMÜ Karaman")

# 4. Ana Ekran - MHRS Üst Barı Taklidi
st.markdown("""
    <div style='background-color: #e30613; padding: 10px; border-radius: 5px; margin-bottom: 25px;'>
        <h3 style='color: white !important; margin: 0; text-align: center;'>T.C. SAĞLIK BAKANLIĞI AKILLI YÖNLENDİRME SİSTEMİ</h3>
    </div>
    """, unsafe_allow_html=True)

# Şikayet Giriş Alanı
with st.container():
    st.markdown("### 🏥 Şikayet Bilgi Girişi")
    st.write("Lütfen mevcut rahatsızlığınızı aşağıdaki alana detaylıca tanımlayınız.")
    
    sikayet = st.text_area("", placeholder="Örn: Mide yanması, bulantı ve sabahları görülen halsizlik...", height=150)
    
    if st.button("SİSTEM ANALİZİNİ BAŞLAT"):
        if sikayet:
            try:
                with st.spinner('Yapay zeka tıbbi algoritmaları çalıştırıyor...'):
                    prompt = f"Sen bir triyaj asistanısın. Şu şikayeti profesyonel ve kısa bir rapor haline getir: '{sikayet}'. Hangi poliklinik ve randevu türü seçilmeli?"
                    response = model.generate_content(prompt)
                
                st.markdown("### 📋 Analiz ve Poliklinik Önerisi")
                st.success(response.text)
                
                # MHRS Butonu
                st.markdown("---")
                st.info("💡 **Bilgilendirme:** Analiz sonucuna göre randevunuzu MHRS üzerinden hemen alabilirsiniz.")
                st.link_button("👉 MHRS'DEN RANDEVU ALMAK İÇİN TIKLAYIN", "https://mhrs.gov.tr/vatandas/#/")
                
            except Exception as e:
                st.error(f"Bir sorun oluştu, lütfen tekrar deneyin: {e}")
        else:
            st.warning("Lütfen analiz için bir şikayet yazınız.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #999; font-size: 0.8rem;'>Bu portal Karaman KMÜ öğrencisi tarafından geliştirilmiş akademik bir çalışmadır. © 2026</p>", unsafe_allow_html=True)
