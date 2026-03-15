import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="Akıllı Sağlık Asistanı", page_icon="🩺")

# API Bağlantısı (Secrets üzerinden)
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("Hata: API anahtarı sisteme tanımlanmamış!")
except Exception as e:
    st.error(f"Bağlantı hatası: {e}")

st.title("🩺 Akıllı Sağlık Yönlendirme")
st.write("Şikayetinizi yazın, sizi doğru bölüme yönlendireyim.")

sikayet = st.text_area("Şikayetiniz nedir?")
if st.button("Analiz Et"):
    if sikayet:
        response = model.generate_content(f"Bir sağlık asistanı gibi şu şikayeti analiz et ve poliklinik öner: {sikayet}")
        st.success(response.text)
    else:
        st.warning("Lütfen bir şikayet yazın.")
