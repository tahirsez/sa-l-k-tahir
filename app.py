import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Sağlık Asistanı - Tanı Modu", page_icon="🩺")

# 1. API Bağlantısı
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Secrets kutusunda GOOGLE_API_KEY bulunamadı!")

st.title("🩺 Akıllı Sağlık Asistanı")

# 2. Mevcut Modelleri Listeleme (Arıza Tespit)
try:
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    st.info(f"Senin anahtarınla kullanılabilecek modeller: {available_models}")
    
    # Listeden en güncel görüneni seçelim (genellikle listenin sonundaki veya flash olanı)
    # Eğer liste boş değilse ilkini varsayılan yapalım
    if available_models:
        # models/gemini-1.5-flash gibi bir isim gelecek, biz onu kullanacağız
        secili_model_adi = available_models[0] 
        model = genai.GenerativeModel(model_name=secili_model_adi)
        st.success(f"Şu an aktif olan model: {secili_model_adi}")
    else:
        st.error("Kullanılabilir model bulunamadı!")
except Exception as e:
    st.error(f"Model listesi alınamadı: {e}")

# 3. Şikayet Analiz Kısmı
sikayet = st.text_area("Şikayetiniz:", placeholder="Örn: Başım çok ağrıyor...")

if st.button("Analiz Et"):
    if sikayet and available_models:
        try:
            with st.spinner('Yapay zeka analiz ediyor...'):
                response = model.generate_content(f"Bir sağlık asistanı olarak şu şikayeti değerlendir ve poliklinik öner: {sikayet}")
                st.success(response.text)
        except Exception as e:
            st.error(f"Üretim hatası: {e}")
    else:
        st.warning("Lütfen şikayet yazın veya modelin yüklendiğinden emin olun.")
