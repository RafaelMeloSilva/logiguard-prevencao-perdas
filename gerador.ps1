$origens = @("CD Cajamar - SP", "CD Extrema - MG", "CD Duque de Caxias - RJ", "CD Curitiba - PR", "CD Louveira - SP")
$destinos = @("São Paulo Capital - SP", "Belo Horizonte - MG", "Rio de Janeiro - RJ", "Curitiba - PR", "Salvador - BA", "Recife - PE", "Porto Alegre - RS", "Goiânia - GO")
$transportadoras = @("TransLog Express", "Rodocargo Brasil", "Rápido Sudeste", "ViaCarga Log", "Expresso Nacional", "Frota Própria")
$categorias = @(
    @{ Nome="Eletrônicos & Smart"; TicketMin=80000; TicketMax=350000; RiscoRoubo=0.25; SensivelTemp=$false },
    @{ Nome="Farmacêuticos & Vacinas"; TicketMin=50000; TicketMax=280000; RiscoRoubo=0.10; SensivelTemp=$true },
    @{ Nome="Alimentos Congelados"; TicketMin=25000; TicketMax=95000; RiscoRoubo=0.03; SensivelTemp=$true },
    @{ Nome="Cosméticos & Perfumaria"; TicketMin=40000; TicketMax=180000; RiscoRoubo=0.15; SensivelTemp=$false },
    @{ Nome="Eletrodomésticos"; TicketMin=30000; TicketMax=120000; RiscoRoubo=0.08; SensivelTemp=$false },
    @{ Nome="Bebidas Premium"; TicketMin=20000; TicketMax=85000; RiscoRoubo=0.12; SensivelTemp=$false }
)

$linhas = @("id_remessa,data_envio,origem_cd,destino,transportadora,categoria_carga,valor_carga_brl,tempo_previsto_h,tempo_real_h,desvio_rota_km,paradas_nao_programadas,variacao_temp_celsius,tipo_sinistro,valor_perda_brl,score_risco_ml,anomalia_detectada,status_acao")

$rnd = New-Object System.Random(42)
$dataBase = [DateTime]::Parse("2026-01-01")

for ($i = 1; $i -le 650; $i++) {
    $id = "REM-2026-$("{0:D4}" -f $i)"
    $dias = $rnd.Next(0, 310)
    $dataEnvio = $dataBase.AddDays($dias).ToString("yyyy-MM-dd")
    $origem = $origens[$rnd.Next($origens.Length)]
    $destino = $destinos[$rnd.Next($destinos.Length)]
    $transp = $transportadoras[$rnd.Next($transportadoras.Length)]
    $cat = $categorias[$rnd.Next($categorias.Length)]
    
    $valorCarga = [Math]::Round($rnd.NextDouble() * ($cat.TicketMax - $cat.TicketMin) + $cat.TicketMin, 2)
    $tempoPrev = $rnd.Next(6, 48)
    
    # Anomalia simulada
    $probAnomalia = $rnd.NextDouble()
    $temAnomalia = $probAnomalia -gt 0.82
    
    $desvio = 0.0
    $paradas = 0
    $tempoReal = $tempoPrev + $rnd.Next(-1, 3)
    if ($tempoReal -lt 4) { $tempoReal = 4 }
    $tempVar = [Math]::Round(($rnd.NextDouble() * 1.8) - 0.9, 1)
    
    $tipoSinistro = "Nenhum"
    $valorPerda = 0.0
    $scoreRisco = [Math]::Round($rnd.NextDouble() * 0.35, 3)
    $anomaliaML = 0
    $statusAcao = "Concluído sem Intercorrências"
    
    if ($temAnomalia) {
        $anomaliaML = 1
        $scoreRisco = [Math]::Round(0.65 + ($rnd.NextDouble() * 0.34), 3)
        $paradas = $rnd.Next(2, 6)
        $desvio = [Math]::Round($rnd.NextDouble() * 45.0 + 5.0, 1)
        $tempoReal = $tempoPrev + $rnd.Next(5, 26)
        
        # Tipo de anomalia
        if ($cat.SensivelTemp -and ($rnd.NextDouble() -gt 0.4)) {
            $tempVar = [Math]::Round($rnd.NextDouble() * 12.0 + 4.0, 1)
            $tipoSinistro = "Quebra da Cadeia de Frio"
            $valorPerda = [Math]::Round($valorCarga * ($rnd.NextDouble() * 0.6 + 0.3), 2)
            $statusAcao = if ($rnd.NextDouble() -gt 0.55) { "Prevenido via Alerta IoT" } else { "Perda Confirmada" }
        } elseif ($cat.RiscoRoubo -gt 0.12 -and ($rnd.NextDouble() -lt 0.5)) {
            $desvio = [Math]::Round($rnd.NextDouble() * 80.0 + 25.0, 1)
            $tipoSinistro = "Desvio de Rota Suspeito / Tentativa de Furto"
            $valorPerda = if ($rnd.NextDouble() -gt 0.6) { [Math]::Round($valorCarga * 0.9, 2) } else { 0.0 }
            $statusAcao = if ($valorPerda -eq 0.0) { "Carga Recuperada por Bloqueio Remoto" } else { "Perda Confirmada" }
        } else {
            $tipoSinistro = "Avaria Mecânica / Tombamento Parcial"
            $valorPerda = [Math]::Round($valorCarga * ($rnd.NextDouble() * 0.3 + 0.05), 2)
            $statusAcao = "Acionado Seguro / Reabastecimento Imediato"
        }
    }
    
    $linhas += "$id,$dataEnvio,$origem,$destino,$transp,$($cat.Nome),$valorCarga,$tempoPrev,$tempoReal,$desvio,$paradas,$tempVar,$tipoSinistro,$valorPerda,$scoreRisco,$anomaliaML,$statusAcao"
}

$caminhoCsv = "C:\Users\rafae\.gemini\antigravity\scratch\logiguard-prevencao-perdas\data\ocorrencias_logistica_perdas.csv"
$linhas | Set-Content -Path $caminhoCsv -Encoding UTF8
Write-Output "Dataset gerado com sucesso: $($linhas.Length) linhas."
