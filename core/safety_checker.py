"""
Validador de Segurança, Limites Regulatórios (CIR/ANVISA/CosIng) e Incompatibilidades Farmacotécnicas
"""

from typing import List, Dict, Any, Tuple
from core.cosmetic_database import ACTIVE_INGREDIENTS

class SafetyChecker:
    """Verifica limites seguros de concentração e potenciais incompatibilidades físico-químicas"""

    @staticmethod
    def evaluate_formula(
        ingredients_list: List[Dict[str, Any]], 
        target_ph: float, 
        skin_type: str = "normal",
        vehicle: str = "serum"
    ) -> Dict[str, Any]:
        """
        Executa bateria completa de testes de segurança, compatibilidade e alertas técnicos.
        """
        warnings = []
        regulatory_checks = []
        synergies = []
        
        ingredient_keys = [item.get("key") for item in ingredients_list if item.get("key")]
        inci_names = [item.get("inci", "").lower() for item in ingredients_list]

        # 1. Checagem de Limites de Concentração Regulatórios
        for item in ingredients_list:
            key = item.get("key")
            percent = float(item.get("percent", 0.0))
            inci = item.get("inci", "")
            
            if key in ACTIVE_INGREDIENTS:
                meta = ACTIVE_INGREDIENTS[key]
                safe_limit = meta.get("safe_limit", 100.0)
                max_rec = meta.get("max_percent", safe_limit)
                
                if percent > safe_limit:
                    msg = f"Concentração de {inci} ({percent}%) ultrapassa o limite de segurança toxicológica CIR/CosIng ({safe_limit}%)."
                    warnings.append({"type": "REGULATORY_EXCEEDED", "severity": "HIGH", "message": msg})
                    regulatory_checks.append({"ingredient": inci, "status": "REPROVADO", "limit": f"Máx {safe_limit}%", "current": f"{percent}%"})
                elif percent > max_rec:
                    msg = f"Concentração de {inci} ({percent}%) está acima da faixa cosmética usual recomendada ({max_rec}%)."
                    warnings.append({"type": "CONCENTRATION_HIGH", "severity": "MEDIUM", "message": msg})
                    regulatory_checks.append({"ingredient": inci, "status": "ALERTA", "limit": f"Sugerido {max_rec}%", "current": f"{percent}%"})
                else:
                    regulatory_checks.append({"ingredient": inci, "status": "CONFORME", "limit": f"Até {safe_limit}%", "current": f"{percent}%"})

        # 2. Incompatibilidades Físico-Químicas e Dermatológicas
        # a) Niacinamida + pH muito ácido (< 4.5)
        if any("niacinamide" in k for k in ingredient_keys) and target_ph < 4.5:
            warnings.append({
                "type": "PH_HYDROLYSIS_RISK",
                "severity": "HIGH",
                "message": f"pH alvo de {target_ph} é excessivamente ácido para Niacinamida. Risco de hidrólise lenta em ácido nicotínico, podendo causar rubor facial transitório (flushing) e irritação."
            })

        # b) Ácido Salicílico / BHA em veículo exclusivamente aquoso sem solubilizante
        if any("salicylic_acid" in k for k in ingredient_keys):
            has_solvent = any("propanediol" in name or "alcohol" in name or "polysorbate" in name for name in inci_names)
            if not has_solvent and vehicle == "serum":
                warnings.append({
                    "type": "SOLUBILITY_WARNING",
                    "severity": "MEDIUM",
                    "message": "Ácido Salicílico possui baixa solubilidade em água pura. Certifique-se de manter co-solventes (Propanediol, Butilenoglicol) ou solubilizantes adequados para evitar cristalização/precipitação."
                })

        # c) Retinol + Pele Extremamente Sensível
        if any("retinol" in k for k in ingredient_keys) and ("sensivel" in skin_type.lower() or "rosacea" in skin_type.lower()):
            warnings.append({
                "type": "SKIN_TOLERANCE",
                "severity": "MEDIUM",
                "message": "Retinol em pele sensível/rosácea exige introdução gradual ou preferência por derivados encapsulados / Bakuchiol vegetal associado a agentes calmantes (Pantenol/Centella)."
            })

        # 3. Mapeamento de Sinergias Positivas Comprovadas
        if "tranexamic_acid" in ingredient_keys and "niacinamide" in ingredient_keys:
            synergies.append({
                "pair": "Ácido Tranexâmico + Niacinamida",
                "benefit": "Sinergia padrão-ouro em melasma: Bloqueio duplo da cascata melanogênica (redução de síntese pela via plasminogênio + bloqueio de transferência de melanossomas)."
            })

        if "ceramide_complex" in ingredient_keys and "hyaluronic_acid_multi" in ingredient_keys:
            synergies.append({
                "pair": "Complexo de Ceramidas + Ácido Hialurônico Multimolecular",
                "benefit": "Restauração bimodal da barreira: Retenção hídrica higroscópica em profundidade + vedação lipídica lamelar no estrato córneo."
            })

        if "centella_asiatica_extract" in ingredient_keys and "panthenol" in ingredient_keys:
            synergies.append({
                "pair": "Centella Asiática + D-Pantenol",
                "benefit": "Potencialização anti-inflamatória e pró-cicatrizante, acelerando a reepitelização e neutralizando eritema."
            })

        # 4. Avaliação do pH Fisiológico
        ph_status = "ADEQUADO"
        if target_ph < 4.0:
            ph_status = "ÁCIDO (Atenção à barreira cutânea diária)"
        elif target_ph > 6.5:
            ph_status = "ELEVADO (Pode desestabilizar o manto ácido da pele)"

        is_safe = all(w["severity"] != "HIGH" for w in warnings)

        return {
            "is_safe": is_safe,
            "target_ph": target_ph,
            "ph_status": ph_status,
            "warnings": warnings,
            "regulatory_checks": regulatory_checks,
            "synergies": synergies
        }
