import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="Sağlık Asistanı", page_icon="🩺")

# 1. API Bağlantısı
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # EN ÖNEMLİ SATIR: Model ismini tam olarak böyle yazıyoruz
        model = genai.GenerativeModel(model_name='gemini-1.5-flash')
    else:
        st.error("Secrets kutusunda GOOGLE_API_KEY bulunamadı!")
except Exception as e:
    st.error(f"Bağlantı hatası: {e}")

st.title("🩺 Akıllı Sağlık Yönlendirme")
st.write("Şikayetinizi yazıp 'Analiz Et' butonuna basın.")

sikayet = st.text_area("Şikayetiniz:", placeholder="Örn: Başım dönüyor...")

if st.button("Analiz Et"):
    if sikayet:
        try:
            with st.spinner('Analiz ediliyor...'):
                # Cevap üretme kısmı
                response = model.generate_content(f"Bir sağlık asistanı olarak şu şikayeti değerlendir ve poliklinik öner: {sikayet}")
                st.success(response.text)
        except Exception as e:
            # Hata verirse tam olarak ne hatası verdiğini ekrana yazdırıyoruz
            st.error(f"Üretim hatası: {e}")
    else:
        st.warning("Lütfen bir şikayet yazın.")
