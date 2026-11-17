# 🛡️ LogiGuard Analytics: Prevenção Inteligente de Perdas na Logística

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange?logo=scikit-learn)](https://scikit-learn.org/)
[![Analytics](https://img.shields.io/badge/Business%20Intelligence-Executive%20Dashboard-green)](dashboard/index.html)
[![Domain](https://img.shields.io/badge/Domain-Logistics%20%26%20Supply%20Chain-purple)]()
[![Status](https://img.shields.io/badge/Status-Complete-success)]()

> **Estudo de Caso Prático & Projeto de Portfólio**: Sistema preditivo de inteligência artificial e torre de controle analítica para detecção de anomalias em telemetria, mitigação de roubos de carga, quebras na cadeia fria e avarias no transporte.

---

## 📌 1. Visão Geral do Problema de Negócio
No setor de transporte e cadeia de suprimentos, os sinistros e avarias representam uma sangria financeira silenciosa e expressiva:
- **Tentativas de furto e desvios de rota** representam mais de 40% das perdas totais em cargas de alto valor agregado (eletrônicos e cosméticos).
- **Quebras térmicas na cadeia fria** causam perda total imediata de lotes de alimentos congelados e medicamentos termolábeis.
- **Falta de visibilidade preditiva**: torres de controle convencionais operam de forma puramente reativa, emitindo avisos quando a mercadoria já foi violada ou deteriorada.

### O Desafio
Transformar telemetria contínua (GPS, paradas, tempos de trânsito e sensores de temperatura) em **ações preventivas imediatas**, antes que a anomalia se converta em perda financeira irreversível.

---

## 🏗️ 2. Arquitetura da Solução

```
[Sensores IoT & Telemetria] ➔ GPS / Odômetro / Temperatura / Paradas
           │
           ▼
[Pipeline de Dados & Feature Engineering] ➔ Razão de Atraso, Desvio PGR, Delta Térmico
           │
           ▼
[Camada Preditiva de IA] ➔ Random Forest Classifier + Isolation Forest (Detecção de Anomalias)
           │
           ▼
[Torre de Controle & Dashboard] ➔ Alertas em Tempo Real, Classificação de Risco & Simulador de ROI
```

---

## 📊 3. Destaques de Performance do Modelo
- **Área sob a Curva ROC (AUC-ROC)**: `0.942`
- **F1-Score Geral**: `0.89`
- **Recall em Cargas Críticas de Alto Risco**: `92.0%`
- **Principais Preditores de Risco**:
  1. Desvio quilométrico da rota homologada no PGR (peso: 34%)
  2. Oscilação térmica cumulativa em relação ao setpoint (peso: 27%)
  3. Frequência de paradas em pontos não autorizados (peso: 21%)

---

## 💰 4. Impacto Financeiro Simulado
| Métrica Operacional | Antes da Solução | Com LogiGuard Analytics | Variação (%) |
| :--- | :--- | :--- | :--- |
| **Volume de Cargas Monitoradas** | R$ 57,84 Milhões | R$ 57,84 Milhões | - |
| **Sinistralidade Anual Bruta** | R$ 3,12 Milhões (5.39%) | R$ 1,28 Milhão (2.21%) | **-34% na taxa de perdas** |
| **Valor Total em Cargas Salvas** | R$ 0,00 | R$ 1,84 Milhão | **+R$ 1.84M preservados** |
| **Retorno sobre Investimento (ROI)** | N/A | > 300% ao ano | **Payback em < 4 meses** |

---

## 💻 5. Estrutura do Repositório

```text
logiguard-prevencao-perdas/
├── data/
│   ├── ocorrencias_logistica_perdas.csv   # Dataset sintético com 650 viagens monitoradas
│   ├── dicionario_dados.md                # Dicionário de variáveis e regras de negócio
│   └── gerador.ps1                        # Script gerador do dataset com distribuições estocásticas
├── scripts/
│   └── analise_e_modelo.py                # Pipeline Python completo (EDA, features, IA, ROI)
├── dashboard/
│   └── index.html                         # Dashboard executivo interativo (HTML5, Tailwind, Chart.js)
├── linkedin_kit/
│   ├── 01_post_linkedin.md                # 3 opções de posts magnéticos para o LinkedIn
│   ├── 02_roteiro_carrossel.md            # Roteiro slide a slide para Carrossel em PDF
│   └── 03_perfil_linkedin_otimizacao.md   # Textos para otimizar Título, Sobre, Destaques e Skills
└── README.md                              # Documentação oficial do projeto
```

---

## 🚀 6. Como Executar o Projeto Localmente

### Abrir o Dashboard Executivo Interativo
Basta abrir o arquivo `dashboard/index.html` em qualquer navegador (Google Chrome, Microsoft Edge, Firefox). Ele não requer instalação de servidor ou banco de dados!

### Executar a Análise e Modelagem em Python
```bash
# 1. Instalar dependências básicas
pip install pandas numpy scikit-learn

# 2. Executar o pipeline analítico
python scripts/analise_e_modelo.py
```

---

## 👨‍💻 Autor & Conexões
- **Desenvolvido por**: Rafael de Melo da Silva
- **LinkedIn**: www.linkedin.com/in/rafael-melo-4533a9171
- **Portfólio / GitHub**: https://github.com/RafaelMeloSilva
