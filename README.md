# DATOS DEL APRENDIZ

NOMBRE: Janer Duvan Rivas Rodriguez
FICHA: 3407186

# Funcionalidades desarrolladas

## Clientes

Para comenzar trabajé la parte de clientes que ya se habia realizado en clases anteriores, donde realicé un CRUD completo. Esto permite registrar nuevos clientes, consultar los que ya se encuentran guardados, buscarlos por su ID, actualizar sus datos y eliminarlos cuando sea necesario. Toda la información se va guardando en la lista `lista_clientes`, que funciona como una pequeña base de datos mientras la aplicación está en ejecución.

## Facturas

Después continué con las facturas. Aquí implementé las funciones para crear facturas y relacionarlas con un cliente que ya estuviera registrado. También agregué opciones para consultar todas las facturas, buscar una factura específica por su ID, eliminarlas y ver todas las facturas que tiene un cliente. La información se almacena en la lista `lista_facturas`.

## Transacciones

Por último desarrollé la parte de transacciones, que son los productos o servicios que se agregan a una factura. Antes de registrar una transacción, el sistema verifica que el cliente exista y que la factura corresponda correctamente. Además, se pueden consultar las transacciones registradas, buscarlas por ID, actualizarlas o eliminarlas. Estas se guardan en la lista `lista_transacciones` y quedan asociadas a su respectiva factura.

## Experiencia durante la práctica

La verdad, al principio me enredé un poco con algunas cosas, especialmente cuando tocó relacionar clientes, facturas y transacciones. Sin embargo, a medida que fui haciendo pruebas, revisando errores y repitiendo varias veces el proceso, fui entendiendo mejor cómo funcionaba todo. Muchas de las funciones que agregué, como buscar facturas por ID o consultar las facturas de un cliente específico me acostubre a ellas por el hecho de repetirlas


Segundo Trabajo del Project_Clients

1. Se reorganizó la estructura del proyecto creando el archivo conexion_bd.py, donde se almacenan las listas de clientes, facturas y transacciones para simular una base de datos en memoria.

2. Se separó la lógica de los endpoints en diferentes archivos dentro del módulo enrutador, creando los archivos clientes.py, facturas.py y transacciones.py para mejorar la organización y el mantenimiento del código.

3. Se configuraron los APIRouter de FastAPI y se enlazaron correctamente con el archivo main.py mediante include_router(), permitiendo que todos los endpoints quedaran disponibles desde un único punto de entrada.

4. Se agregaron prefijos (prefix) y etiquetas (tags) a cada enrutador para organizar la documentación generada automáticamente por Swagger y facilitar la identificación de los servicios.

5. Se implementó la relación entre clientes, facturas y transacciones, validando la existencia de clientes y facturas antes de registrar nuevas transacciones.

6. Se desarrolló la funcionalidad para calcular automáticamente el valor total de una factura a partir de las transacciones registradas, multiplicando la cantidad por el valor unitario de cada producto y sumando los resultados.

7. Se realizaron pruebas de creación, consulta, edición y eliminación de clientes, facturas y transacciones para verificar el correcto funcionamiento de los procesos CRUD implementados.

8. Se verificó que la información se mantuviera correctamente relacionada entre los diferentes módulos del sistema, garantizando la integridad de los datos durante las operaciones realizadas.
