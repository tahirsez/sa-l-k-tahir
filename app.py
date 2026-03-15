import streamlit as st
import google.generativeai as genai
from datetime import datetime

# 1. Sayfa Ayarları
st.set_page_config(page_title="Sağlık Analiz Portalı", page_icon="🩺", layout="wide")

# PROFESYONEL CSS - Okunabilirlik ve Kontrast Ayarı
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    
    /* Üst Panel */
    .header-container {
        background-color: #e30613;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    /* Kart Yapısı */
    .content-card {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #dee2e6;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* GENEL YAZI RENKLERİ (Okunabilirlik için siyah/koyu gri) */
    p, span, label, h1, h2, h3, .stMarkdown { color: #212529 !important; }
    
    /* YAN PANEL (SIDEBAR) BUTON DÜZENLEME */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 5px solid #e30613 !important;
    }
    
    /* Sidebar'daki Link Butonlarının Renklerini Sabitleme (Okunmuyor demiştin) */
    [data-testid="stSidebar"] .stButton>button, 
    [data-testid="stSidebar"] a {
        background-color: #f1f3f5 !important; /* Hafif gri arka plan */
        color: #e30613 !important; /* MHRS Kırmızısı yazı */
        border: 1px solid #e30613 !important;
        font-weight: bold !important;
        text-decoration: none !important;
    }

    /* ANA BUTON TASARIMI */
    .stButton>button {
        background-color: #e30613 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        height: 3.5rem !important;
    }

    /* FOOTER (KMÜ Notu) */
    .footer-text {
        text-align: center;
        color: #6c757d !important;
        margin-top: 50px;
        font-size: 0.9rem;
        border-top: 1px solid #dee2e6;
        padding-top: 20px;
    }
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
        st.image("logo.png", width=150)
    except:
        st.markdown("<h1 style='color:#e30613;'>🩺</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #212529;'>DİJİTAL SAĞLIK<br>ASİSTANI</h3>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.write("---")
    st.markdown("#### 🏥 HIZLI ERİŞİM")
    # Linkler artık daha belirgin
    st.link_button("🏥 MHRS Randevu Sistemi", "https://mhrs.gov.tr/vatandas/#/")
    st.link_button("📑 E-Nabız Portalı", "https://enabiz.gov.tr/")
    
    st.write("---")
    st.caption(f"🗓️ {datetime.now().strftime('%d.%m.%Y')}")
    st.caption("📍 KMÜ / Karaman Yerleşkesi")

# 4. Ana Ekran
st.markdown("""
    <div class='header-container'>
        <h1 style='color: white !important; margin:0; font-size: 26px;'>AKILLI SAĞLIK ANALİZ VE YÖNLENDİRME SİSTEMİ</h1>
    </div>
    """, unsafe_allow_html=True)

col1, col_mid, col2 = st.columns([1, 10, 1])

with col_mid:
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.markdown("### 📝 Şikayet Bildirimi")
    st.write("Lütfen yaşadığınız belirtileri aşağıya detaylıca yazınız.")
    
    sikayet = st.text_area("", placeholder="Örn: 2 gündür süren şiddetli baş ağrısı ve ışığa duyarlılık...", height=150, key="txt_area", label_visibility="collapsed")
    
    st.write("") 
    if st.button("SİSTEM ANALİZİNİ BAŞLAT"):
        if sikayet:
            try:
                with st.spinner('Yapay zeka detaylı analiz yapıyor...'):
                    prompt = f"""
                    Sen profesyonel bir hastane triyaj uzmanısın. 
                    Şikayet: '{sikayet}'
                    Lütfen şu başlıklarla DETAYLI bir analiz sun:
                    1. 🔍 **Şikayet Analizi:** Belirtiler neye işaret ediyor?
                    2. 🏥 **Poliklinik Önerisi:** Hangi bölüme gidilmeli?
                    3. ⚡ **Aciliyet Durumu:** Durumun ciddiyeti nedir?
                    4. 💡 **Tavsiyeler:** Doktora gidene kadar ne yapılmalı?
                    5. ⚠️ **Kritik Uyarı:** Ne zaman hemen 112 aranmalı?
                    """
                    response = model.generate_content(prompt)
                
                st.markdown("---")
                st.markdown("#### 🩺 Yapay Zeka Ön Değerlendirmesi")
                st.info(response.text)
                st.link_button("👉 MHRS'den Randevu Al", "https://mhrs.gov.tr/vatandas/#/")
                
            except Exception as e:
                st.error(f"Sistemde bir hata oluştu: {e}")
        else:
            st.warning("Lütfen analiz için bir şikayet metni giriniz.")
    st.markdown("</div>", unsafe_allow_html=True)

# 5. FOOTER (Senin imzanı buraya kalıcı çaktık)
st.markdown("""
    <div class='footer-text'>
        Bu uygulama Karamanoğlu Mehmetbey Üniversitesi (KMÜ) Otomotiv Teknolojisi öğrencisi <b>Tahir Sezen</b> tarafından bir bitirme projesi prototipi olarak geliştirilmiştir. © 2026
    </div>
    """, unsafe_allow_html=True)
