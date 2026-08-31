"""
Base de Dados Farmacotécnica e Dermocosmética
Contém ingredientes INCI, fases usuais, limites de concentração (CIR/ANVISA/CosIng),
faixas de pH ideais, funções e termos de busca científica para o PubMed.
"""

from typing import Dict, List, Any

# Ativos Dermocosméticos com metadados e termos de busca científica
ACTIVE_INGREDIENTS: Dict[str, Dict[str, Any]] = {
    "tranexamic_acid": {
        "inci": "Tranexamic Acid",
        "name_pt": "Ácido Tranexâmico",
        "category": "Clareador / Anti-inflamatório",
        "default_percent": 3.0,
        "min_percent": 1.0,
        "max_percent": 5.0,
        "safe_limit": 5.0,
        "phase": "C",
        "ph_range": (5.0, 7.0),
        "indication": ["melasma", "hiperpigmentacao", "manchas", "vermelhidao", "rosacea", "anti-manchas"],
        "mechanism": "Inibidor da via do ativador de plasminogênio; bloqueia a liberação de ácido araquidônico e prostaglandinas que estimulam a melanogênese.",
        "pubmed_query": '("Tranexamic Acid"[Title/Abstract]) AND (melasma OR "hyperpigmentation" OR skin) AND (trial OR clinical OR double-blind)'
    },
    "niacinamide": {
        "inci": "Niacinamide",
        "name_pt": "Niacinamida (Vitamina B3)",
        "category": "Multifuncional / Barreira / Clareador",
        "default_percent": 4.0,
        "min_percent": 2.0,
        "max_percent": 5.0,
        "safe_limit": 10.0,
        "phase": "C",
        "ph_range": (5.0, 6.5),
        "indication": ["melasma", "acne", "oleosidade", "barreira", "anti-idade", "pele_sensivel", "poros"],
        "mechanism": "Inibe a transferência de melanossomas dos melanócitos para os queratinócitos em até 68%; estimula a síntese de ceramidas e filagrina.",
        "pubmed_query": '("Niacinamide"[Title/Abstract] OR "Nicotinamide"[Title/Abstract]) AND (skin OR barrier OR melasma OR acne) AND (clinical OR "double-blind")'
    },
    "alpha_arbutin": {
        "inci": "Alpha-Arbutin",
        "name_pt": "Alfa-Arbutin",
        "category": "Clareador",
        "default_percent": 1.5,
        "min_percent": 0.5,
        "max_percent": 2.0,
        "safe_limit": 2.0,  # SCCS/CIR limit for face products
        "phase": "C",
        "ph_range": (4.5, 6.5),
        "indication": ["melasma", "hiperpigmentacao", "manchas", "sardas"],
        "mechanism": "Inibidor competitivo da enzima tirosinase por analogia estrutural ao substrato L-tirosina, sem citotoxicidade melanocítica.",
        "pubmed_query": '("Alpha-Arbutin"[Title/Abstract] OR "Arbutin"[Title/Abstract]) AND (tyrosinase OR hyperpigmentation OR skin) AND (clinical OR in vivo)'
    },
    "hyaluronic_acid_multi": {
        "inci": "Sodium Hyaluronate (Multi-Molecular Weight)",
        "name_pt": "Ácido Hialurônico Multimolecular",
        "category": "Hidratante / Preenchedor",
        "default_percent": 1.0,
        "min_percent": 0.1,
        "max_percent": 2.0,
        "safe_limit": 2.5,
        "phase": "C",
        "ph_range": (4.0, 7.5),
        "indication": ["hidratacao", "anti-idade", "linhas_finas", "pele_seca", "pele_sensivel", "barreira"],
        "mechanism": "Fração de alto peso molecular (1.5 MDa) forma filme não oclusivo retentor de água; fração de baixo peso (<50 kDa) penetra na epiderme estimulando CD44 e síntese endógena de colágeno.",
        "pubmed_query": '("Sodium Hyaluronate"[Title/Abstract] OR "Hyaluronic Acid"[Title/Abstract]) AND (skin hydration OR wrinkles OR barrier) AND (clinical OR trial)'
    },
    "salicylic_acid": {
        "inci": "Salicylic Acid",
        "name_pt": "Ácido Salicílico (BHA)",
        "category": "Queratorregulador / Anti-acne",
        "default_percent": 1.5,
        "min_percent": 0.5,
        "max_percent": 2.0,
        "safe_limit": 2.0,  # CIR & ANVISA OTC leave-on limit
        "phase": "C",
        "ph_range": (3.5, 4.5),
        "indication": ["acne", "oleosidade", "cravos", "poros_dilatados", "esfoliacao"],
        "mechanism": "Beta-hidroxiácido lipofílico com afinidade pelo ducto pilossebáceo; atua desfazendo desmossomos intercelulares e possui ação anti-inflamatória intrínseca.",
        "pubmed_query": '("Salicylic Acid"[Title/Abstract]) AND (acne vulgaris OR comedones OR sebum) AND (clinical OR trial)'
    },
    "retinol_encapsulated": {
        "inci": "Retinol (and) Phospholipids",
        "name_pt": "Retinol Encapsulado",
        "category": "Anti-idade / Renovação Celular",
        "default_percent": 0.3,
        "min_percent": 0.1,
        "max_percent": 0.5,
        "safe_limit": 0.3,  # SCCS safe limit for face products (0.3% pure eq.)
        "phase": "C",
        "ph_range": (5.5, 6.5),
        "indication": ["anti-idade", "rugas_profundas", "firmeza", "textura", "fotoenvelhecimento"],
        "mechanism": "Ativa receptores nucleares RAR/RXR, promovendo expressão de pró-colágeno I e III e inibindo a metaloproteinase MMP-1 gerada por radiação UV.",
        "pubmed_query": '("Retinol"[Title/Abstract] OR "Retinoids"[Title/Abstract]) AND (anti-aging OR collagen OR wrinkles OR photoaging) AND (clinical OR double-blind)'
    },
    "centella_asiatica_extract": {
        "inci": "Centella Asiatica (Madecassoside & Asiaticoside) Extract",
        "name_pt": "Extrato de Centella Asiática (CICA)",
        "category": "Calmante / Cicatrizante / Barreira",
        "default_percent": 1.0,
        "min_percent": 0.5,
        "max_percent": 3.0,
        "safe_limit": 5.0,
        "phase": "C",
        "ph_range": (4.5, 7.0),
        "indication": ["pele_sensivel", "vermelhidao", "rosacea", "cicatrizacao", "reparacao_barreira"],
        "mechanism": "Triterpenoides (madecassosídeo e asiaticosídeo) reduzem citocinas pró-inflamatórias (IL-1b, TNF-a) e estimulam fibroblastos via via TGF-beta/Smad.",
        "pubmed_query": '("Centella Asiatica"[Title/Abstract] OR "Madecassoside"[Title/Abstract]) AND (skin OR barrier OR wound OR inflammation) AND (clinical OR study)'
    },
    "ceramide_complex": {
        "inci": "Ceramide NP (and) Ceramide AP (and) Ceramide EOP (and) Phytosphingosine (and) Cholesterol",
        "name_pt": "Complexo Lipídico de Ceramidas Idênticas à Pele",
        "category": "Reparação de Barreira Cutânea",
        "default_percent": 2.0,
        "min_percent": 1.0,
        "max_percent": 5.0,
        "safe_limit": 10.0,
        "phase": "C",
        "ph_range": (5.0, 6.5),
        "indication": ["barreira", "pele_seca", "pele_sensivel", "dermatite", "pos_procedimento"],
        "mechanism": "Restaura a estrutura lamelar intercelular do estrato córneo na proporção estequiométrica de lipídios fisiológicos, reduzindo a perda transepidérmica de água (TEWL).",
        "pubmed_query": '("Ceramides"[Title/Abstract] OR "Ceramide NP"[Title/Abstract]) AND ("transepidermal water loss" OR "skin barrier" OR hydration) AND (clinical OR trial)'
    },
    "azelaic_acid": {
        "inci": "Azelaic Acid",
        "name_pt": "Ácido Azelaico",
        "category": "Anti-acne / Anti-rosácea / Despigmentante",
        "default_percent": 5.0,
        "min_percent": 2.0,
        "max_percent": 10.0,
        "safe_limit": 10.0,  # Cosmetic max limit (above 10% is usually Rx/medical)
        "phase": "C",
        "ph_range": (4.5, 5.5),
        "indication": ["acne", "rosacea", "melasma", "hiperpigmentacao_pos_inflamatoria", "vermelhidao"],
        "mechanism": "Ação bacteriostática contra Cutibacterium acnes via inibição de síntese proteica celular; inibidor reversível da tirosinase em melanócitos hiperativos.",
        "pubmed_query": '("Azelaic Acid"[Title/Abstract]) AND (acne OR rosacea OR melasma) AND (clinical OR randomized OR trial)'
    },
    "bakuchiol": {
        "inci": "Bakuchiol",
        "name_pt": "Bakuchiol (Retinol-Like Vegetal)",
        "category": "Anti-idade / Alternativa Vegana ao Retinol",
        "default_percent": 1.0,
        "min_percent": 0.5,
        "max_percent": 1.5,
        "safe_limit": 2.0,
        "phase": "C",
        "ph_range": (4.5, 6.5),
        "indication": ["anti-idade", "vegano", "pele_sensivel", "linhas_finas", "firmeza"],
        "mechanism": "Modulador da expressão gênica do colágeno tipo I, III e IV semelhante ao retinol sem ligar-se diretamente aos receptores de ácido retinoico, evitando irritação e fotossensibilidade.",
        "pubmed_query": '("Bakuchiol"[Title/Abstract]) AND (skin OR anti-aging OR wrinkles OR "clinical trial")'
    },
    "ascorbyl_glucoside": {
        "inci": "Ascorbyl Glucoside",
        "name_pt": "Ascorbil Glicosídeo (Vitamina C Estabilizada)",
        "category": "Antioxidante / Iluminador / Pró-colágeno",
        "default_percent": 2.0,
        "min_percent": 1.0,
        "max_percent": 3.0,
        "safe_limit": 5.0,
        "phase": "C",
        "ph_range": (5.5, 6.5),
        "indication": ["antioxidante", "iluminador", "anti-idade", "fotoenvelhecimento", "manchas"],
        "mechanism": "Derivado estável de vitamina C hidrossolúvel com liberação enzimática sustentada por alfa-glicosidase na epiderme; neutraliza radicais livres e inibe melanogênese.",
        "pubmed_query": '("Ascorbyl Glucoside"[Title/Abstract]) AND (skin OR antioxidant OR hyperpigmentation OR collagen) AND (clinical OR study)'
    },
    "panthenol": {
        "inci": "Panthenol (D-Panthenol)",
        "name_pt": "Pantenol (Pró-Vitamina B5)",
        "category": "Calmante / Umectante / Cicatrizante",
        "default_percent": 2.0,
        "min_percent": 0.5,
        "max_percent": 5.0,
        "safe_limit": 5.0,
        "phase": "C",
        "ph_range": (4.5, 7.0),
        "indication": ["hidratacao", "pele_sensivel", "barreira", "calmante", "pos_sol"],
        "mechanism": "Convertido em ácido pantotênico (componente essencial da Coenzima A), promovendo regeneração epitelial e reduzindo prurido e eritema.",
        "pubmed_query": '("Panthenol"[Title/Abstract] OR "Dexpanthenol"[Title/Abstract]) AND (skin OR barrier OR hydration OR wound) AND (clinical OR trial)'
    }
}

