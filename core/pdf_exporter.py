"""
Exportador de Dossiê Técnico Dermocosmético em PDF e Markdown
Utiliza ReportLab para gerar documentos técnicos com formatação profissional.
"""

import io
from typing import Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

class PDFExporter:
    """Gera o arquivo PDF do Dossiê Técnico de Formulação Dermocosmética"""

    @staticmethod
    def generate_dossier_pdf(dossier_data: Dict[str, Any]) -> bytes:
        """Gera o PDF em memória (bytes) para download ou salvamento"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        
        # Estilos Customizados
        title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=20,
            leading=24,
            textColor=colors.HexColor('#1A365D'),
            spaceAfter=6
        )
        
        subtitle_style = ParagraphStyle(
            'DocSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=11,
            leading=14,
            textColor=colors.HexColor('#4A5568'),
            spaceAfter=12
        )
        
        h2_style = ParagraphStyle(
            'SectionH2',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=13,
            leading=16,
            textColor=colors.HexColor('#2B6CB0'),
            spaceBefore=12,
            spaceAfter=6
        )

        cell_header_style = ParagraphStyle(
            'CellHeader',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=8.5,
            leading=10,
            textColor=colors.white
        )

        cell_text_style = ParagraphStyle(
            'CellText',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            leading=10,
            textColor=colors.HexColor('#2D3748')
        )

        cell_bold_style = ParagraphStyle(
            'CellBold',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=8,
            leading=10,
            textColor=colors.HexColor('#1A202C')
        )

        story = []

        # 1. Cabeçalho Principal
        story.append(Paragraph(f"Dossiê Técnico: {dossier_data.get('product_title')}", title_style))
        story.append(Paragraph("Dermocare Formulator AI • Relatório Farmacotécnico & Evidência Científica", subtitle_style))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2B6CB0'), spaceAfter=10))

        # 2. Informações Gerais do Produto
        claims_str = ", ".join(dossier_data.get("target_claims", [])) or "Dermocosmética Geral"
        meta_table_data = [
            [
                Paragraph("<b>Veículo Galênico:</b>", cell_bold_style),
                Paragraph(dossier_data.get("vehicle_name", ""), cell_text_style),
                Paragraph("<b>Tipo de Pele:</b>", cell_bold_style),
                Paragraph(dossier_data.get("skin_type", "").title(), cell_text_style)
            ],
            [
                Paragraph("<b>pH Alvo:</b>", cell_bold_style),
                Paragraph(f"{dossier_data.get('target_ph')} ± 0.2", cell_text_style),
                Paragraph("<b>Viscosidade Estimada:</b>", cell_bold_style),
                Paragraph(dossier_data.get("viscosity", ""), cell_text_style)
            ],
            [
                Paragraph("<b>Claims / Alegações:</b>", cell_bold_style),
                Paragraph(claims_str, cell_text_style),
                Paragraph("<b>Totalização da Fórmula:</b>", cell_bold_style),
                Paragraph(f"<b>{dossier_data.get('total_percent', 100.0):.2f}% p/p</b>", cell_bold_style)
            ]
        ]
        meta_table = Table(meta_table_data, colWidths=[1.3*inch, 2.3*inch, 1.3*inch, 2.3*inch])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F7FAFC')),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E0')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 10))

        # 3. Tabela Completa de Composição (% p/p)
        story.append(Paragraph("1. Composição Farmacotécnica Detalhada (% p/p)", h2_style))
        
        formula_headers = [
            Paragraph("Fase", cell_header_style),
            Paragraph("Nomenclatura INCI", cell_header_style),
            Paragraph("Nome Comercial / Descritivo", cell_header_style),
            Paragraph("% p/p", cell_header_style),
            Paragraph("Função na Formulação", cell_header_style)
        ]
        
        formula_rows = [formula_headers]
        phases_dict = dossier_data.get("phases", {})
        
        for phase_name, items in phases_dict.items():
            phase_letter = phase_name.split(" ")[1].replace("(", "")
            for it in items:
                formula_rows.append([
                    Paragraph(f"<b>{phase_letter}</b>", cell_bold_style),
                    Paragraph(it.get("inci", ""), cell_bold_style),
                    Paragraph(it.get("name", ""), cell_text_style),
                    Paragraph(f"<b>{it.get('percent', 0.0):.2f}</b>", cell_bold_style),
                    Paragraph(it.get("function", ""), cell_text_style)
                ])

        formula_table = Table(formula_rows, colWidths=[0.5*inch, 2.2*inch, 1.9*inch, 0.7*inch, 2.1*inch])
        formula_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2B6CB0')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (3, 1), (3, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E0')),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')])
        ]))
        story.append(formula_table)
        story.append(Spacer(1, 10))

        # 4. Avaliação de Segurança e Sinergias
        story.append(Paragraph("2. Avaliação Regulatória, Limites CIR e Sinergias", h2_style))
        safety = dossier_data.get("safety_evaluation", {})
        
        safety_text = f"<b>Status Geral:</b> {'<font color=\"green\">CONFORME & SEGURO</font>' if safety.get('is_safe') else '<font color=\"red\">ATENÇÃO A ALERTAS</font>'} | <b>pH Fisiológico:</b> {safety.get('ph_status')}"
        story.append(Paragraph(safety_text, cell_text_style))
        story.append(Spacer(1, 4))

        if safety.get("synergies"):
            for syn in safety.get("synergies"):
                syn_p = f"• <b>Sinergia ({syn.get('pair')}):</b> {syn.get('benefit')}"
                story.append(Paragraph(syn_p, cell_text_style))
                story.append(Spacer(1, 2))

        if safety.get("warnings"):
            for w in safety.get("warnings"):
                w_p = f"• <font color=\"#C53030\"><b>Aviso ({w.get('type')}):</b> {w.get('message')}</font>"
                story.append(Paragraph(w_p, cell_text_style))
                story.append(Spacer(1, 2))

        story.append(Spacer(1, 8))

        # 5. Evidências Científicas e Publicações no PubMed
        story.append(Paragraph("3. Comprovação Científica Indexada (PubMed / Clinical Evidence)", h2_style))
        
        evidence_list = dossier_data.get("scientific_evidence", [])
        if evidence_list:
            for ev in evidence_list:
                active_hdr = f"<b>Ativo:</b> {ev.get('active_name')} (<i>{ev.get('inci')}</i>)"
                story.append(Paragraph(active_hdr, cell_bold_style))
                story.append(Paragraph(f"<b>Mecanismo Biológico:</b> {ev.get('mechanism')}", cell_text_style))
                story.append(Spacer(1, 3))
                
                studies = ev.get("studies", [])
                for st in studies[:2]:  # Top 2 estudos para caber com elegância
                    study_box = [
                        [Paragraph(f"<b>{st.get('title')}</b>", cell_bold_style)],
                        [Paragraph(f"<i>Autores:</i> {st.get('authors')} | <i>Revista:</i> {st.get('journal')} ({st.get('year')}) | <b>PMID:</b> {st.get('pmid')} | <b>DOI:</b> {st.get('doi')}", cell_text_style)],
                        [Paragraph(f"<b>Conclusão Clínica:</b> {st.get('conclusion')}", cell_text_style)]
                    ]
                    st_table = Table(study_box, colWidths=[7.2*inch])
                    st_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EDF2F7')),
                        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E0')),
                        ('TOPPADDING', (0, 0), (-1, -1), 3),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                    ]))
                    story.append(st_table)
                    story.append(Spacer(1, 4))
                story.append(Spacer(1, 4))

        # 6. Modo de Preparo Galênico
        story.append(Paragraph("4. Procedimento de Manipulação e Fabricação", h2_style))
        for step in dossier_data.get("manufacturing_steps", []):
            story.append(Paragraph(step, cell_text_style))
            story.append(Spacer(1, 2))

        # 7. Protocolo de Estabilidade Acelerada
        story.append(Paragraph("5. Controle de Qualidade e Protocolo de Estabilidade", h2_style))
        stab = dossier_data.get("stability_protocol", {})
        story.append(Paragraph(f"• <b>Estabilidade Preliminar:</b> {stab.get('estabilidade_preliminar')}", cell_text_style))
        story.append(Paragraph(f"• <b>Estabilidade Acelerada:</b> {stab.get('estabilidade_acelerada')}", cell_text_style))

        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes

    @staticmethod
    def generate_dossier_markdown(dossier_data: Dict[str, Any]) -> str:
        """Gera versão em Markdown completa do dossiê"""
        md = []
        md.append(f"# Dossiê Técnico: {dossier_data.get('product_title')}\n")
        md.append(f"**Veículo:** {dossier_data.get('vehicle_name')} | **pH Alvo:** {dossier_data.get('target_ph')} | **Pele:** {dossier_data.get('skin_type')}\n")
        
        md.append("## 1. Composição Farmacotécnica (% p/p)\n")
        md.append("| Fase | INCI | Nome Comercial | % p/p | Função |")
        md.append("| :--- | :--- | :--- | :---: | :--- |")
        
        for phase_name, items in dossier_data.get("phases", {}).items():
            phase_letter = phase_name.split(" ")[1].replace("(", "")
            for it in items:
                md.append(f"| {phase_letter} | **{it.get('inci')}** | {it.get('name')} | {it.get('percent', 0.0):.2f}% | {it.get('function')} |")

        md.append(f"\n**Total da Formulação:** {dossier_data.get('total_percent', 100.0):.2f}% p/p\n")

        md.append("## 2. Evidência Científica Indexada (PubMed)\n")
        for ev in dossier_data.get("scientific_evidence", []):
            md.append(f"### {ev.get('active_name')} (*{ev.get('inci')}*)")
            md.append(f"> **Mecanismo:** {ev.get('mechanism')}\n")
            for st in ev.get("studies", []):
                md.append(f"- **{st.get('title')}**")
                md.append(f"  - *Autores:* {st.get('authors')} ({st.get('year')}) | *Revista:* {st.get('journal')}")
                md.append(f"  - *PMID:* [{st.get('pmid')}]({st.get('url')}) | *DOI:* {st.get('doi')}")
                md.append(f"  - *Conclusão:* {st.get('conclusion')}\n")

        md.append("## 3. Modo de Preparo Galênico\n")
        for step in dossier_data.get("manufacturing_steps", []):
            md.append(f"- {step}")

        return "\n".join(md)
