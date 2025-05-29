import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('TEST/stress_insultServer.csv')

# Forza los tipos numéricos correctos
num_cols = ['n_peticiones', 'workers', 'tiempo_total', 'req/s', 't_media']
for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Quita XMLRPC
df = df[(df['servicio'] == 'InsultServer') & (df['sistema'] != 'XMLRPC')]

cols_to_avg = ['n_peticiones', 'tiempo_total', 'req/s', 't_media']

# 1. Gráfica de tiempo total vs número de workers (para cada sistema)
plt.figure()
for sistema in df['sistema'].unique():
    sub = df[df['sistema'] == sistema]
    sub_grouped = sub.groupby('workers')[cols_to_avg].mean().reset_index()
    plt.plot(sub_grouped['workers'], sub_grouped['tiempo_total'], marker='o', label=sistema)
plt.xlabel('Número de workers')
plt.ylabel('Tiempo total (s)')
plt.title('Tiempo total vs número de workers')
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

# 2. Gráfica de throughput (req/s) vs workers
plt.figure()
for sistema in df['sistema'].unique():
    sub = df[df['sistema'] == sistema]
    sub_grouped = sub.groupby('workers')[cols_to_avg].mean().reset_index()
    plt.plot(sub_grouped['workers'], sub_grouped['req/s'], marker='o', label=sistema)
plt.xlabel('Número de workers')
plt.ylabel('Throughput (req/s)')
plt.title('Throughput vs número de workers')
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

# 3. Gráfica de tiempo medio por petición vs workers
plt.figure()
for sistema in df['sistema'].unique():
    sub = df[df['sistema'] == sistema]
    sub_grouped = sub.groupby('workers')[cols_to_avg].mean().reset_index()
    plt.plot(sub_grouped['workers'], sub_grouped['t_media'], marker='o', label=sistema)
plt.xlabel('Número de workers')
plt.ylabel('Tiempo medio por petición (s)')
plt.title('Tiempo medio por petición vs número de workers')
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

# 4. Gráfica de Speedup (T1 / TN) vs workers para cada sistema y cada n_peticiones (UNA GRÁFICA POR MIDDLEWARE)
for sistema in df['sistema'].unique():
    plt.figure()
    sub = df[df['sistema'] == sistema]
    for n_peticiones in sorted(sub['n_peticiones'].unique()):
        sub_n = sub[sub['n_peticiones'] == n_peticiones].sort_values('workers')
        if 1 in sub_n['workers'].values:
            t1 = sub_n[sub_n['workers'] == 1]['tiempo_total'].values[0]
            speedup = t1 / sub_n['tiempo_total']
            plt.plot(sub_n['workers'], speedup, marker='o', label=f"{n_peticiones} req")
    plt.xlabel('Número de workers')
    plt.ylabel('Speedup')
    plt.title(f'Speedup vs número de workers ({sistema})')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()
