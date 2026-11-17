"""
=============================================================================
Projeto: LogiGuard Analytics - Prevenção de Perdas na Cadeia Logística
Módulo: Pipeline de Ciência de Dados, Modelagem Preditiva & Análise Financeira
Autor: Portfólio de Dados / Inteligência Artificial
=============================================================================
"""

import sys
import os
import pandas as pd
import numpy as np

# Verificação opcional de bibliotecas
try:
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier, IsolationForest
    from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


def carregar_dados(caminho_csv: str) -> pd.DataFrame:
    """Carrega e valida o dataset de logística e ocorrências de perda."""
    if not os.path.exists(caminho_csv):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_csv}")
    
    df = pd.read_csv(caminho_csv)
    print(f"[+] Dataset carregado: {df.shape[0]} registros, {df.shape[1]} colunas.")
    return df


def preparar_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Feature Engineering com foco em regras de logística e prevenção de perdas:
    - Razão de atraso (tempo_real / tempo_previsto)
    - Densidade de paradas não programadas por hora de viagem
    - Indicador de desvio crítico (> 30 km da rota PGR)
    - Risco térmico severo (> 3°C de oscilação)
    """
    df = df.copy()
    
    # 1. Razão de Atraso
    df['razao_atraso'] = df['tempo_real_h'] / df['tempo_previsto_h'].replace(0, 1)
    
    # 2. Frequência de paradas por hora de percurso
    df['paradas_por_hora'] = df['paradas_nao_programadas'] / df['tempo_real_h'].replace(0, 1)
    
    # 3. Flags de risco operacional
    df['flag_desvio_critico'] = (df['desvio_rota_km'] > 25.0).astype(int)
    df['flag_quebra_termica'] = (df['variacao_temp_celsius'].abs() > 3.0).astype(int)
    
    # 4. Target binário de perda financeira efetiva
    df['houve_perda'] = (df['valor_perda_brl'] > 0).astype(int)
    
    return df


def executar_analise_negocio(df: pd.DataFrame) -> dict:
    """Calcula os principais KPIs operacionais e de negócio."""
    valor_total_transportado = df['valor_carga_brl'].sum()
    valor_total_perdas = df['valor_perda_brl'].sum()
    taxa_sinistralidade = (valor_total_perdas / valor_total_transportado) * 100
    
    perdas_por_categoria = df.groupby('categoria_carga')['valor_perda_brl'].agg(['sum', 'count']).sort_values('sum', ascending=False)
    perdas_por_tipo = df[df['tipo_sinistro'] != 'Nenhum']['tipo_sinistro'].value_counts()
    
    # Estimativa de perdas prevenidas pelo sistema de alerta
    perdas_prevenidas = df[df['status_acao'].str.contains('Prevenido|Recuperada', na=False)]['valor_carga_brl'].sum() * 0.45
    
    metricas = {
        'total_transportado_brl': valor_total_transportado,
        'total_perdas_brl': valor_total_perdas,
        'taxa_sinistralidade_pct': taxa_sinistralidade,
        'perdas_prevenidas_estimadas_brl': perdas_prevenidas,
        'ocorrencias_criticas': int((df['anomalia_detectada'] == 1).sum())
    }
    
    print("\n" + "="*50)
    print("📈 RESUMO EXECUTIVO DE INDICADORES (BUSINESS KPIs)")
    print("="*50)
    print(f"Total Cargas Monitoradas : R$ {valor_total_transportado:,.2f}")
    print(f"Prejuízo Total Bruto     : R$ {valor_total_perdas:,.2f}")
    print(f"Taxa de Sinistralidade   : {taxa_sinistralidade:.2f}%")
    print(f"Economia Estimada (IA)   : R$ {perdas_prevenidas:,.2f}")
    print(f"Anomalias Interceptadas  : {metricas['ocorrencias_criticas']}")
    print("="*50 + "\n")
    
    return metricas


def treinar_modelo_risco(df: pd.DataFrame):
    """
    Treina modelo Random Forest para prever probabilidade de sinistro
    e quantificar o impacto de cada feature na prevenção de perdas.
    """
    if not SKLEARN_AVAILABLE:
        print("[!] scikit-learn não instalado neste ambiente. Execute em seu ambiente com: pip install scikit-learn")
        return None
        
    features = [
        'valor_carga_brl', 'tempo_previsto_h', 'tempo_real_h',
        'desvio_rota_km', 'paradas_nao_programadas', 'variacao_temp_celsius',
        'razao_atraso', 'paradas_por_hora', 'flag_desvio_critico', 'flag_quebra_termica'
    ]
    
    X = df[features]
    y = df['anomalia_detectada']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    
    modelo = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
    modelo.fit(X_train, y_train)
    
    y_pred = modelo.predict(X_test)
    y_prob = modelo.predict_proba(X_test)[:, 1]
    
    auc = roc_auc_score(y_test, y_prob)
    print(f"\n[+] Desempenho do Modelo Preditivo:")
    print(f"    - ROC-AUC Score: {auc:.4f}")
    print("\nRelatório de Classificação:\n", classification_report(y_test, y_pred))
    
    importancias = pd.Series(modelo.feature_importances_, index=features).sort_values(ascending=False)
    print("Principais Fatores de Risco Identificados pela IA:")
    for feat, imp in importancias.head(5).items():
        print(f"  • {feat:<24}: {imp*100:.1f}%")
        
    return modelo


if __name__ == "__main__":
    caminho_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho_dados = os.path.join(caminho_base, "data", "ocorrencias_logistica_perdas.csv")
    
    print("Iniciando LogiGuard Analytics...")
    try:
        dados = carregar_dados(caminho_dados)
        dados_tratados = preparar_features(dados)
        kpis = executar_analise_negocio(dados_tratados)
        modelo = treinar_modelo_risco(dados_tratados)
    except Exception as e:
        print(f"[!] Erro na execução: {e}")
