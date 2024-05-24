# LEITURA DOS DADOS
import pandas as pd
pd.set_option('display.max_rows', 100)
uri = 'https://raw.githubusercontent.com/sthemonica/alura-voz/main/Dados/Telco-Customer-Churn.json'
df = pd.read_json(uri)
print(df.head())


# NORMALIZAÇÃO DO JSON
def normalizar_json(dados):
    json_normalizado = pd.DataFrame()
    data_frame = pd.DataFrame()
    for coluna in dados.columns[2:]:
        json_normalizado = pd.concat([json_normalizado, pd.json_normalize(data=dados[coluna])], axis=1)
    
    data_frame = pd.concat([dados.iloc[:, 0:2], json_normalizado], axis=1)
    return data_frame

df = normalizar_json(df)


# AJUSTE DE NOME DAS COLUNAS
rename = {
    'customerID':'id_cliente',
    'Churn':'churn',
    'gender':'genero',
    'SeniorCitizen':'idoso',
    'Partner':'possui_parceiro',
    'Dependents':'possui_dependentes',
    'tenure':'meses_contrato',
    'PhoneService':'assinatura_telefone',
    'MultipleLines':'linhas_multiplas',
    'InternetService':'assinatura_provedor_internet',
    'OnlineSecurity':'assinatura_seguranca',
    'OnlineBackup':'assinatura_backup',
    'DeviceProtection':'assinatura_protecao_dispositivo',
    'TechSupport':'assinatura_suporte_tecnico',
    'StreamingTV':'assinatura_tv_cabo',
    'StreamingMovies':'assinatura_streaming_filmes',
    'Contract':'tipo_contrato',
    'PaperlessBilling':'fatura_online',
    'PaymentMethod':'forma_pagamento',
    'Charges.Monthly':'valor_fatura_mensal',
    'Charges.Total':'valor_total_pago'
}

df = df.rename(columns=rename)


# EXPLORE
print(df.info())

for coluna in df.columns:
    print('---',coluna,'---')
    print(df[coluna].value_counts())
    print('***************************')

# Removendo as linhas sem label de churn
df = df[df['churn'] != '']

# Há 11 ocorrências missing em valor_total_pago que são referentes a clientes que não completaram 1 mês de contrato
# Esses valores serão preenchidos com 0
filtro = df['valor_total_pago'] == ' '
print(df[filtro])
df['valor_total_pago'][filtro] = 0

# Tipagem da feature valor_total_pago
df['valor_total_pago'] = df['valor_total_pago'].astype('float64')

print(df.head())

df.to_csv('churn.csv', index=False)
