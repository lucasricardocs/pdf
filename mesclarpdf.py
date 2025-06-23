import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
import io

def pagina_em_branco(pagina):
    """Verifica se uma página PDF está em branco"""
    texto = pagina.extract_text()
    if texto is None or texto.strip() == "":
        return True
    return False

def remover_paginas_em_branco(arquivo_pdf):
    """Remove páginas em branco de um PDF"""
    reader = PdfReader(arquivo_pdf)
    writer = PdfWriter()
    
    for pagina in reader.pages:
        if not pagina_em_branco(pagina):
            writer.add_page(pagina)
    
    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    return output

def unir_pdfs_sem_branco(arquivos):
    """Une PDFs removendo páginas em branco"""
    writer = PdfWriter()
    
    for arquivo in arquivos:
        # Remove páginas em branco de cada arquivo
        arquivo_limpo = remover_paginas_em_branco(arquivo)
        reader = PdfReader(arquivo_limpo)
        
        # Adiciona apenas páginas com conteúdo
        for pagina in reader.pages:
            writer.add_page(pagina)
    
    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    return output

st.set_page_config(page_title="WE ❤️ PDF")

# Interface limpa e escura
st.markdown("""
<style>
.main { background-color: #2e2e2e; }
h1 { color: #ff6b6b; text-align: center; }
.stSuccess { background-color: #1e3a1e; }
</style>
""", unsafe_allow_html=True)

st.title("WE ❤️ PDF")

arquivos = st.file_uploader("Selecione os PDFs", type=["pdf"], accept_multiple_files=True)

# Opção para remover páginas em branco
remover_branco = st.checkbox("Remover páginas em branco", value=True)

if arquivos and len(arquivos) > 0:
    if st.button("Unir PDFs"):
        with st.spinner("Processando PDFs..."):
            if remover_branco:
                pdf_unido = unir_pdfs_sem_branco(arquivos)
                st.success("PDFs unidos com páginas em branco removidas!")
            else:
                # Função original sem remoção
                from PyPDF2 import PdfMerger
                merger = PdfMerger()
                for arquivo in arquivos:
                    merger.append(arquivo)
                output = io.BytesIO()
                merger.write(output)
                merger.close()
                output.seek(0)
                pdf_unido = output
                st.success("PDFs unidos!")
        
        st.download_button(
            "📥 Baixar PDF Limpo",
            data=pdf_unido.read(),
            file_name="pdf_unido_limpo.pdf",
            mime="application/pdf"
        )
        
        st.markdown("🦄🌈 **SURPRESA!** PDF limpo e organizado! 🌈🦄")
