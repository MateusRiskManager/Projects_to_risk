# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 13:45:01 2022

https://github.com/eudesrodrigo/brFinance

@author: mafeitosa
"""

import pandas as pd
from brfinance import CVMAsyncBackend
from datetime import datetime, date

cvm_httpclient = CVMAsyncBackend()

# Dict de códigos CVM para todas as empresas
cvm_codes = cvm_httpclient.get_cvm_codes()

# Dict de todas as categorias de busca disponíveis (Fato relevante, DFP, ITR, etc.)
categories = cvm_httpclient.get_consulta_externa_cvm_categories()

print('Buscando BancoInter')

start_date = date(2010, 1, 1)
end_dt = date(2022, 1, 1)
cvm_codes_string = "024406" #BancoInter
report_type = ["EST_4", "EST_3", "IPE_4_-1_-1"] # Códigos de categoria para DFP, ITR e fatos relevantes
report_type = ",".join(report_type) # Busca de DFP, ITR e fatos relevantes, separados por ","
last_ref_date = True # Se "True" retorna apenas o último report no intervalo de datas
reports_list = [
    'Balanço Patrimonial Ativo',
    'Balanço Patrimonial Passivo',
    'Demonstração do Resultado',
    'Demonstração do Resultado Abrangente',
    'Demonstração do Fluxo de Caixa',
    'Demonstração das Mutações do Patrimônio Líquido',
    'Demonstração de Valor Adicionado'] # Se None retorna todos os demonstrativos disponíveis.

# "get_consulta_externa_cvm_results" retorna um dataframe com os dados da busca
search_result = cvm_httpclient.get_consulta_externa_cvm_results(
    cod_cvm=cvm_codes_string,
    start_date=start_date,
    end_date=end_dt,
    last_ref_date=last_ref_date,
    report_type=report_type)

print('Obter demonstrativos')

# Obter demonstrativos

# Filtro search_result para ITR e DFP apenas
search_result = search_result[
    (search_result['categoria']=="DFP - Demonstrações Financeiras Padronizadas") |
    (search_result['categoria']=="ITR - Informações Trimestrais")]

search_result = search_result[pd.to_numeric(search_result['numero_seq_documento'], errors='coerce').notnull()]

for index, row in search_result.iterrows():
    empresa = f"{row['cod_cvm']} - {cvm_codes[row['cod_cvm']]} - {row['numero_seq_documento']} - {row['codigo_tipo_instituicao']}"
    print("*" * 20, empresa, "*" * 20)
    
    reports = cvm_httpclient.get_report(row["numero_seq_documento"], row["codigo_tipo_instituicao"], reports_list=reports_list)
    for report in reports:
        print(report)
        reports[report]["cod_cvm"] = row["cod_cvm"]
                
df_report = pd.DataFrame.from_dict(reports,index = 'Balanço Patrimonial Ativo')

print('Exportar')
df_report.to_csv('C:\\Users\mafeitosa\OneDrive - UNIVERSO ONLINE S.A\Área de Trabalho\Temporário\CVM', 
                 index=False)