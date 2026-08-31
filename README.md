# 🧪 Dermocare Formulator AI
**Agente Inteligente de Formulação Dermocosmética com Grounding Científico (PubMed)**

Aplicação que une inteligência artificial farmacotécnica e busca científica em tempo real no **PubMed / NCBI Entrez** e **Europe PMC** para gerar formulações cosméticas balanceadas a 100% p/p com comprovação clínica.

---

## 🌐 Como Subir no GitHub e Publicar no Vercel

### Passo 1: Inicializar o Repositório Git Localmente
No terminal (PowerShell), entre na pasta do projeto e faça o primeiro commit:

```bash
cd "C:\Users\user\.gemini\antigravity\scratch\dermocare_formulator"
git init
git add .
git commit -m "Initial commit - Dermocare Formulator AI"
```

### Passo 2: Criar Repositório no GitHub e Fazer o Push
1. Crie um novo repositório vazio no seu [GitHub](https://github.com/new) com o nome `dermocare-formulator-ai`.
2. Conecte e envie os arquivos:

```bash
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/dermocare-formulator-ai.git
git push -u origin main
```

---

## 🚀 Publicar no Vercel (Gratuito em 1 Minuto)

1. Acesse o painel do [Vercel](https://vercel.com/) e faça login com sua conta do GitHub.
2. Clique em **"Add New..."** → **"Project"**.
3. Selecione o repositório `dermocare-formulator-ai` e clique em **"Import"**.
4. Não precisa alterar nenhuma configuração de Build! O arquivo [`vercel.json`](vercel.json) e o [`index.html`](index.html) já estão 100% prontos.
5. Clique em **"Deploy"**.

Seu projeto estará no ar com link público HTTPS (ex: `https://dermocare-formulator.vercel.app`)!

---

## 💻 Como Rodar Localmente (Streamlit)

Caso queira rodar a versão em Python Streamlit no seu computador:

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```
