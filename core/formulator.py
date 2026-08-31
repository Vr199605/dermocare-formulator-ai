"""
Motor de Formulação Dermocosmética e Integração com Inteligência Artificial & Ciência
"""

import os
import json
from typing import Dict, List, Any, Optional
from core.cosmetic_database import ACTIVE_INGREDIENTS, VEHICLE_CONFIGS
from core.pubmed_service import PubMedService
from core.safety_checker import SafetyChecker

class DermocareFormulator:
    """Motor central de geração e validação de fórmulas dermocosméticas"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.pubmed = PubMedService()

    def generate_formulation(
        self,
        product_title: str,
        target_claims: List[str],
        skin_type: str,
        vehicle_type: str = "serum",
        exclusions: Optional[List[str]] = None,
        custom_instructions: str = "",
        custom_actives_selection: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Gera uma formulação dermocosmética completa e balanceada a 100% p/p
        com evidências científicas do PubMed e verificação de segurança.
        """
        exclusions = exclusions or []
        
        # 1. Selecionar Veículo Base
        vehicle_key = vehicle_type if vehicle_type in VEHICLE_CONFIGS else "serum"
        v_config = VEHICLE_CONFIGS[vehicle_key]
        target_ph = v_config["target_ph"]
        
        # 2. Selecionar Ativos Adequados
        selected_actives_keys = []
        if custom_actives_selection:
            selected_actives_keys = [k for k in custom_actives_selection if k in ACTIVE_INGREDIENTS]
        else:
            # Algoritmo de afinidade baseado nas alegações e tipo de pele
            claims_text = " ".join(target_claims).lower() + " " + skin_type.lower() + " " + custom_instructions.lower()
            
            # Pontuar cada ativo
            scores = {}
            for key, data in ACTIVE_INGREDIENTS.items():
                score = 0
                for ind in data["indication"]:
                    if ind in claims_text:
                        score += 2
                # Ajustes específicos
                if "sensivel" in skin_type.lower() and key in ["centella_asiatica_extract", "panthenol", "ceramide_complex"]:
                    score += 3
                if "melasma" in claims_text and key in ["tranexamic_acid", "niacinamide", "alpha_arbutin"]:
                    score += 4
                if "acne" in claims_text and key in ["salicylic_acid", "niacinamide", "azelaic_acid"]:
                    score += 4
                if "anti-idade" in claims_text and key in ["retinol_encapsulated", "bakuchiol", "hyaluronic_acid_multi"]:
                    score += 4
                scores[key] = score
            
            # Ordenar por maior pontuação e escolher os 2 a 4 melhores
            sorted_keys = sorted(scores.keys(), key=lambda k: scores[k], reverse=True)
            selected_actives_keys = [k for k in sorted_keys if scores[k] > 0][:4]
            
            # Fallback se nada foi selecionado
            if not selected_actives_keys:
                selected_actives_keys = ["niacinamide", "hyaluronic_acid_multi"]

        # 3. Montar Composição da Fórmula por Fases
        phase_a = []
        phase_b = []
        phase_c = []
        phase_d = []

        # Copiar base do veículo
        for item in v_config["base_phase_a"]:
            phase_a.append(dict(item))
        for item in v_config["base_phase_b"]:
            phase_b.append(dict(item))
        for item in v_config["base_phase_d"]:
            phase_d.append(dict(item))

        # Adicionar Ativos na Fase C
        scientific_evidence = []
        for key in selected_actives_keys:
            act = ACTIVE_INGREDIENTS[key]
            percent = act["default_percent"]
            
            # Ajuste de dose se for para pele sensível
            if "sensivel" in skin_type.lower() and key == "salicylic_acid":
                percent = 1.0
            
            phase_c.append({
                "key": key,
                "inci": act["inci"],
                "name": act["name_pt"],
                "percent": percent,
                "function": f"Ativo cosmético ({act['category']})",
                "phase": "C",
                "mechanism": act["mechanism"]
            })

            # Buscar Evidência Científica no PubMed
            evidence = self.pubmed.get_evidence_for_ingredient(key, act.get("pubmed_query", ""))
            scientific_evidence.append({
                "active_name": act["name_pt"],
                "inci": act["inci"],
                "mechanism": act["mechanism"],
                "studies": evidence
            })

        # 4. Ajuste Estequiométrico para fechar rigorosamente em 100.00% p/p
        # Somar todas as porcentagens fixas
        total_non_water = 0.0
        
        all_items = phase_a + phase_b + phase_c + phase_d
        for item in all_items:
            if item.get("inci") != "Aqua" and "percent" in item:
                total_non_water += float(item["percent"])

        water_percent = round(100.00 - total_non_water, 2)
        if water_percent < 20.0:
            water_percent = 20.0  # Proteção de segurança

        # Atualizar a água na Fase A
        for item in phase_a:
            if item.get("inci") == "Aqua":
                item["percent"] = water_percent

        # 5. Lista consolidada para checagem de segurança
        consolidated_ingredients = []
        for p in [phase_a, phase_b, phase_c, phase_d]:
            for item in p:
                consolidated_ingredients.append(item)

        safety_eval = SafetyChecker.evaluate_formula(
            consolidated_ingredients, 
            target_ph=target_ph, 
            skin_type=skin_type,
            vehicle=vehicle_key
        )

        # 6. Procedimento de Manipulação Padronizado
        manufacturing_steps = self._generate_manufacturing_steps(vehicle_key, target_ph)

        # 7. Construir Dossiê Final
        result = {
            "product_title": product_title or f"Dermocosmético Personalizado ({v_config['name']})",
            "vehicle_name": v_config["name"],
            "vehicle_key": vehicle_key,
            "skin_type": skin_type,
            "target_claims": target_claims,
            "target_ph": target_ph,
            "viscosity": v_config["viscosity"],
            "total_percent": sum(item["percent"] for item in consolidated_ingredients if "percent" in item),
            "phases": {
                "Phase A (Aquosa / Umectantes / Quelantes)": phase_a,
                "Phase B (Polímeros / Lipídica / Emulsionantes)": phase_b,
                "Phase C (Ativos Termossensíveis & Biológicos)": phase_c,
                "Phase D (Conservantes & Ajuste de pH)": phase_d
            },
            "raw_ingredients_list": consolidated_ingredients,
            "safety_evaluation": safety_eval,
            "scientific_evidence": scientific_evidence,
            "manufacturing_steps": manufacturing_steps,
            "stability_protocol": self._generate_stability_protocol()
        }

        return result

    def _generate_manufacturing_steps(self, vehicle_key: str, target_ph: float) -> List[str]:
        """Gera o passo a passo galênico para laboratório de manipulação / P&D"""
        if vehicle_key == "serum":
            return [
                "1. Sanitize e pese rigorosamente todos os componentes em balança analítica calibrada.",
                "2. FASE A: Em béquer principal, adicionar a Água Deionizada. Sob agitação mecânica (300-500 RPM), dissolver o EDTA Dissódico, Glicerina e Propanediol até completa homogeneização translúcida.",
                "3. FASE B: Polvilhar a Goma Esclerótica / Xantana lentamente sobre a Fase A sob agitação vigorosa (800-1200 RPM) por 15-20 minutos até hidratação total do polímero e formação de gel uniforme livre de grumos.",
                "4. FASE C: Adicionar os ativos um a um em temperatura ambiente (< 40°C), aguardando a completa dissolução/dispersão de cada um antes do próximo.",
                "5. FASE D: Incorporar o sistema conservante (Fenoxietanol / Etilhexilglicerina) e homogeneizar por 5 minutos.",
                f"6. CONTROLE DE PROCESSO: Aferir o pH em potenciômetro calibrado a 25°C. Ajustar para pH {target_ph} com solução de Ácido Cítrico ou NaOH 10% q.s.p.",
                "7. Embalar em frasco âmbar com gotejador ou pump airless para proteção contra fotodegradação."
            ]
        elif vehicle_key == "barrier_cream":
            return [
                "1. FASE A: Aquecer a água deionizada, EDTA, glicerina e alantoína a 75°C - 80°C sob agitação constante.",
                "2. FASE B: Em béquer separado, fundir o emulsionante Montanov 68, esqualano, manteiga de karité e tocoferol a 75°C - 80°C até fusão límpida total.",
                "3. EMULSIFICAÇÃO: Verter lentamente a Fase B na Fase A sob alta homogeneização (Ultra-Turrax / rotor-estator a 3000-4000 RPM) por 5 minutos para formar a estrutura lamelar.",
                "4. RESFRIAMENTO: Reduzir a agitação para pá lenta tipo âncora (100 RPM) e resfriar até 40°C.",
                "5. FASE C & D: Abaixo de 40°C, incorporar o Complexo de Ceramidas, demais ativos termossensíveis e o sistema conservante.",
                f"6. AJUSTE: Checar pH final ({target_ph}) e viscosidade. Embalar em bisnaga ou pote protegido."
            ]
        else:
            return [
                "1. Pesar os insumos e preparar a Fase A com água e polímero autoemulsionante a frio sob agitação rápida.",
                "2. Adicionar os emolientes da Fase B gota a gota sobre a Fase A até espessamento e formação de gel cremoso suave.",
                "3. Incorporar os ativos cosméticos da Fase C abaixo de 35°C garantindo homogeneidade perfeita.",
                f"4. Adicionar conservante da Fase D e ajustar o pH com ácido cítrico para {target_ph}.",
                "5. Avaliar aspecto, homogeneidade e estabilidade centrífuga inicial (3000 RPM por 30 min)."
            ]

    def _generate_stability_protocol(self) -> Dict[str, Any]:
        """Protocolo acelerado de estabilidade conforme Guia de Estabilidade da ANVISA"""
        return {
            "estabilidade_preliminar": "Centrifugação a 3000 RPM por 30 minutos a 25°C e ciclos de Gelo-Degelo (-5°C a 40°C por 12 dias).",
            "estabilidade_acelerada": "Estufa a 45°C ± 2°C (UR 75%) por 90 dias com coletas em T0, T15, T30, T60 e T90 para avaliação de pH, viscosidade, cor, odor e contagem microbiológica.",
            "especificacoes_controle": {
                "aspecto": "Límpido a levemente translúcido / Emulsão homogênea",
                "odor": "Característico das matérias-primas, isento de rancificação",
                "limite_microbiologico": "Contagem total de microrganismos mesófilos < 100 UFC/g; Ausência de P. aeruginosa, S. aureus, E. coli e C. albicans."
            }
        }
