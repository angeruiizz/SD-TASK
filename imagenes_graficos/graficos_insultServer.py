import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Cargar datos
df = pd.read_csv('TEST/stress_insultServer.csv')

# 1. Rendimiento (req/s) vs Número de Workers/Consumidores para cada sistema
plt.figure(figsize=(10, 6))
for sistema in df['sistema'].unique():
    subset = df[df['sistema'] == sistema]
    medios = subset.groupby('Workers/Consumidores')['req/s'].mean()
    plt.plot(medios.index, medios.values, marker='o', label=sistema)
plt.xlabel('Número de Workers/Consumidores')
plt.ylabel('Peticiones por segundo (req/s)')
plt.title('Rendimiento vs Número de Consumidores/Servidores')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 2. Tiempo total vs Número de Workers/Consumidores para cada sistema (sin XMLRPC)
plt.figure(figsize=(10, 6))
for sistema in df['sistema'].unique():
    if sistema == 'XMLRPC':
        continue
    subset = df[df['sistema'] == sistema]
    medios = subset.groupby('Workers/Consumidores')['tiempo_total'].mean()
    plt.plot(medios.index, medios.values, marker='o', label=sistema)
plt.xlabel('Número de Workers/Consumidores')
plt.ylabel('Tiempo total (s)')
plt.title('Tiempo total vs Número de Workers/Consumidores (sin XMLRPC)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 3. Speedup vs Número de Workers/Consumidores para cada sistema

sistemas = df['sistema'].unique()
fig, axs = plt.subplots(1, len(sistemas), figsize=(18, 5), sharey=True)
markers = ['o', 's', 'D', '^', 'v']

for i, sistema in enumerate(sistemas):
    subset = df[df['sistema'] == sistema]
    cargas = sorted(subset['n_peticiones'].unique())
    for j, carga in enumerate(cargas):
        subcarga = subset[subset['n_peticiones'] == carga]
        tiempos = subcarga.groupby('Workers/Consumidores')['tiempo_total'].mean().sort_index()
        if 1 in tiempos.index:
            speedup = tiempos.loc[1] / tiempos
            axs[i].plot(speedup.index, speedup.values, marker=markers[j % len(markers)], label=f'{carga} req')
    axs[i].set_title(sistema)
    axs[i].set_xlabel('Número de Workers/Consumidores')
    axs[i].grid(True)
    axs[i].legend(title='Carga')
axs[0].set_ylabel('Speedup')
plt.suptitle('Speedup vs Número de Workers/Consumidores por Middleware')
plt.tight_layout()
plt.show()

# 4. Tiempo medio de respuesta (t_media) vs Workers/Consumidores para cada sistema (sin XMLRPC)
plt.figure(figsize=(10, 6))
for sistema in df['sistema'].unique():
    if sistema == 'XMLRPC':
        continue
    subset = df[df['sistema'] == sistema]
    medios = subset.groupby('Workers/Consumidores')['t_media'].mean()
    plt.plot(medios.index, medios.values, marker='o', label=sistema)
plt.xlabel('Número de Workers/Consumidores')
plt.ylabel('Tiempo medio de respuesta (s)')
plt.title('Tiempo medio de respuesta vs Número de Workers/Consumidores (sin XMLRPC)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Extra: Rendimiento (req/s) vs Número de peticiones para cada sistema y Workers/Consumidores=3
plt.figure(figsize=(10, 6))
for sistema in df['sistema'].unique():
    subset = df[(df['sistema'] == sistema) & (df['Workers/Consumidores'] == 3)]
    plt.plot(subset['n_peticiones'], subset['req/s'], marker='o', label=sistema)
plt.xlabel('Número de peticiones')
plt.ylabel('Peticiones por segundo (req/s)')
plt.title('Rendimiento vs Número de Peticiones (Workers/Consumidores=3)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
