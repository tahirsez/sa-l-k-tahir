import streamlit as st
import google.generativeai as genai
from datetime import datetime

# 1. Sayfa Ayarları
st.set_page_config(page_title="Sağlık Analiz Portalı", page_icon="🩺", layout="wide")

# PROFESYONEL CSS - Görünürlük ve Kontrast Ayarı
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .header-container {
        background-color: #e30613;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .content-card {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #dee2e6;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    /* Yazı renklerini siyah/koyu gri yapıyoruz */
    p, span, label, h1, h2, h3, .stMarkdown { color: #212529 !important; }
    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #212529 !important;
        border: 1px solid #ced4da !important;
    }
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 5px solid #e30613 !important;
    }
    .stButton>button {
        background-color: #e30613 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        height: 3.5rem !important;
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
    st.link_button("🏥 MHRS Randevu Sistemi", "https://mhrs.gov.tr/vatandas/#/")
    st.link_button("📑 E-Nabız Portalı", "https://enabiz.gov.tr/")
    st.write("---")
    st.caption(f"🗓️ Tarih: {datetime.now().strftime('%d.%m.%Y')}")
    st.caption("📍 KMÜ / Karaman")

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
    st.write("Lütfen yaşadığınız belirtileri detaylıca aşağıya yazınız.")
    
    sikayet = st.text_area("", placeholder="Örn: 2 gündür süren şiddetli baş ağrısı ve ışığa duyarlılık...", height=150, key="txt_area", label_visibility="collapsed")
    
    st.write("") 
    if st.button("SİSTEM ANALİZİNİ BAŞLAT"):
        if sikayet:
            try:
                with st.spinner('Yapay zeka detaylı analiz yapıyor...'):
                    # Turbo Modu: Detaylı Prompt
                    prompt = f"""
                    Sen profesyonel bir hastane triyaj uzmanısın. 
                    Şikayet: '{sikayet}'
                    Lütfen şu başlıklarla DETAYLI bir analiz sun:
                    1. 🔍 **Şikayet Analizi:** Belirtiler neyi gösteriyor?
                    2. 🏥 **Poliklinik Önerisi:** Hangi bölüme gidilmeli?
                    3. ⚡ **Aciliyet Durumu:** Durumun ciddiyeti nedir?
                    4. 💡 **Tavsiyeler:** Doktora gidene kadar ne yapılmalı?
                    5. ⚠️ **Kritik Uyarı:** Ne zaman hemen 112 aranmalı?
                    """
                    response = model.generate_content(prompt)
                
                # SONUÇLARI EKRANA BAS (with bloğundan çıktık, try içindeyiz)
                st.markdown("---")
                st.markdown("#### 🩺 Yapay Zeka Ön Değerlendirmesi")
                st.success(response.text)
                st.link_button("👉 MHRS'den Randevu Al", "https://mhrs.gov.tr/vatandas/#/")
                
            except Exception as e:
                # Hata sigortası burada (SyntaxError'u bu çözer)
                st.error(f"Sistemde bir hata oluştu: {e}")
        else:
            st.warning("Lütfen analiz için bir şikayet metni giriniz.")
