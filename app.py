# app.py
import streamlit as st
import pandas as pd
from validacion_datos import validar_dataframe

st.set_page_config(page_title="Validador de Datos - Great Expectations")

st.title("🔍 Validador de Datos con Great Expectations")
st.write("Sube un archivo `.csv` con columnas: `nombre`, `edad`, `correo`.")

uploaded_file = st.file_uploader("Sube tu archivo CSV", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)

        if st.button("🚀 Ejecutar Validación"):
            with st.spinner("Validando datos..."):
                result, html_path = validar_dataframe(df)

            if result["success"]:
                st.success("¡Validación exitosa! ✅")
            else:
                st.warning("La validación encontró algunos problemas ❗")

            st.markdown(f"[📄 Ver reporte HTML]({html_path})", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