# Veículos e Estruturantes por Categoria de Produto
VEHICLE_CONFIGS = {
    "serum": {
        "name": "Sérum Aquoso de Alta Penetração",
        "target_ph": 5.5,
        "viscosity": "Fluido aquoso leve (~500 - 1.500 cPs)",
        "base_phase_a": [
            {"inci": "Aqua", "name": "Água Deionizada / Purificada", "function": "Veículo solvente universal", "phase": "A"},
            {"inci": "Disodium EDTA", "name": "EDTA Dissódico", "percent": 0.1, "function": "Agente quelante de íons metálicos", "phase": "A"},
            {"inci": "Glycerin", "name": "Glicerina Vegetal USP", "percent": 3.0, "function": "Umectante hidrofílico", "phase": "A"},
            {"inci": "Propanediol", "name": "Propanodiol (Zemea)", "percent": 4.0, "function": "Solvente carreador e promotor de permeação biológico", "phase": "A"}
        ],
        "base_phase_b": [
            {"inci": "Sclerotium Gum (and) Xanthan Gum", "name": "Goma Esclerótica e Xantana", "percent": 0.6, "function": "Modificador reológico e formador de gel suave", "phase": "B"}
        ],
        "base_phase_d": [
            {"inci": "Phenoxyethanol (and) Ethylhexylglycerin", "name": "Fenoxietanol e Etilhexilglicerina", "percent": 1.0, "function": "Sistema conservante de amplo espectro (livre de parabenos)", "phase": "D"},
            {"inci": "Sodium Hydroxide / Citric Acid (Sol. 10%)", "name": "Ajustador de pH q.s.p. pH 5.5", "percent": 0.2, "function": "Tampão corretor de pH fisiológico", "phase": "D"}
        ]
    },
    "gel_cream": {
        "name": "Gel-Creme Toque Seco / Oil-Free",
        "target_ph": 5.5,
        "viscosity": "Gel cremoso leve (~15.000 - 25.000 cPs)",
        "base_phase_a": [
            {"inci": "Aqua", "name": "Água Deionizada", "function": "Veículo principal", "phase": "A"},
            {"inci": "Disodium EDTA", "name": "EDTA Dissódico", "percent": 0.1, "function": "Quelante", "phase": "A"},
            {"inci": "Glycerin", "name": "Glicerina Vegetal", "percent": 3.0, "function": "Umectante", "phase": "A"},
            {"inci": "Sodium Polyacrylate (and) Dimethicone", "name": "Polímero Gelificante Autoemulsionante", "percent": 2.0, "function": "Espessante / Emulsionante a frio toque seco", "phase": "A"}
        ],
        "base_phase_b": [
            {"inci": "C12-15 Alkyl Benzoate", "name": "Benzoato de Alquila C12-15", "percent": 3.0, "function": "Emoliente leve toque seco", "phase": "B"},
            {"inci": "Caprylic/Capric Triglyceride", "name": "Triglicerídeos do Ácido Cáprico/Caprílico", "percent": 2.0, "function": "Emoliente biocompatível carreador", "phase": "B"},
            {"inci": "Silica", "name": "Sílica Esférica (Matificante)", "percent": 1.0, "function": "Modificador sensorial de toque aveludado e efeito mate", "phase": "B"}
        ],
        "base_phase_d": [
            {"inci": "Benzyl Alcohol (and) Glyceryl Caprylate (and) Glyceryl Undecylenate", "name": "Blend Conservante ECOCERT", "percent": 1.0, "function": "Sistema conservante natural", "phase": "D"},
            {"inci": "Citric Acid (Sol. 10%)", "name": "Ácido Cítrico q.s.p. pH 5.5", "percent": 0.15, "function": "Ajustador de pH", "phase": "D"}
        ]
    },
    "barrier_cream": {
        "name": "Emulsão Reparadora de Barreira Cutânea",
        "target_ph": 5.8,
        "viscosity": "Creme nutritivo aveludado (~35.000 - 50.000 cPs)",
        "base_phase_a": [
            {"inci": "Aqua", "name": "Água Deionizada", "function": "Veículo contínuo", "phase": "A"},
            {"inci": "Disodium EDTA", "name": "EDTA Dissódico", "percent": 0.1, "function": "Quelante estabilizante", "phase": "A"},
            {"inci": "Glycerin", "name": "Glicerina Vegetal USP", "percent": 4.0, "function": "Umectante fisiológico", "phase": "A"},
            {"inci": "Allantoin", "name": "Alantoína", "percent": 0.3, "function": "Anti-irritante e proliferador celular", "phase": "A"}
        ],
        "base_phase_b": [
            {"inci": "Cetearyl Alcohol (and) Cetearyl Glucoside", "name": "Emulsionante Não-Iônico Cristal Líquido (Montanov 68)", "percent": 4.0, "function": "Auto-emulsionante lamelar formador de cristais líquidos", "phase": "B"},
            {"inci": "Squalane (Olive/Sugar Cane Derived)", "name": "Esqualano Vegetal 100%", "percent": 4.0, "function": "Lipídio biomimético reparador do manto hidrolipídico", "phase": "B"},
            {"inci": "Butyrospermum Parkii (Shea) Butter", "name": "Manteiga de Karité", "percent": 2.5, "function": "Emoliente oclusivo suave rico em fitoesteróis", "phase": "B"},
            {"inci": "Tocopherol", "name": "Vitamina E Natural", "percent": 0.5, "function": "Antioxidante protetor da fase oleosa", "phase": "B"}
        ],
        "base_phase_d": [
            {"inci": "Phenoxyethanol (and) Ethylhexylglycerin", "name": "Conservante de Amplo Espectro", "percent": 0.9, "function": "Preservante antimicrobiano", "phase": "D"},
            {"inci": "Lactic Acid (Sol. 10%)", "name": "Ácido Lático q.s.p. pH 5.8", "percent": 0.1, "function": "Ajustador de pH biomimético", "phase": "D"}
        ]
    }
}
