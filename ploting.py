#Archivo de graficacion de datos

#importacion de las librerias necesarias
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_info(data3,data4,total,date_req):

    """
    Esta funcion lee los dataframes necesarios para la generacion un analisis simple,
    los productos con mayor y menor venta asi como los dias con mayor o menor venta
    """
    
    #Calculo de los totales de productos vendidos y la extraccion de los nombres
    total_sales_by_product = data4.groupby('ID Producto')['Cantidad'].sum()
    product_names = data3.set_index('ID Producto')['Producto']

    #Creacion de dataframes para la visualizacion de datos a partir de las listas creadas anteriormente
    df_products = pd.DataFrame({
        'Producto': [product_names[product_id] for product_id in total_sales_by_product.index],
        'Cantidad': total_sales_by_product.values
    })

    df_dates = pd.DataFrame({
        'Total': total,
        'Fecha pedido': date_req,
    })


    y_min = min(total)
    y_max = max(total)

    #graficos para la visualizacion de datos

    #grafico de la cantidad total de productos vendidos
    plt.figure(figsize=(10, 6))

    most_sold_product = df_products.loc[df_products['Cantidad'].idxmax()]
    least_sold_product = df_products.loc[df_products['Cantidad'].idxmin()]

    sns.barplot(
        x='Producto',
        y='Cantidad',
        data=df_products,
        palette='viridis'
    )
    plt.title('Cantidad total vendida por producto', fontsize=14)
    plt.xlabel('Productos', fontsize=12)
    plt.ylabel('Cantidad total vendida', fontsize=12)
    plt.xticks(rotation=90, fontsize=10)

    plt.legend(
        labels=[
            f"Mas vendido: {most_sold_product['Producto']} ({most_sold_product['Cantidad']})",
            f"Menos vendido: {least_sold_product['Producto']} ({least_sold_product['Cantidad']})"
        ],
        title="Resumen",
        loc="upper right",
        fontsize=10,
        title_fontsize=12
    )

    plt.tight_layout()
    plt.show()

    #grafico de las ventas y sus totales
    plt.figure(figsize=(20, 12))

    max_sales_day = df_dates.loc[df_dates['Total'].idxmax()]
    min_sales_day = df_dates.loc[df_dates['Total'].idxmin()]

    sns.barplot(
        x='Fecha pedido',
        y='Total',
        data=df_dates,
        palette='magma'
    )

    y_min = df_dates['Total'].min()
    y_max = df_dates['Total'].max()

    y_ticks = [y_min, (y_min + y_max) / 2, y_max] 
    plt.yticks(ticks=y_ticks)
    plt.xticks(rotation=90, fontsize=5)
    plt.legend(
        labels=[
            f"Dia con mayor venta: {max_sales_day['Fecha pedido']} ({max_sales_day['Total']:.2f})",
            f"Dia con menor venta: {min_sales_day['Fecha pedido']} ({min_sales_day['Total']:.2f})"
        ],
        title="Resumen",
        loc="upper right",
        fontsize=10,
        title_fontsize=12
    )
    plt.tight_layout()
    plt.show()