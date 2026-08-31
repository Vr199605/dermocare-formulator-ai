"""
Dermocare Formulator AI - Interface Web Interativa (Streamlit)
Agente Inteligente de Formulação Dermocosmética com Comprovação Científica no PubMed
"""

import streamlit as st
import pandas as pd
import os
from core.formulator import DermocareFormulator
from core.cosmetic_database import ACTIVE_INGREDIENTS, VEHICLE_CONFIGS
from core.pdf_exporter import PDFExporter

st.set_page_config(
    page_title="Dermocare Formulator AI",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS para visual moderno e dermocosmético
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-box {
        background: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
    }
    .study-card {
        background: #F8FAFC;
        border-left: 4px solid #2563EB;
        padding: 12px 16px;
        border-radius: 4px;
        margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .synergy-card {
        background: #EFF6FF;
        border-left: 4px solid #3B82F6;
        padding: 10px 14px;
        border-radius: 4px;
        margin-bottom: 8px;
    }
    .badge-conforme {
        background-color: #DCFCE7;
        color: #166534;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar o formulador na sessão
if "formulator" not in st.session_state:
    st.session_state.formulator = DermocareFormulator()

if "current_dossier" not in st.session_state:
    st.session_state.current_dossier = None

# Sidebar - Configurações e Presets Rápidos
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/cosmetics.png", width=64)
    st.title("🧪 Dermocare AI")
    st.caption("P&D Dermocosmético & Grounding Científico")
    
    st.markdown("---")
    st.subheader("⚡ Presets de Demonstração")
    
    preset = st.selectbox(
        "Carregar Fórmula Modelo:",
        [
            "Selecione um preset...",
            "Sérum Melasma & Pele Sensível",
            "Creme Barreira com Ceramidas & CICA",
            "Gel-Creme Anti-Acne & Poros (BHA)",
            "Sérum Anti-Aging Bakuchiol (Retinol-Like)"
        ]
    )

    st.markdown("---")
    st.subheader("⚙️ Configurações de IA")
    api_key_input = st.text_input("Gemini API Key (Opcional):", type="password", help="Opcional. Se não informada, o sistema usa a base científica e farmacotécnica interna.")
    if api_key_input:
        st.session_state.formulator = DermocareFormulator(api_key=api_key_input)
        st.success("Chave configurada!")

    st.markdown("---")
    st.markdown("""
    **Bases Científicas Conectadas:**
    - 🏛️ **PubMed / NCBI Entrez**
    - 🔬 **Europe PMC**
    - 🛡️ **CIR / CosIng Safety Guidelines**
    """)

# Cabeçalho Principal
st.markdown('<div class="main-header">🧪 Dermocare Formulator AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Desenvolva formulações dermocosméticas farmacotecnicamente balanceadas com comprovação científica instantânea via PubMed.</div>', unsafe_allow_html=True)

# Definição dos valores padrão de acordo com o preset selecionado
default_title = "Sérum Clareador Facial para Pele Sensível"
default_vehicle = "serum"
default_skin = "Pele Sensível e com Rosácea"
default_claims = ["Clareamento de Melasma / Manchas", "Acalmar Vermelhidão / Anti-inflamatório", "Reparação de Barreira Cutânea"]
default_instructions = "Formulação suave sem fragrância, toque aveludado e rápida absorção."

if preset == "Sérum Melasma & Pele Sensível":
    default_title = "Sérum Clareador Despigmentante Suave"
    default_vehicle = "serum"
    default_skin = "Pele Sensível e com Rosácea"
    default_claims = ["Clareamento de Melasma / Manchas", "Acalmar Vermelhidão / Anti-inflamatório"]
    default_instructions = "Sinergia de Ácido Tranexâmico 3% + Niacinamida 4% com foco em segurança."
elif preset == "Creme Barreira com Ceramidas & CICA":
    default_title = "Creme Reparador de Barreira Lamelar"
    default_vehicle = "barrier_cream"
    default_skin = "Pele Seca, Atópica ou Ressecada"
    default_claims = ["Reparação de Barreira Cutânea", "Hidratação Profunda / Anti-ressecamento", "Acalmar Vermelhidão / Anti-inflamatório"]
    default_instructions = "Emulsão rica em lipídios biomiméticos e esqualano vegetal."
elif preset == "Gel-Creme Anti-Acne & Poros (BHA)":
    default_title = "Gel-Creme Matificante Anti-Acne e Desobstrutor de Poros"
    default_vehicle = "gel_cream"
    default_skin = "Pele Oleosa e Acneica"
    default_claims = ["Controle de Oleosidade / Anti-acne", "Clareamento de Melasma / Manchas"]
    default_instructions = "Ácido Salicílico 1.5% e Niacinamida em gel toque seco com sílica matificante."
elif preset == "Sérum Anti-Aging Bakuchiol (Retinol-Like)":
    default_title = "Sérum Pro-Aging Firmeza & Renovação Vegetal"
    default_vehicle = "serum"
    default_skin = "Pele Madura / Fotoenvelhecida"
    default_claims = ["Anti-idade / Firmeza e Rugas", "Hidratação Profunda / Anti-ressecamento", "Antioxidante / Iluminação"]
    default_instructions = "Alternativa vegana ao retinol com Bakuchiol 1% e Ácido Hialurônico Multimolecular."

# Formulário de Briefing
with st.expander("📝 Configurar Briefing do Produto", expanded=st.session_state.current_dossier is None):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        product_name = st.text_input("Nome do Produto / Projeto:", value=default_title)
        
        claims_options = [
            "Clareamento de Melasma / Manchas",
            "Anti-idade / Firmeza e Rugas",
            "Controle de Oleosidade / Anti-acne",
            "Reparação de Barreira Cutânea",
            "Hidratação Profunda / Anti-ressecamento",
            "Acalmar Vermelhidão / Anti-inflamatório",
            "Antioxidante / Iluminação"
        ]
        selected_claims = st.multiselect("Alegações / Claims Desejados:", claims_options, default=default_claims)
        
        custom_notes = st.text_area("Instruções Especiais / Restrições do Briefing:", value=default_instructions, height=70)

    with col2:
        vehicle_choice = st.selectbox(
            "Forma Farmacêutica / Veículo:",
            options=["serum", "gel_cream", "barrier_cream"],
            format_func=lambda x: {
                "serum": "💧 Sérum Aquoso de Rápida Absorção",
                "gel_cream": "✨ Gel-Creme Toque Seco / Oil-Free",
                "barrier_cream": "🛡️ Creme Reparador Lamelar Nutritivo"
            }[x],
            index=["serum", "gel_cream", "barrier_cream"].index(default_vehicle)
        )
        
        skin_choice = st.selectbox(
            "Tipo de Pele Alvo:",
            options=[
                "Pele Sensível e com Rosácea",
                "Pele Oleosa e Acneica",
                "Pele Seca, Atópica ou Ressecada",
                "Pele Madura / Fotoenvelhecida",
                "Pele Mista / Normal"
            ],
            index=[
                "Pele Sensível e com Rosácea",
                "Pele Oleosa e Acneica",
                "Pele Seca, Atópica ou Ressecada",
                "Pele Madura / Fotoenvelhecida",
                "Pele Mista / Normal"
            ].index(default_skin) if default_skin in [
                "Pele Sensível e com Rosácea",
                "Pele Oleosa e Acneica",
                "Pele Seca, Atópica ou Ressecada",
                "Pele Madura / Fotoenvelhecida",
                "Pele Mista / Normal"
            ] else 0
        )
        
        active_multiselect = st.multiselect(
            "Ativos Específicos (Opcional - deixe vazio para seleção inteligente automática):",
            options=list(ACTIVE_INGREDIENTS.keys()),
            format_func=lambda k: f"{ACTIVE_INGREDIENTS[k]['name_pt']} ({ACTIVE_INGREDIENTS[k]['inci']})"
        )

    btn_generate = st.button("🚀 Gerar Formulação com Comprovação Científica", type="primary", use_container_width=True)

if btn_generate:
    with st.spinner("Analisando farmacotécnica, calculando proporções a 100% e buscando artigos no PubMed..."):
        dossier = st.session_state.formulator.generate_formulation(
            product_title=product_name,
            target_claims=selected_claims,
            skin_type=skin_choice,
            vehicle_type=vehicle_choice,
            custom_instructions=custom_notes,
            custom_actives_selection=active_multiselect if active_multiselect else None
        )
        st.session_state.current_dossier = dossier
        st.success("✅ Formulação e Dossiê Científico gerados com sucesso!")

# Exibição do Dossiê Técnico
if st.session_state.current_dossier:
    dossier = st.session_state.current_dossier
    
    st.markdown("---")
    
    # Linha de Métricas Rápidas
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Forma Galênica", dossier.get("vehicle_name", "").split(" ")[0])
    with m2:
        st.metric("pH Alvo Fisiológico", f"{dossier.get('target_ph')} ± 0.2")
    with m3:
        st.metric("Total da Fórmula", f"{dossier.get('total_percent', 100.0):.2f}% p/p")
    with m4:
        safety_status = "Seguro & Conforme" if dossier["safety_evaluation"]["is_safe"] else "Atenção a Alertas"
        st.metric("Segurança Regulatória", safety_status)

    # Abas de Navegação
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Fórmula Detalhada (% p/p)",
        "🔬 Evidências Científicas (PubMed)",
        "🛡️ Segurança & Sinergias (CIR)",
        "🧪 Processo de Manipulação & CQ",
        "📄 Exportar Dossiê"
    ])

    # TAB 1: Fórmula
    with tab1:
        st.subheader("Composição Farmacotécnica por Fases")
        
        all_phase_rows = []
        for phase_name, items in dossier.get("phases", {}).items():
            st.markdown(f"#### {phase_name}")
            df_phase = pd.DataFrame([
                {
                    "INCI": it.get("inci"),
                    "Nome Comercial": it.get("name"),
                    "Concentração (% p/p)": f"{it.get('percent', 0.0):.2f}%",
                    "Função Galênica": it.get("function")
                }
                for it in items
            ])
            st.dataframe(df_phase, use_container_width=True, hide_index=True)

        st.info(f"💡 **Viscosidade e Aspecto:** {dossier.get('viscosity')}")

    # TAB 2: Evidências Científicas
    with tab2:
        st.subheader("📚 Comprovação Científica Indexada (PubMed / Europe PMC)")
        st.caption("Artigos clínicos reais recuperados para respaldar os claims de eficácia e mecanismos de ação.")
        
        for ev in dossier.get("scientific_evidence", []):
            with st.container():
                st.markdown(f"### 🧬 {ev.get('active_name')} (`{ev.get('inci')}`)")
                st.markdown(f"**Mecanismo de Ação Biológico:** {ev.get('mechanism')}")
                
                studies = ev.get("studies", [])
                if studies:
                    for s in studies:
                        st.markdown(f"""
                        <div class="study-card">
                            <div style="font-weight: 700; color: #1E293B; font-size: 1.05rem;">📄 {s.get('title')}</div>
                            <div style="color: #64748B; font-size: 0.85rem; margin: 4px 0;">
                                <b>Autores:</b> {s.get('authors')} | <b>Revista:</b> {s.get('journal')} ({s.get('year')}) | <b>Tipo:</b> {s.get('study_type')}
                            </div>
                            <div style="margin-top: 6px; color: #334155; font-size: 0.92rem;">
                                <b>💡 Conclusão Clínica:</b> {s.get('conclusion')}
                            </div>
                            <div style="margin-top: 6px;">
                                <a href="{s.get('url')}" target="_blank" style="text-decoration: none; color: #2563EB; font-weight: 600; font-size: 0.85rem;">
                                    🔗 Ver Estudo no PubMed (PMID: {s.get('pmid')}) →
                                </a>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.write("Nenhum estudo adicional localizado para esta combinação específica.")
                st.markdown("---")

    # TAB 3: Segurança e Sinergias
    with tab3:
        st.subheader("🛡️ Avaliação Regulatória e Sinergias de Ativos")
        
        safety = dossier.get("safety_evaluation", {})
        
        # Sinergias
        st.markdown("#### ✨ Sinergias Positivas Mapeadas")
        if safety.get("synergies"):
            for syn in safety.get("synergies"):
                st.markdown(f"""
                <div class="synergy-card">
                    <b>{syn.get('pair')}:</b> {syn.get('benefit')}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.write("Nenhuma interação sinérgica negativa ou positiva de destaque.")

        # Tabela de Limites Regulatórios
        st.markdown("#### ⚖️ Checagem de Limites Toxicológicos (CIR / ANVISA / CosIng)")
        df_reg = pd.DataFrame(safety.get("regulatory_checks", []))
        if not df_reg.empty:
            st.dataframe(df_reg, use_container_width=True, hide_index=True)

        # Alertas e Incompatibilidades
        if safety.get("warnings"):
            st.markdown("#### ⚠️ Alertas Farmacotécnicos")
            for w in safety.get("warnings"):
                st.warning(f"**{w.get('type')}:** {w.get('message')}")

    # TAB 4: Modo de Preparo
    with tab4:
        st.subheader("🧪 Procedimento Operacional Padrão (POP) de Manipulação")
        for step in dossier.get("manufacturing_steps", []):
            st.markdown(f"{step}")
            
        st.markdown("---")
        st.subheader("🔬 Protocolo de Controle de Qualidade e Estabilidade (ANVISA)")
        stab = dossier.get("stability_protocol", {})
        st.markdown(f"**Estabilidade Preliminar:** {stab.get('estabilidade_preliminar')}")
        st.markdown(f"**Estabilidade Acelerada:** {stab.get('estabilidade_acelerada')}")
        
        specs = stab.get("especificacoes_controle", {})
        st.json(specs)

    # TAB 5: Exportação
    with tab5:
        st.subheader("📄 Exportar Dossiê Técnico Completo")
        
        col_pdf, col_md = st.columns(2)
        
        with col_pdf:
            pdf_bytes = PDFExporter.generate_dossier_pdf(dossier)
            st.download_button(
                label="📥 Baixar Dossiê em PDF Profissional",
                data=pdf_bytes,
                file_name=f"Dossie_Tecnico_{dossier.get('product_title').replace(' ', '_')}.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True
            )
            st.caption("PDF formatado com tabelas de fases, evidências indexadas e protocolo de fabricação.")

        with col_md:
            md_content = PDFExporter.generate_dossier_markdown(dossier)
            st.download_button(
                label="📋 Baixar em Markdown / Texto",
                data=md_content,
                file_name=f"Dossie_{dossier.get('product_title').replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True
            )

        with st.expander("Visualizar Markdown Bruto"):
            st.code(md_content, language="markdown")
