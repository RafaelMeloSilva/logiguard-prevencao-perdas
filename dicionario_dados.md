# Dicionário de Dados & Regras de Negócio - LogiGuard Analytics

## 🎯 Contexto do Projeto
O **LogiGuard Analytics** é um projeto de Ciência de Dados e Inteligência de Negócios voltado para a **Prevenção de Perdas na Cadeia Logística e Distribuição**. O objetivo central é identificar padrões anômalos em tempo real (telemetria, rotas, temperaturas e paradas) para evitar furtos de carga, quebra da cadeia fria e avarias operacionais antes que o dano financeiro se consolide.

---

## 📊 Estrutura do Dataset (`data/ocorrencias_logistica_perdas.csv`)

| Coluna | Tipo | Descrição | Exemplo |
| :--- | :--- | :--- | :--- |
| `id_remessa` | String | Identificador exclusivo do manifesto de transporte / frete. | `REM-2026-0142` |
| `data_envio` | Date (YYYY-MM-DD) | Data de expedição do Centro de Distribuição. | `2026-04-12` |
| `origem_cd` | String | CD de origem da expedição. | `CD Cajamar - SP` |
| `destino` | String | Cidade/Estado de destino final da mercadoria. | `Belo Horizonte - MG` |
| `transportadora` | String | Parceiro logístico ou frota responsável pela viagem. | `TransLog Express` |
| `categoria_carga` | String | Tipo da mercadoria transportada e seu perfil de risco. | `Eletrônicos & Smart` |
| `valor_carga_brl` | Float (R$) | Valor fiscal total da nota da mercadoria transportada. | `185000.00` |
| `tempo_previsto_h` | Integer | Tempo SLA estimado em horas de viagem até a entrega. | `14` |
| `tempo_real_h` | Integer | Tempo efetivo total de percurso registrado por telemetria. | `22` |
| `desvio_rota_km` | Float (km) | Desvio acumulado em relação à rota autorizada pelo PGR. | `42.5` |
| `paradas_nao_programadas` | Integer | Contagem de paradas fora de pontos de apoio homologados. | `3` |
| `variacao_temp_celsius` | Float (°C) | Desvio máximo de temperatura em relação à faixa ideal. | `7.4` |
| `tipo_sinistro` | String | Diagnóstico ou classificação da ocorrência registrada. | `Quebra da Cadeia de Frio` |
| `valor_perda_brl` | Float (R$) | Prejuízo financeiro direto apurado na viagem. | `45200.00` |
| `score_risco_ml` | Float (0 a 1) | Probabilidade estimada pelo modelo preditivo de perda/sinistro. | `0.892` |
| `anomalia_detectada` | Binary (0 ou 1) | Flag indicativa de anomalia capturada pela IA. | `1` |
| `status_acao` | String | Resolução operacional executada pela torre de controle. | `Prevenido via Alerta IoT` |

---

## 💡 Indicadores-Chave de Desempenho (KPIs)
1. **Taxa de Sinistralidade Financeira (%)**: `(Total Perdas em R$) / (Total Transportado em R$) * 100`
2. **Índice de Prevenção Ativa (%)**: Percentual de ocorrências anômalas interceptadas a tempo de mitigar perdas.
3. **Loss Reduction ROI**: `(Perdas Evitadas pelo Alerta - Custo Operacional da Solução) / Custo Operacional`
4. **Precisão da Torre de Controle**: Taxa de falsos positivos na detecção de desvios suspeitos.
