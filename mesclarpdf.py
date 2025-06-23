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

# Configuração da página
st.set_page_config(page_title="WE ❤️ PDF", layout="centered")

# CSS com estilo Windows 98 + Unicórnio animado
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

/* Unicórnio Animado CSS */
.unicorn-surprise {
    display: none;
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

.unicorn {
    width: 200px;
    height: 150px;
    position: relative;
}

.unicorn-head {
    width: 60px;
    height: 50px;
    background: #fff;
    border-radius: 50%;
    position: absolute;
    top: 20px;
    left: 70px;
    border: 2px solid #ddd;
}

.horn {
    width: 0;
    height: 0;
    border-left: 8px solid transparent;
    border-right: 8px solid transparent;
    border-bottom: 30px solid #ffddab;
    position: absolute;
    top: -25px;
    left: 22px;
    animation: horn-glow 2s infinite;
}

@keyframes horn-glow {
    0%, 100% { filter: brightness(1); }
    50% { filter: brightness(1.5) hue-rotate(45deg); }
}

.eye {
    width: 8px;
    height: 8px;
    background: #502e75;
    border-radius: 50%;
    position: absolute;
    top: 15px;
}

.eye-left { left: 15px; }
.eye-right { right: 15px; }

.unicorn-body {
    width: 80px;
    height: 60px;
    background: #fff;
    border-radius: 40px;
    position: absolute;
    top: 50px;
    left: 60px;
    border: 2px solid #ddd;
}

.leg {
    width: 12px;
    height: 30px;
    background: #cdd1d2;
    position: absolute;
    top: 100px;
    border-radius: 6px;
}

.leg1 { left: 65px; }
.leg2 { left: 80px; }
.leg3 { left: 110px; }
.leg4 { left: 125px; }

.tail {
    width: 40px;
    height: 20px;
    background: linear-gradient(45deg, #ff2220, #ffae00, #ffe100, #85c900, #00b0ff, #8139df, #ff40e1);
    border-radius: 20px;
    position: absolute;
    top: 60px;
    right: 10px;
    animation: tail-wave 1s infinite;
}

@keyframes tail-wave {
    0%, 100% { transform: rotate(-10deg); }
    50% { transform: rotate(10deg); }
}

.rainbow {
    width: 150px;
    height: 20px;
    background: linear-gradient(to right, #ff2220, #ffae00, #ffe100, #85c900, #00b0ff, #8139df, #ff40e1);
    border-radius: 10px;
    position: absolute;
    top: 120px;
    left: 25px;
    animation: rainbow-flow 2s linear infinite;
}

@keyframes rainbow-flow {
    0% { background-position: 0% 50%; }
    100% { background-position: 200% 50%; }
}

.mane {
    width: 30px;
    height: 40px;
    background: linear-gradient(45deg, #ff40e1, #8139df, #00b0ff);
    border-radius: 15px;
    position: absolute;
    top: 10px;
    left: 45px;
    animation: mane-flow 3s ease-in-out infinite;
}

@keyframes mane-flow {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-5px); }
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

# Estado para controlar o unicórnio
if 'show_unicorn' not in st.session_state:
    st.session_state['show_unicorn'] = False

if arquivos:
    if st.button("Unir PDFs"):
        with st.spinner("Unindo PDFs..."):
            pdf_unido = unir_pdfs(arquivos)
            pdf_bytes = pdf_unido.read()
            
        st.success("PDFs unidos com sucesso!")
        
        # Botão de download
        st.download_button(
            label="📥 Baixar PDF Unido",
            data=pdf_bytes,
            file_name="pdf_unido.pdf",
            mime="application/pdf",
            on_click=lambda: setattr(st.session_state, 'show_unicorn', True)
        )

# Exibir unicórnio quando download for clicado
if st.session_state.get('show_unicorn', False):
    st.markdown("""
    <div class="unicorn-surprise" style="display: block;">
        <div class="unicorn">
            <div class="unicorn-head">
                <div class="horn"></div>
                <div class="eye eye-left"></div>
                <div class="eye eye-right"></div>
                <div class="mane"></div>
            </div>
            <div class="unicorn-body"></div>
            <div class="leg leg1"></div>
            <div class="leg leg2"></div>
            <div class="leg leg3"></div>
            <div class="leg leg4"></div>
            <div class="tail"></div>
            <div class="rainbow"></div>
        </div>
    </div>
    <script>
    setTimeout(function() {
        const unicorn = document.querySelector('.unicorn-surprise');
        if (unicorn) unicorn.style.display = 'none';
    }, 5000);
    </script>
    """, unsafe_allow_html=True)
    
    # Reset do estado após 5 segundos
    import time
    time.sleep(0.1)
    st.session_state['show_unicorn'] = False
    st.rerun()
