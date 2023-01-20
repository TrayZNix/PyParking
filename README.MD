# PyParking

Pyparking es una aplicación creada para gestionar parkings, ya sea los ingresos de coches de clientes , sus salidas, o sus clientes abonados.

## ¿Como funciona?

Está creado completamente en Python, haciendo uso de la librería *"Pickle"* para persistir los datos.
La interfaz es intuitiva.

## Datos inicializados:

Los archivos **pickle** que incluyo en el repositorio traen precargados datos. Estos son:

- El ingreso y retirada de un coche, para poder consultar los cobros en la primera opción de las funciones de administrador.
- Una moto, para probar retirar un vehículo no abonado:
  ![Imagen con los datos de la moto](https://raw.githubusercontent.com/TrayZNix/PyParking/main/imagenes/moto_1.png)
- Un usuario abonado, con los siguientes datos, tanto de él como su vehículo abonado:
- ![Datos del usuario abonado](https://raw.githubusercontent.com/TrayZNix/PyParking/main/imagenes/abono_1.png)

## Información importante

Es importante que, el usuario, al introducir datos que requieran un número únicamente (Por ejemplo, seleccionar 1. para confirmar o 0. para denegar), se aseguren de que introducen un número, de lo contrario, el programa lo contará como un error en la lectura y será devuelto al menú de decisión
