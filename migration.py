#Archivo de limpieza de datos y migracion de los mismos

#importacion de las librerias necesarias
import pandas as pd
#importacion de la sesion de la base de datos y de los modelos
from session import session
from models import Client, Product, Sale, SaleProduct

def data_cleaning(insertions_flag):

    """
    Esta funcion lee el csv inicial de la prueba, limpia y formatea los datos dañados 
    y genera dataframes para su manipulacion para graficas u hojas de calculo,
    ademas, en caso de que la bandera este activa, estos datos seran migrados a una base
    de datos SQL
    """
    
    insertions_flag = bool(int(insertions_flag))
    #Extraer los datos del archivo usando pandas
    data = pd.read_csv("bdd.csv")

    #Extraer y normalizar los valores de cada columna necesarios para la tabla de clientes

    clients = data.iloc[4:,1]
    clients_unique = clients.unique() #Asegurar que no hay clientes repetidos
    id_clients = [i + 1 for i in range(len(clients_unique))] # Generacion de indices numericos para los clientes

    #Extraer y normalizar los valores de cada columna necesarios para la tabla de ventas
    i = 0
    sales = data.iloc[4:,0]
    sales = [int(sale[:-1]) if "S" in sale else int(sale) for sale in sales] #Limpieza necesaria para algunos indices con el carater "S" de mas
    if len(sales) != len(set(sales)):
        min_value = min(sales)  # Valor mínimo actual en la lista
        duplicates = [x for x in sales if sales.count(x) > 1]  # Lista de valores duplicados
        seen = set()  # Para rastrear duplicados ya corregidos

        for idx, sale in enumerate(sales):
            if sale in seen:
                i += 1
                sales[idx] = min_value - i  # Asignar un nuevo valor único menor que el mínimo
            else:
                seen.add(sale)  # Marcar el valor como visto
        
    #Generacion de un diccionario para relacionar el id de los clintes con su nombre
    client_mapping = {client: id_clients[i] for i, client in enumerate(clients_unique)}
    fk_clients = [client_mapping[client] for client in clients] #Asignacion de la clave del diccionario segun el nombre del cliente

    #Limpieza del campo total eliminando caracteres inecesarios
    total = data.iloc[4:,2]
    total = [t[:len(t)-3] for t in total]
    total = [t[1:len(t)] if "$" in t else t for t in total]
    total = [t.replace('.', '') for t in total]
    total = [float(t) for t in total]

    date_req = data.iloc[4:,3]
    date_del = data.iloc[4:,4]

    #Otros campos que no necesitan limpieza
    comments = data.iloc[4:,5]
    comments = [comment if pd.notna(comment) else "" for comment in comments]
    payment = data.iloc[4:,6]
    isBuyed = [1 if pd.notna(p) else 0 for p in payment]#Asignacion del valor booleano para todos aquellos campos no vacios(suponiendo que son metodos de pago validos o si se efecturon)
    payment = [p if p == "EFECTIVO" or p == "TRANSFERENCIA" else "" for p in payment]#Limpieza de valores atipicos dejando solo los valores de efectivo y transferencia

    #Extraer y normalizar los valores de cada columna necesarios para la tabla de productos

    products_cols = data.iloc[:, 7:]#Extraccion de los valores de las columnas de cada producto
    products = products_cols.iloc[3] 
    id_products = [i + 1 for i in range(len(products))]#Generacion de indices para los productos
    products = products.unique()
    prices = [0 for i in range(len(products))]#Generacion de precios para los productos inicializados en 0

    #Dicciorarios con los datos del csv
    clients_data = {
        'ID cliente': id_clients,
        'Clientes': clients_unique,
    }

    sales_data = {
        'Numero de pedido': sales,
        'ID cliente': fk_clients,
        'Total': total,
        'Fecha pedido': date_req,
        'Fecha entregado': date_del,
        'Comentarios': comments,
        'Pagado': isBuyed,
        'Metodo de pago': payment
    }

    products_data = {
        'ID Producto': id_products,
        'Producto': products,
        'Precio': prices
    }

    sales_products_data = []

    #Insertar registros unicamente si se requiere por el usuario
    if(insertions_flag):
        #Insercion de ventas en la base de datos
        for i in range(len(id_clients)):
            client = Client(
                id_cliente=id_clients[i],
                cliente=clients_unique[i],
            )
            session.add(client)
            
        #Insercion de ventas en la base de datos
        for i in range(len(sales)):
            sale = Sale(
                id_venta=sales[i],
                id_cliente=fk_clients[i],
                total=total[i],
                fecha_pedido="",
                fecha_entregado="",
                comentarios=comments[i],
                pagado=isBuyed[i],
                metodo_pago=payment[i]
            )
            session.add(sale)

        #Insercion de productos en la base de datos
        for i in range(len(id_products)):
            product = Product(
                id_producto=id_products[i],
                producto=products[i],
                precio=prices[i]
            )
            session.add(product)


    #Generacion del diccionario de ventas-productos
    #iterar entre los indices y filas de los campos de cada producto
    for idx, row in data.iterrows():
        sale_id = sales[idx - 5]  #indice de la venta
        quantities = row[7:].values  #valores de las cantidades de los productos
        
        #iterar entre cada producto para calcular las cantidades
        for product_id, quantity in zip(id_products, quantities):
            #agregar registros solo si la cantidad es mayor que 0
            try:
                quantity = float(quantity)  # Intentar convertirlo a número
            except ValueError:
                quantity = 0  # Si no se puede convertir, asignar 0
            
            if quantity > 0:
                sales_products_data.append({
                    'Numero de pedido': sale_id,
                    'ID Producto': product_id,
                    'Cantidad': quantity
                })
                #Insertar registros unicamente si se requiere por el usuario
                if(insertions_flag):    
                    #insercion de los datos a la base de datos usando el respectivo modelo
                    sale_product = SaleProduct(id_venta=sale_id, id_producto=product_id, cantidad=quantity)
                    session.add(sale_product)

    if(insertions_flag):
        #cierre de la sesion a la base de datos
        session.commit()
        session.close()

    #creacion de los data frames
    data1 = pd.DataFrame(clients_data)
    data2 = pd.DataFrame(sales_data)
    data3 = pd.DataFrame(products_data)
    data4 = pd.DataFrame(sales_products_data)

    #Retornar los dataframes y algunos arreglos necesarios
    return data1, data2, data3, data4, total, date_req