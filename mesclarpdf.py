import streamlit as st
from PyPDF2 import PdfMerger
import io

def unir_pdfs(arquivos):
    merger = PdfMerger()
    for arquivo in arquivos:
        merger.append(arquivo)
    output = io.BytesIO()
    merger.write(output)
    merger.close()
    output.seek(0)
    return output

st.set_page_config(page_title="WE ❤️ PDF")

# CSS simples sem animações complexas
st.markdown("""
<style>
.main { background-color: #2e2e2e; }
h1 { color: #ff6b6b; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.title("WE ❤️ PDF")

arquivos = st.file_uploader("Selecione os PDFs", type=["pdf"], accept_multiple_files=True)

if arquivos and len(arquivos) > 0:
    if st.button("Unir PDFs"):
        pdf_unido = unir_pdfs(arquivos)
        st.success("Pronto!")
        
        st.download_button(
            "Baixar PDF",
            data=pdf_unido.read(),
            file_name="pdf_unido.pdf",
            mime="application/pdf"
        )
        
        # Unicórnio simples em texto
        st.markdown("🦄🌈 SURPRESA! 🌈🦄")
