#Archivo con los modelos de los datos de la nueva estructura, necesarios para la migracion a la base de datos
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

#modelo para la tabla de clientes
class Client(Base):
    __tablename__ = 'clientes'
    id_cliente = Column(Integer, primary_key=True)
    cliente = Column(String(255), nullable=False)

#modelo para la tabla de productos
class Product(Base):
    __tablename__ = 'productos'
    id_producto = Column(Integer, primary_key=True)
    producto = Column(String(255), nullable=False)
    precio = Column(Float, nullable=False)

#modelo para la tabla de ventas
class Sale(Base):
    __tablename__ = 'ventas'
    id_venta = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, nullable=False)
    total = Column(Float, nullable=False)
    fecha_pedido = Column(String(255), nullable=False)
    fecha_entregado = Column(String(255), nullable=False)
    comentarios = Column(String(1000))
    pagado = Column(Boolean)
    metodo_pago = Column(String(255))

#modelo para la tabla transitoria entre ventas y productos
class SaleProduct(Base):
    __tablename__ = 'ventas_productos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_venta = Column(Integer, ForeignKey('ventas.id_venta'), nullable=False)  # Clave foránea hacia ventas
    id_producto = Column(Integer, ForeignKey('productos.id_producto'), nullable=False)  # Clave foránea hacia productos
    cantidad = Column(Float, nullable=False)

