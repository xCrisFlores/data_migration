#Archivo principal que importa las herramientas necesarias para toda la limpieza, migracion y el analisis

#importacion de las librerias necesarias y modulos principales
import pandas as pd
from migration import data_cleaning
from ploting import plot_info
from xls_generator import gen_xls

#Preguntar si se requiere migrar los datos a SQL, solo especificar que si en caso de que no existan datos
insertions_flag = input("Deseas migrar la estructura a una base de datos existente?, 1: si, 0: no")
#Recoleccion de los dataframes generados
data1,data2,data3,data4,total,date_req = data_cleaning(insertions_flag)

#Preguntar si se requiere generar un archivo excel con los datos, solo especificar que si en caso de que no existan dicho archivo
xls_flag = input("Deseas generar un archivo excel con los datos?, 1: si, 0: no")
if(xls_flag):
    gen_xls(data1,data2,data3,data4)

#Preguntar si se requieren visualizar los datos en graficas
xls_flag = input("Deseas visualizar informacion util en graficas?, 1: si, 0: no")
if(xls_flag):
    plot_info(data3,data4,total,date_req)