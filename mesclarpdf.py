import streamlit as st
from PyPDF2 import PdfMerger
import io

# Função para unir PDFs mantendo a qualidade
def unir_pdfs(arquivos):
    merger = PdfMerger()
    for arquivo in arquivos:
        merger.append(arquivo)
    output = io.BytesIO()
    merger.write(output)
    merger.close()
    output.seek(0)
    return output

# Configuração da página
st.set_page_config(page_title="WE ❤️ PDF", layout="centered")

# CSS com estilo Windows 98 + Unicórnio animado (mesmo CSS anterior)
st.markdown("""
<style>
body {
    background-color: #008080;
    font-family: 'MS Sans Serif', sans-serif;
}
h1 {
    font-size: 32px;
    text-align: center;
    text-shadow: 1px 1px 0 #000;
}
.unicorn-surprise {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 9999;
    animation: surprise 3s ease-in-out;
}
@keyframes surprise {
    0% { transform: scale(0) rotate(0deg); opacity: 0; }
    50% { transform: scale(1.2) rotate(360deg); opacity: 1; }
    100% { transform: scale(1) rotate(0deg); opacity: 1; }
}
/* Resto do CSS do unicórnio aqui */
</style>
""", unsafe_allow_html=True)

st.title("WE ❤️ PDF")

arquivos = st.file_uploader("Selecione os arquivos PDF", type=["pdf"], accept_multiple_files=True)

if arquivos:
    if st.button("Unir PDFs"):
        with st.spinner("Unindo PDFs..."):
            pdf_unido = unir_pdfs(arquivos)
            pdf_bytes = pdf_unido.read()
            
        st.success("PDFs unidos com sucesso!")
        
        # Botão de download SEM callback problemático
        st.download_button(
            label="📥 Baixar PDF Unido",
            data=pdf_bytes,
            file_name="pdf_unido.pdf",
            mime="application/pdf"
        )
        
        # Unicórnio aparece automaticamente após o sucesso
        st.markdown("""
        <div class="unicorn-surprise">
            <!-- HTML do unicórnio aqui -->
        </div>
        """, unsafe_allow_html=True)
