# Script de migracion de datos
Este es un proyecto que se compone de distintos modulos, necesarios para realizar la limpieza, migracion y el analisis de los datos del archivo de excel de la prueba, a grandes razgos, el script principal integra los modulos de limpiza y migracion, de generacion hojas de calculo y de la visualizacion de datos usando Python y librerias como SQLAlchemy, Pandas, Seaborn y Matplotlib.
## ¿Como se usa?
Antes de poner en marcha este script es necesario que cuentes con las siguientes tecnologias instaladas:
* [Python](https://www.python.org/downloads/windows/)
* [Maria db](https://mariadb.org/download/?t=mariadb&p=mariadb&r=11.6.2&os=windows&cpu=x86_64&pkg=msi&mirror=accretive) (Opcional o alguna otra distribucion de SQL)
* [Git](https://git-scm.com/downloads) (Opcional si deseas clonar el repositorio)

Puedes iniciar clonando este repositorio usando el siguiente comando git:
```
git clone https://github.com/xCrisFlores/data_migration.git
```
O en su defecto simplemente descarga el proyecto desde esta pagina, Una vez que tengas el proyecto dirigete a el en tu explorador de archivos y abre una terminal, o navega a el desde una terminal si conoces la ruta. Ahora deberas ejecutar el siguiente comando para instalar las dependencias del proyecto:
```
pip install requirements.txt
```
Una vez que hays instalado las dependencias, necesitas crear al menos la base de datos, si instalaste maria db, guarda los datos necesarios para la conexion con tu servidor local, ahora deberas lleanr los valores del archivo de conexion "session.py" para lograr la conexion con el script y la base de datos, posterior a esto pudes usar la UI de Maria db, Heidi SQL para crear la base de datos, esto es necesario ya que necesitas especificar este dato en la conexion.
Una vez que tienes la base de datos creada y el archivo "session.py" completo puedes ejecutar el script con el siguiente comando.
```
python main.py
```
Esto ejecutara el script, ahora debes especificar las tareas que deseas que realice, debes ingresar el valor de 0 en caso de que no requieras la tarea o 1 si es que la requieres, debes tener cuidado con los valores ingresados ya que solo acepta estos valores ademas, la tarea de migrar los datos a SQL y la generacion del archivo excel solo puede realizarse la primera vez, a menos que elimines el archivo y la base de datos y volverla a crear respectivamente para cada tarea.
