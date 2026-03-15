import streamlit as st
import google.generativeai as genai
from datetime import datetime

# 1. Sayfa Ayarları
st.set_page_config(page_title="Akıllı Sağlık Paneli", page_icon="🩺", layout="wide")

# PROFESYONEL CSS (Kontrast ve Boşluk Ayarı)
st.markdown("""
    <style>
    /* Arka planı hafif gri yap ki beyaz kartlar belli olsun */
    .stApp {
        background-color: #f0f2f5;
    }
    
    /* Üst Panel */
    .header-container {
        background-color: #e30613;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    /* Kart Yapısı (Yazıların kaybolmasını engeller) */
    .content-card {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        color: #2d2d2d !important;
        margin-bottom: 20px;
    }

    /* Tüm metinlerin rengini koyu yapalım ki beyazda kaybolmasın */
    p, span, label, .stMarkdown {
        color: #2d2d2d !important;
    }

    /* Giriş Kutusu (Textarea) Düzenlemesi */
    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #2d2d2d !important;
        border: 1px solid #ced4da !important;
        font-size: 16px !important;
    }

    /* Yan Panel (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 4px solid #e30613 !important;
    }

    /* Buton */
    .stButton>button {
        background-color: #e30613 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        height: 3.5rem !important;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #2d2d2d !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. API ve Model (Gemini 2.5 Flash)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    st.error("API Anahtarı bulunamadı!")

# 3. YAN PANEL
with st.sidebar:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    try:
        st.image("logo.png", width=160)
    except:
        st.markdown("<h1 style='color:#e30613; font-size: 70px;'>🩺</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #2d2d2d;'>SAĞLIK ANALİZ<br>SİSTEMİ</h3>", unsafe_allow
