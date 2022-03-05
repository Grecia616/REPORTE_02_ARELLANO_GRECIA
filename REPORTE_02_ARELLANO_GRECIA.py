#%% Importar módulos
from itertools import product
from unicodedata import name
import pandas as pd
import matplotlib.pyplot as ptl
import seaborn as sns

# %%# Variable para leer base de datos
base_de_datos = pd.read_csv("synergy_logistics_database.csv", parse_dates =[5])

#%% Para interpretar el año
base_de_datos["month"] = base_de_datos["date"].dt.month
base_de_datos["año_mes"] = base_de_datos["date"].dt.to_period("m")

#%%
""" ___________________________1. 10 RUTAS MÁS DEMANDADAS (M, X)__________________________________
1. Frecuencia de rutas (porcentaje del top 10)
"""

#%% #Agrupar por origen y destino 
rutas = base_de_datos.groupby(["direction","origin", "destination"]).count()["transport_mode"]
rutas

#%%Ordenar rutas de mayor a menor e imprimir únicamente los 10 primeros
rutas_orden = rutas.sort_values(ascending=False).head(10)

#%% Suma total del top 10 frecuencias de rutas 
rutas_top_frecuencia = rutas_orden.sum()

#%% Cambiar las series a datafreame
rutas_orden = rutas.reset_index()

#%% Suma total de todas las frecuencias de rutas
rutas_total_frecuencia = rutas.sum()

#%% Cálculo de porcentaje
porcentaje_frecuencia = (rutas_top_frecuencia* 100) // rutas_total_frecuencia
print(f"El porcentaje de las 10 rutas con mayor frecuencia es de {porcentaje_frecuencia} %")

#%%
"""
2. Valor total de rutas (porcentaje del top 10)
"""

#%% Variable para calcular el total value
rutas_2 = base_de_datos.groupby(["direction", "origin", "destination"]).sum()["total_value"]

#%%Ordenar rutas de mayor a menor e imprimir únicamente los 10 primeros
rutas_orden_2 = rutas_2.sort_values(ascending=False).head(10)

#%% Suma del valor total del top 10 rutas
rutas_top_value = rutas_orden_2.sum()

#%% Cambiar series a dataframe
rutas_orden_2 = rutas_2.reset_index()

#%% Suma total de todas las frecuencias de rutas
rutas_total_value = rutas_2.sum()

#%% Cálculo de porcentaje
porcentaje_value = (rutas_top_value* 100) // rutas_total_value
print(f"El porcentaje de las 10 rutas con mayor valor es de {porcentaje_value} %")

#%%
""" _______________ 3 MEDIOS DE TRANSPORTE medios de transporte con mayor frecuencia de uso___________
1. Transporte - valor total
"""

#%% Se crea la variable transportes que tiene (x,m) + total value
transporte = base_de_datos [["direction", "transport_mode","total_value"]]

#______________EXPORTACIONES

#%% Filtrar Exportaciones, se pasan a booleanos
transporte_x = transporte ["direction"] == "Exports"

#%% Se imprimen nombres finales
transporte_x_filtrado= transporte[transporte_x]

#%% Suma total_value por medio de transporte
filtro_x = transporte_x_filtrado.groupby(by=["transport_mode"]).sum()

#____________IMPORTACIONES

#%% Filtrar Importaciones, se pasan a booleanos
transporte_m = transporte ["direction"] == "Imports"

#%% Se imprimen nombres finales
transporte_m_filtrado= transporte[transporte_m]

#%% Suma total_value por medio de transporte
filtro_m = transporte_m_filtrado.groupby(by=["transport_mode"]).sum()

#%%Combinación tabla X e M
x_m = pd.concat([filtro_x, filtro_m], axis = 1)

#Asignado nombres correspondientes a las columnas
x_m.columns = ["Valor Total Exportaciones", "Valor Total Importaciones"]

"""
2. Datos por año
"""

#%% Se establece un grupo para calcular el conteo y valor anual
transporte_anual = base_de_datos.groupby(by=["year","transport_mode"])
conteo_anual_transporte = trans_anual ["total_value"].describe()["count"]
valor_anual_transporte = trans_anual ["total_value"].agg(pd.Series.sum)

#%% Se crea dataframe con series valor y conteo
count_valor = pd.DataFrame()
count_valor["conteo"] = conteo_anual_transporte
count_valor["valor"] = valor_anual_transporte

#%%
"""
Análisis por medio de gráficas
"""
#%% Gráfica de barras de médios de transporte
sns.countplot(data = base_de_datos, x = "transport_mode")

#%% Gráfica de lineas para medios de transporte a través del tiempo (2015-2020) conteo
sns.lineplot( x = "year", y = "conteo", hue = "transport_mode", data = count_valor)

#%% Gráfica de lineas para medios de transporte a través del tiempo (2015-2020) valor
sns.lineplot( x = "year", y = "valor", hue = "transport_mode", data = count_valor)

#%%
"""_______________________________ 3. VALOR TOTAL DE LAS X e M____________________________________"""

# %% Ingreso agrupado por Exportaciones e Importaciones 
valor_xm = base_de_datos.groupby("direction"). sum()["total_value"]
print(valor_xm)

#%%  Valor global
valor_total = valor_xm.sum()
print(valor_total)

#%%----Paises que generan el 80 de X

#%%  Se crea lista de X 
exportaciones = base_de_datos[base_de_datos["direction"] =="Exports"]

#%%Paises que aportan mayor valor
suma_paises_x = exportaciones.groupby("destination").sum()["total_value"]

#%% Ordenar datos
suma_exportaciones_total = suma_paises_x.sort_values (ascending=False)

#%% Porcentaje por país
# Convertimos el multi - índice a series
suma_exportaciones_total = suma_exportaciones_total.reset_index()

#%% Suma de la columna total_value
total_exp = suma_exportaciones_total["total_value"].sum()

#%% Se crea nueva columna para porcentaje por país
suma_exportaciones_total["porcentaje_x"] = (suma_exportaciones_total["total_value"]/ total_exp)*100

#%% Se crea nueva columna para porcentaje
suma_exportaciones_total["porcentaje_x_acumulado"] = suma_exportaciones_total.cumsum()["porcentaje_x"]

#%%----Paises que generan el 80% del valor de M

#%% Se crea lista de M
importaciones = base_de_datos[base_de_datos["direction"]=="Imports"]

#%% Paises que aportan mayor valor
suma_paises_m = importaciones.groupby("origin").sum()["total_value"]

#%% Ordenar datos
suma_importaciones_total =  suma_paises_m.sort_values(ascending= False)

#%% Porcentaje por país 
#Convertimos el multi-índice a series
suma_importaciones_total = suma_importaciones_total.reset_index() 

#%% Suma de la columna total_value
total_imp = suma_importaciones_total["total_value"].sum()

#%% Se crea nueva columna para porcentaje por país
suma_importaciones_total["porcentaje_m"] = (suma_importaciones_total["total_value"]/ total_imp)*100

#%% Se crea nueva columna para porcentaje
suma_importaciones_total["porcentaje_m_acumulado"] = suma_importaciones_total.cumsum()["porcentaje_m"]

