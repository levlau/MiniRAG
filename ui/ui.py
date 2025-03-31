import streamlit as st
import requests

# Basis URL des API-Servers anpassen
BASE_URL = "http://localhost:9721"

st.title("MiniRAG API UI")

# Erstelle Tabs für die verschiedenen Endpoints
tab_upload, tab_batch, tab_scan, tab_query, tab_graphs, tab_health, tab_documents = st.tabs([
    "Upload", "Batch", "Scan", "Query", "Graphs", "Health", "Documents"
])

# --- /documents/upload ---
with tab_upload:
    st.header("Dokumente Upload")
    uploaded_file = st.file_uploader(
        "Wählen Sie eine Datei zum Hochladen",
        type=["pdf", "txt", "docx"],
        key="upload_file"
    )
    if uploaded_file is not None:
        # Sende den Upload-Request
        response = requests.post(
            f"{BASE_URL}/documents/upload",
            files={"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        )
        st.write("Response:", response.json())

# --- /documents/batch ---
with tab_batch:
    st.header("Batch Upload")
    uploaded_files = st.file_uploader(
        "Wählen Sie mehrere Dateien für den Batch-Upload",
        type=["pdf", "txt", "docx"],
        key="batch_files",
        accept_multiple_files=True
    )
    if st.button("Batch Upload starten"):
        if uploaded_files:
            files = []
            for file in uploaded_files:
                files.append(("files", (file.name, file, file.type)))
            response = requests.post(f"{BASE_URL}/documents/batch", files=files)
            st.write("Response:", response.json())
        else:
            st.warning("Bitte wählen Sie mindestens eine Datei aus.")

# --- /documents/scan ---
with tab_scan:
    st.header("Dokumente scannen")
    if st.button("Scan starten"):
        response = requests.post(f"{BASE_URL}/documents/scan")
        st.write("Response:", response.json())

# --- /query ---
with tab_query:
    st.header("Abfrage")
    query_text = st.text_input("Geben Sie Ihre Abfrage ein:")
    mode = st.selectbox("Modus", ["light", "naive", "mini"])
    stream = st.checkbox("Stream", value=False)
    only_context = st.checkbox("Nur Kontext zurückgeben", value=False)
    if st.button("Abfrage senden"):
        payload = {
            "query": query_text,
            "mode": mode,
            "stream": stream,
            "only_need_context": only_context
        }
        response = requests.post(f"{BASE_URL}/query", json=payload)
        st.write("Response:", response.json())

# --- /graphs ---
with tab_graphs:
    st.header("Graphen")
    label = st.text_input("Label eingeben:", value="default")
    if st.button("Graph abrufen"):
        params = {"label": label}
        response = requests.get(f"{BASE_URL}/graphs", params=params)
        st.write("Response:", response.json())

# --- /health ---
with tab_health:
    st.header("System Health")
    if st.button("Health prüfen"):
        response = requests.get(f"{BASE_URL}/health")
        st.write("Response:", response.json())

# --- /documents (GET und DELETE) ---
with tab_documents:
    st.header("Dokumente Verwaltung")
    if st.button("Dokumente abrufen"):
        response = requests.get(f"{BASE_URL}/documents")
        st.write("Response:", response.json())
    if st.button("Dokumente löschen"):
        response = requests.delete(f"{BASE_URL}/documents")
        st.write("Response:", response.json())
