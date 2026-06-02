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
