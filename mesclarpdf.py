import streamlit as st
from PyPDF2 import PdfMerger
import io
import time
import natsort

def sort_files(files, sort_option):
    """
    Ordena os arquivos conforme a opção selecionada
    """
    if sort_option == "Ordem de seleção":
        return files
    elif sort_option == "Alfabética (A-Z)":
        return sorted(files, key=lambda x: x.name.lower())
    elif sort_option == "Alfabética (Z-A)":
        return sorted(files, key=lambda x: x.name.lower(), reverse=True)
    elif sort_option == "Numérica":
        return natsort.natsorted(files, key=lambda x: x.name)
    else:
        return files

def merge_pdfs(pdf_files):
    """
    Une múltiplos PDFs mantendo a máxima qualidade possível
    """
    merger = PdfMerger()
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        total_files = len(pdf_files)
        
        for i, pdf_file in enumerate(pdf_files):
            status_text.text(f'Processando arquivo {i+1} de {total_files}: {pdf_file.name}')
            
            # Reset file pointer
            pdf_file.seek(0)
            pdf_bytes = io.BytesIO(pdf_file.read())
            
            # Append PDF mantendo qualidade original
            merger.append(pdf_bytes)
            
            # Atualizar barra de progresso
            progress = (i + 1) / total_files
            progress_bar.progress(progress)
            
            # Pequena pausa para não sobrecarregar
            time.sleep(0.01)
        
        status_text.text('Finalizando união dos PDFs...')
        
        # Criar arquivo final
        output_pdf = io.BytesIO()
        merger.write(output_pdf)
        merger.close()
        output_pdf.seek(0)
        
        progress_bar.progress(1.0)
        status_text.text('✅ PDFs unidos com sucesso!')
        
        return output_pdf
        
    except Exception as e:
        st.error(f"Erro ao unir PDFs: {str(e)}")
        return None

st.set_page_config(layout="centered", page_title="WE ❤️ PDFs")

st.markdown("""
<style>
    .stApp {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    .main {
        background-color: #1a1a1a;
        padding: 2rem;
    }
    
    h1 {
        color: #ff6b6b;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    
    .stButton > button {
        background-color: #4ecdc4;
        color: #1a1a1a;
        border: none;
        border-radius: 5px;
        padding: 0.75rem 1.5rem;
        font-weight: bold;
        font-size: 1rem;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #45b7aa;
    }
    
    .stFileUploader {
        background-color: #2d2d2d;
        border: 2px dashed #4ecdc4;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
    }
    
    .stSelectbox > div > div {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #4ecdc4;
    }
    
    .stExpander {
        background-color: #2d2d2d;
        border: 1px solid #4ecdc4;
        border-radius: 5px;
    }
    
    .stSuccess {
        background-color: #2d4a2d;
        color: #90ee90;
        border: 1px solid #4caf50;
    }
    
    .stInfo {
        background-color: #2d2d4a;
        color: #87ceeb;
        border: 1px solid #2196f3;
    }
    
    .stError {
        background-color: #4a2d2d;
        color: #ffb3b3;
        border: 1px solid #f44336;
    }
    
    .stProgress > div > div {
        background-color: #4ecdc4;
    }
    
    .stDownloadButton > button {
        background-color: #ff6b6b;
        color: #ffffff;
        border: none;
        border-radius: 5px;
        padding: 0.75rem 1.5rem;
        font-weight: bold;
        font-size: 1rem;
        width: 100%;
    }
    
    .stDownloadButton > button:hover {
        background-color: #ff5252;
    }
    
    hr {
        border-color: #4ecdc4;
    }
    
    .stMarkdown {
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

st.title("WE ❤️ PDFs")

st.write("Faça o upload de seus arquivos PDF para uni-los em um único documento.")
st.write("Suporta até 100 PDFs com máxima qualidade!")

uploaded_files = st.file_uploader(
    "Escolha os arquivos PDF", 
    type="pdf", 
    accept_multiple_files=True,
    help="Selecione múltiplos arquivos PDF para unir em um só documento"
)

if uploaded_files:
    st.success(f"📁 {len(uploaded_files)} arquivo(s) carregado(s)")
    
    # Opções de ordenação
    st.subheader("Ordenação dos arquivos")
    sort_option = st.selectbox(
        "Como deseja ordenar os PDFs antes de uni-los?",
        ["Ordem de seleção", "Alfabética (A-Z)", "Alfabética (Z-A)", "Numérica"],
        help="A ordem numérica é inteligente e ordena corretamente arquivos como: arquivo1.pdf, arquivo2.pdf, arquivo10.pdf"
    )
    
    # Aplicar ordenação
    sorted_files = sort_files(uploaded_files, sort_option)
    
    # Mostrar lista de arquivos ordenados
    with st.expander("Ver arquivos na ordem de união"):
        for i, file in enumerate(sorted_files, 1):
            st.write(f"{i}. {file.name} ({file.size} bytes)")
    
    if st.button("Unir PDFs", type="primary"):
        merged_pdf = merge_pdfs(sorted_files)
        
        if merged_pdf:
            # Calcular tamanho do arquivo final
            file_size = len(merged_pdf.getvalue())
            file_size_mb = file_size / (1024 * 1024)
            
            st.success(f"PDFs unidos com sucesso! Tamanho final: {file_size_mb:.2f} MB")
            
            # Botão de download
            st.download_button(
                label="Baixar PDF Unido",
                data=merged_pdf,
                file_name="pdfs_unidos.pdf",
                mime="application/pdf"
            )
else:
    st.info("Selecione os arquivos PDF acima para começar")

# Rodapé
st.markdown("---")
st.markdown("**Dica:** Esta aplicação mantém a qualidade original dos PDFs durante a união!")
