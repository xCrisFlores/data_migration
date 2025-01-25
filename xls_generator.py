#Archivo generador de excel
#importacion de las librerias necesarias
import pandas as pd

def gen_xls(data1,data2,data3,data4):

    """
    Esta funcion lee los dataframes y los convierte cada uno en hojas de excel
    """

    #generacion de un archivo excel con los data frames creados
    with pd.ExcelWriter('ventas_datos.xlsx') as writer:
        data1.to_excel(writer, sheet_name='Clientes', index=False)
        data2.to_excel(writer, sheet_name='Ventas', index=False)
        data3.to_excel(writer, sheet_name='Productos', index=False)
        data4.to_excel(writer, sheet_name='Ventas-Productos', index=False)