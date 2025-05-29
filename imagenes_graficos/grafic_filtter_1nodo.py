import pandas as pd
import matplotlib.pyplot as plt

# Carga de datos
df = pd.read_csv('TEST/stress_insultfiltter.csv')


# Filtrar solo los datos del servicio InsultFilter, con workers=1 y quitando XMLRPC
df1 = df[(df['servicio'] == 'InsultFilter') & (df['workers'] == 1) & (df['sistema'] != 'XMLRPC')]

# Listado de middlewares únicos
sistemas = df1['sistema'].unique()

# 1. Requests per Second (req/s) vs. Número de Peticiones
plt.figure(figsize=(8,5))
for sistema in sistemas:
    df_sys = df1[df1['sistema'] == sistema]
    plt.plot(df_sys['n_peticiones'], df_sys['req/s'], marker='o', label=sistema)
plt.title('Requests per Second vs. Número de Peticiones (InsultFilter, workers=1)')
plt.xlabel('Número de Peticiones')
plt.ylabel('Requests per Second (req/s)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 2. Tiempo total vs. Número de Peticiones
plt.figure(figsize=(8,5))
for sistema in sistemas:
    df_sys = df1[df1['sistema'] == sistema]
    plt.plot(df_sys['n_peticiones'], df_sys['tiempo_total'], marker='o', label=sistema)
plt.title('Tiempo Total vs. Número de Peticiones (InsultFilter, workers=1)')
plt.xlabel('Número de Peticiones')
plt.ylabel('Tiempo Total (s)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 3. Tiempo medio por petición vs. Número de Peticiones
plt.figure(figsize=(8,5))
for sistema in sistemas:
    df_sys = df1[df1['sistema'] == sistema]
    plt.plot(df_sys['n_peticiones'], df_sys['t_media'], marker='o', label=sistema)
plt.title('Tiempo Medio por Petición vs. Número de Peticiones (InsultFilter, workers=1)')
plt.xlabel('Número de Peticiones')
plt.ylabel('Tiempo Medio por Petición (s)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
