
import streamlit as st
import pandas as pd

st.set_page_config(page_title="🧹 Data Cleaner PRO", layout="wide")

# 🌍 Selettore lingua
lingua = st.selectbox(
    "🌐 Seleziona la lingua / Select language / Selecciona el idioma",
    ["Español", "Italiano", "English"]
)

# Dizionario testi
testi = {
    "Español": {
        "title": "🧹 Data Cleaner PRO",
        "subtitle": "Limpia y prepara tus datos con facilidad",
        "upload": "📂 Sube un archivo CSV",
        "preview": "👁️ Vista previa de los datos",
        "row_analysis": "🔍 Análisis fila por fila – ¿Qué falta en cada registro?",
        "cleaning": "🧼 Opciones de limpieza",
        "drop_empty_cols": "Eliminar columnas completamente vacías",
        "drop_dupe_cols": "Eliminar columnas duplicadas",
        "drop_null_rows": "Eliminar filas con valores nulos",
        "cleaned_data": "🧾 Datos después de la limpieza",
        "download": "💾 Descargar CSV limpio",
        "upload_prompt": "Por favor, sube un archivo CSV para comenzar.",
        "success_upload": "✅ Archivo cargado correctamente",
        "all_complete": "✅ Todas las filas están completas.",
        "unnamed": "Columna sin nombre",
        "row": "Fila",
        "missing": "falta"
    },
    "Italiano": {
        "title": "🧹 Data Cleaner PRO",
        "subtitle": "Pulisci e prepara i tuoi dati facilmente",
        "upload": "📂 Carica un file CSV",
        "preview": "👁️ Anteprima dei dati",
        "row_analysis": "🔍 Analisi riga per riga – Cosa manca in ogni record?",
        "cleaning": "🧼 Opzioni di pulizia",
        "drop_empty_cols": "Elimina colonne completamente vuote",
        "drop_dupe_cols": "Elimina colonne duplicate",
        "drop_null_rows": "Elimina righe con valori nulli",
        "cleaned_data": "🧾 Dati dopo la pulizia",
        "download": "💾 Scarica CSV pulito",
        "upload_prompt": "Carica un file CSV per iniziare.",
        "success_upload": "✅ File caricato correttamente",
        "all_complete": "✅ Tutte le righe sono complete.",
        "unnamed": "Colonna senza nome",
        "row": "Riga",
        "missing": "manca"
    },
    "English": {
        "title": "🧹 Data Cleaner PRO",
        "subtitle": "Clean and prepare your data easily",
        "upload": "📂 Upload a CSV file",
        "preview": "👁️ Data preview",
        "row_analysis": "🔍 Row-by-row analysis – What's missing?",
        "cleaning": "🧼 Cleaning options",
        "drop_empty_cols": "Remove completely empty columns",
        "drop_dupe_cols": "Remove duplicated columns",
        "drop_null_rows": "Remove rows with missing values",
        "cleaned_data": "🧾 Data after cleaning",
        "download": "💾 Download cleaned CSV",
        "upload_prompt": "Please upload a CSV file to begin.",
        "success_upload": "✅ File uploaded successfully",
        "all_complete": "✅ All rows are complete.",
        "unnamed": "Unnamed column",
        "row": "Row",
        "missing": "missing"
    }
}

t = testi[lingua]

st.title(t["title"])
st.subheader(t["subtitle"])

file = st.file_uploader(t["upload"], type=["csv"])

if file is not None:
    df = pd.read_csv(file)

    df.columns = [
        f"{t['unnamed']} {i}" if "Unnamed" in col else col
        for i, col in enumerate(df.columns)
    ]

    st.success(t["success_upload"])
    st.subheader(t["preview"])
    st.dataframe(df)

    st.subheader(t["row_analysis"])
    messages = []
    for i, row in df.iterrows():
        missing = row[row.isnull()].index.tolist()
        if missing:
            name = row.get("Nombre", f"{t['row']} {i+1}")
            row_label = name if pd.notnull(name) else f"{t['row']} {i+1}"
            msg = f"🔴 {row_label} → {t['missing']}: {', '.join(missing)}"
            messages.append(msg)

    if messages:
        for m in messages:
            st.write(m)
    else:
        st.success(t["all_complete"])

    st.subheader(t["cleaning"])

    if st.checkbox(t["drop_empty_cols"]):
        df = df.dropna(axis=1, how='all')

    if st.checkbox(t["drop_dupe_cols"]):
        df = df.loc[:, ~df.columns.duplicated()]

    if st.checkbox(t["drop_null_rows"]):
        df = df.dropna()

    st.subheader(t["cleaned_data"])
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=t["download"],
        data=csv,
        file_name='datos_limpios.csv',
        mime='text/csv'
    )

else:
    st.info(t["upload_prompt"])
