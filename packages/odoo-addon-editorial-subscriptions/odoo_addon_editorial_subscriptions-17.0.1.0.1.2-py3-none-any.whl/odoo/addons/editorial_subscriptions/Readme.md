# Editorial Subscriptions


## Configuración
1. Ir a ajustes del módulo de “gestión editorial” y activar el módulo de suscripciónes. Esta opción instala el módulo 
Subscription Manager gestionado por la OCA (https://odoo-community.org/shop/subscription-management-715311#attr=941148).

2. Se mostrará otra opción para “Incluir funciones editoriales". Esta opción instala las modificaciones al módulo Subscription Manager 
específicas para la gestión editorial.

3. Crear plantilla de suscripción
   1. Ir a “Suscripciones” → Configuración → Plantillas de suscripción
   2. Pulsar Nuevo
   3. Indicar un nombre y las condiciones de frecuencia de la suscripción

4. Crear producto de suscripción
   1. Ve a Productos -> Nuevo, y crea un nuevo producto que servirá para crear automáticamente una suscripción a partir de la venta de ese producto.
   2. Ve a la pestaña de “Ventas” y seleccionar el campo “Producto suscribible”
   3. Se mostrará un campo para indicar la Plantilla de suscripción. Indica aquí qué plantilla se usará cuando se venda este producto
   4. Si el producto no requiere inventariado, en la pestaña de “Información general”, selecciona el Tipo de producto como “Servicio”.
   5. Completa el resto de detalles como precio de venta, impuestos, etc.


## Uso
1. Cuando un cliente se inscriba en una de las suscripciones. Iremos a la sección de Ventas y crearemos una nueva venta 
indicando el producto de suscripción que creamos en el paso anterior.
2. Al confirmar la venta, podemos comprobar que la suscripción se ha creado correctamente en el apartado “Suscripciones”.
3. Para añadir un libro a las suscripciones en curso tenemos que ir a la ficha del libro que queramos incluir y pulsar 
el botón “Añadir a suscripciones”.
4. Al pulsar el botón nos dejará filtrar por plantilla de suscripción o por suscriptor.
5. Al confirmar, se añadirá el libro a las suscripciones mostradas. Además se creará una orden de entrega para cada cliente. 
Las órdenes de entrega se pueden consultar desde Inventario →Libros a suscripción.