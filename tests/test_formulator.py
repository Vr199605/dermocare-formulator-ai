"""
Testes Automatizados do Dermocare Formulator AI
"""

import unittest
from core.formulator import DermocareFormulator
from core.pubmed_service import PubMedService
from core.safety_checker import SafetyChecker
from core.pdf_exporter import PDFExporter

class TestDermocareFormulator(unittest.TestCase):

    def setUp(self):
        self.formulator = DermocareFormulator()

    def test_formulation_balance_sums_to_100(self):
        """Testa se a soma percentual da fórmula fecha rigorosamente em 100%"""
        dossier = self.formulator.generate_formulation(
            product_title="Sérum Teste Melasma",
            target_claims=["Clareamento de Melasma / Manchas"],
            skin_type="Pele Sensível e com Rosácea",
            vehicle_type="serum"
        )
        self.assertAlmostEqual(dossier["total_percent"], 100.00, places=2)
        self.assertTrue(len(dossier["scientific_evidence"]) > 0)
        self.assertTrue(len(dossier["phases"]) == 4)

    def test_pubmed_service_retrieves_evidence(self):
        """Testa se o serviço do PubMed recupera estudos com PMIDs para Tranexamic Acid"""
        pubmed = PubMedService()
        evidence = pubmed.get_evidence_for_ingredient("tranexamic_acid", '("Tranexamic Acid"[Title/Abstract]) AND (melasma)')
        self.assertTrue(len(evidence) > 0)
        self.assertTrue(any("pmid" in item for item in evidence))

    def test_safety_checker_warns_on_high_ph_or_incompatibilities(self):
        """Testa se o validador detecta pH excessivamente ácido para Niacinamida"""
        fake_ingredients = [
            {"key": "niacinamide", "inci": "Niacinamide", "percent": 4.0},
            {"key": "salicylic_acid", "inci": "Salicylic Acid", "percent": 2.0}
        ]
        eval_res = SafetyChecker.evaluate_formula(fake_ingredients, target_ph=3.5, skin_type="sensivel")
        # Deve alertar sobre hidrólise de niacinamida em pH < 4.5
        warning_types = [w["type"] for w in eval_res["warnings"]]
        self.assertIn("PH_HYDROLYSIS_RISK", warning_types)

    def test_pdf_generation(self):
        """Testa se a exportação em PDF gera bytes válidos de PDF"""
        dossier = self.formulator.generate_formulation(
            product_title="Sérum Teste PDF",
            target_claims=["Anti-idade / Firmeza e Rugas"],
            skin_type="Pele Madura / Fotoenvelhecida",
            vehicle_type="serum"
        )
        pdf_bytes = PDFExporter.generate_dossier_pdf(dossier)
        self.assertTrue(len(pdf_bytes) > 1000)
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))

if __name__ == "__main__":
    unittest.main()
