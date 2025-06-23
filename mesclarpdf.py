
import streamlit as st
from PyPDF2 import PdfMerger
import io
import time
import re
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

st.set_page_config(layout="centered", page_title="Unir PDFs - Windows 98 Style")

st.markdown("""
<style>
    @font-face {
        font-family: 'W98';
        src: url('https://unpkg.com/xp.css/dist/fonts/MS-Sans-Serif.woff2') format('woff2');
    }
    body {
        font-family: 'W98', sans-serif;
        background-color: #008080; /* Teal color of Windows 98 */
        color: #000000;
    }
    .stApp {
        background-color: #C0C0C0; /* Grey background for the app */
        border: 2px solid white;
        border-right: 2px solid black;
        border-bottom: 2px solid black;
        padding: 10px;
        box-shadow: 5px 5px 0px black;
    }
    .stButton>button {
        background-color: #C0C0C0;
        border: 2px solid white;
        border-right: 2px solid black;
        border-bottom: 2px solid black;
        padding: 5px 10px;
        font-family: 'W98', sans-serif;
        font-size: 16px;
    }
    .stButton>button:active {
        background-color: #D0D0D0;
        border: 2px solid black;
        border-right: 2px solid white;
        border-bottom: 2px solid white;
    }
    .stFileUploader>div>div>button {
        background-color: #C0C0C0;
        border: 2px solid white;
        border-right: 2px solid black;
        border-bottom: 2px solid black;
        padding: 5px 10px;
        font-family: 'W98', sans-serif;
        font-size: 16px;
    }
    .stFileUploader>div>div>button:active {
        background-color: #D0D0D0;
        border: 2px solid black;
        border-right: 2px solid white;
        border-bottom: 2px solid white;
    }
    .stFileUploader>div>div>div>div>label {
        font-family: 'W98', sans-serif;
        font-size: 16px;
    }
    h1 {
        color: #000000;
        font-family: 'W98', sans-serif;
        text-shadow: 1px 1px #FFFFFF;
    }
    .css-1d391kg {
        background-color: #C0C0C0;
        border: 2px solid white;
        border-right: 2px solid black;
        border-bottom: 2px solid black;
        padding: 10px;
        box-shadow: 5px 5px 0px black;
    }
    
    /* Efeito especial do unicórnio */
    .unicorn-surprise {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 9999;
        display: none;
        animation: unicornJump 2s ease-in-out;
        font-size: 100px;
        text-shadow: 0 0 20px #ff69b4;
    }
    
    .rainbow-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 9998;
        display: none;
        background: linear-gradient(45deg, 
            #ff0000, #ff7f00, #ffff00, #00ff00, 
            #0000ff, #4b0082, #9400d3, #ff0000);
        background-size: 400% 400%;
        animation: rainbowMove 1s ease-in-out;
        opacity: 0.8;
    }
    
    @keyframes unicornJump {
        0% { transform: translate(-50%, 200%); }
        50% { transform: translate(-50%, -50%) scale(1.5); }
        100% { transform: translate(-50%, -200%); }
    }
    
    @keyframes rainbowMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .shake {
        animation: shake 0.5s;
    }
    
    @keyframes shake {
        0% { transform: translate(1px, 1px) rotate(0deg); }
        10% { transform: translate(-1px, -2px) rotate(-1deg); }
        20% { transform: translate(-3px, 0px) rotate(1deg); }
        30% { transform: translate(3px, 2px) rotate(0deg); }
        40% { transform: translate(1px, -1px) rotate(1deg); }
        50% { transform: translate(-1px, 2px) rotate(-1deg); }
        60% { transform: translate(-3px, 1px) rotate(0deg); }
        70% { transform: translate(3px, 1px) rotate(-1deg); }
        80% { transform: translate(-1px, -1px) rotate(1deg); }
        90% { transform: translate(1px, 2px) rotate(0deg); }
        100% { transform: translate(1px, -2px) rotate(-1deg); }
    }
</style>

<div class="rainbow-bg" id="rainbowBg"></div>
<div class="unicorn-surprise" id="unicornSurprise">🦄🌈</div>

<script>
function triggerUnicornSurprise() {
    const rainbow = document.getElementById('rainbowBg');
    const unicorn = document.getElementById('unicornSurprise');
    const app = document.querySelector('.stApp');
    
    // Mostrar efeitos
    rainbow.style.display = 'block';
    unicorn.style.display = 'block';
    app.classList.add('shake');
    
    // Tocar som de susto (se possível)
    try {
        const audio = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSuBzvLZiTYIG2m98OScTgwOUarm7blmGgU7k9n1unEiBC13yO/eizEIHWq+8+OWT');
        audio.play();
    } catch(e) {}
    
    // Remover efeitos após 2 segundos
    setTimeout(() => {
        rainbow.style.display = 'none';
        unicorn.style.display = 'none';
        app.classList.remove('shake');
    }, 2000);
}

// Detectar clique no botão de download
document.addEventListener('click', function(e) {
    if (e.target.textContent && e.target.textContent.includes('Baixar PDF')) {
        setTimeout(triggerUnicornSurprise, 100);
    }
});
</script>
""", unsafe_allow_html=True)

st.title("🦄 Unir PDFs - Estilo Windows 98 🌈")

st.write("Faça o upload de seus arquivos PDF para uni-los em um único documento.")
st.write("⚡ Suporta até 100 PDFs com máxima qualidade!")

uploaded_files = st.file_uploader(
    "Escolha os arquivos PDF", 
    type="pdf", 
    accept_multiple_files=True,
    help="Selecione múltiplos arquivos PDF para unir em um só documento"
)

if uploaded_files:
    st.success(f"📁 {len(uploaded_files)} arquivo(s) carregado(s)")
    
    # Opções de ordenação
    st.subheader("🔄 Ordenação dos arquivos")
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
    
    if st.button("🔗 Unir PDFs", type="primary"):
        merged_pdf = merge_pdfs(sorted_files)
        
        if merged_pdf:
            st.balloons()
            
            # Calcular tamanho do arquivo final
            file_size = len(merged_pdf.getvalue())
            file_size_mb = file_size / (1024 * 1024)
            
            st.success(f"🎉 PDFs unidos com sucesso! Tamanho final: {file_size_mb:.2f} MB")
            
            # Botão de download com efeito especial
            st.download_button(
                label="📥 Baixar PDF Unido",
                data=merged_pdf,
                file_name="pdfs_unidos.pdf",
                mime="application/pdf",
                help="Clique para baixar o PDF unido (prepare-se para uma surpresa! 🦄)"
            )
else:
    st.info("👆 Selecione os arquivos PDF acima para começar")

# Rodapé
st.markdown("---")
st.markdown("💡 **Dica:** Esta aplicação mantém a qualidade original dos PDFs durante a união!")
st.markdown("🎨 **Estilo:** Windows 98 Retro com surpresas especiais!")


