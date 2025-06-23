import streamlit as st
from PyPDF2 import PdfMerger
import base64
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

# Função para gerar link de download
def gerar_link_download(pdf_bytes, nome_arquivo):
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{nome_arquivo}" id="download-link">Clique aqui para baixar o PDF unido</a>'
    return href

# Configuração da página
st.set_page_config(page_title="WE ❤️ PDF", layout="centered")

# Estilo Windows 98
st.markdown("""
<style>
body {
    background-color: #008080;
    font-family: 'MS Sans Serif', Tahoma, Geneva, Verdana, sans-serif;
    color: white;
}
h1 {
    font-size: 32px;
    font-weight: bold;
    text-align: center;
    margin-top: 20px;
    margin-bottom: 20px;
    text-shadow: 1px 1px 0 #000;
}
button, .stButton>button {
    font-family: 'MS Sans Serif', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 14px;
    background-color: #c0c0c0;
    border: 2px outset #fff;
    padding: 5px 10px;
    cursor: pointer;
}
.stFileUploader {
    background-color: #c0c0c0;
    border: 2px inset #fff;
}
</style>
""", unsafe_allow_html=True)

st.title("WE ❤️ PDF")

# Upload de arquivos
arquivos = st.file_uploader(
    "Selecione os arquivos PDF", 
    type=["pdf"], 
    accept_multiple_files=True
)

# Estado para exibir unicórnio após download
if 'show_unicorn' not in st.session_state:
    st.session_state['show_unicorn'] = False

if arquivos:
    if st.button("Unir PDFs"):
        pdf_unido = unir_pdfs(arquivos)
        st.success("PDFs unidos com sucesso!")
        # Botão de download customizado
        st.markdown(gerar_link_download(pdf_unido.read(), "pdf_unido.pdf"), unsafe_allow_html=True)
        # Script para detectar clique no link de download
        st.markdown("""
        <script>
        const link = window.parent.document.getElementById("download-link");
        if (link) {
            link.onclick = function() {
                window.parent.postMessage("show_unicorn", "*");
            }
        }
        window.addEventListener("message", (event) => {
            if (event.data === "show_unicorn") {
                const unicorn = document.getElementById("unicorn-img");
                if (unicorn) {
                    unicorn.style.display = "block";
                    setTimeout(() => { unicorn.style.display = "none"; }, 5000);
                }
            }
        });
        </script>
        <img id="unicorn-img" src="https://i.imgur.com/4AiXzf8.jpeg" style="display:none;position:fixed;bottom:20px;right:20px;max-width:300px;z-index:9999;" />
        """, unsafe_allow_html=True)
