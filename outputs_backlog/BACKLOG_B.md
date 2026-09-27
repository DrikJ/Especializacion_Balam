# Product Backlog: Módulo de Rastreo Aduanero

## 1. Resumen del Proyecto
Sistema diseñado para rastrear el ingreso de contenedores en una bodega aduanera del puerto de Manzanillo y gestionar notificaciones automáticas por correo electrónico cuando se presenten retrasos en la estadía permitida.

---

## 2. Requerimientos Funcionales (Historias de Usuario)

### RF01: Registro de Ingreso
**Como** Operador de Aduana,  
**Quiero** registrar el ingreso de contenedores escaneando su código de identificación,  
**Para** mantener un control exacto y en tiempo real del inventario en la bodega.

**Criterios de Aceptación:**
- [x] **Dado que** estoy en el andén de recepción con la sesión iniciada, **Cuando** ingreso el número de contenedor válido y selecciono 'Ingresar', **Entonces** el sistema actualiza el estado del contenedor a 'En Bodega' y registra la fecha/hora de entrada.
- [x] **Dado que** intento registrar un contenedor, **Cuando** ingreso un código que ya está registrado como 'En Bodega', **Entonces** el sistema rechaza la operación y muestra la alerta 'Contenedor duplicado'.

### RF02: Rastreo de Estadía
**Como** Sistema Automático (Cron Job),  
**Quiero** rastrear y calcular el tiempo que los contenedores llevan en la bodega,  
**Para** identificar contenedores que han superado el tiempo máximo de estadía permitida.

**Criterios de Aceptación:**
- [x] **Dado que** es la hora de corte diario (ej. 23:59), **Cuando** el sistema revisa la lista de contenedores en bodega, **Entonces** marca con bandera 'Retraso' a aquellos que tengan más de 7 días naturales almacenados.
- [x] **Dado que** un contenedor supera el límite de estadía, **Cuando** cambia su estado a 'Retraso', **Entonces** el sistema desencadena el proceso de notificación por correo.

### RF03: Notificación de Retrasos
**Como** Gerente de Logística,  
**Quiero** recibir notificaciones por correo sobre contenedores con retraso,  
**Para** tomar acciones correctivas y liberar espacio en la aduana.

**Criterios de Aceptación:**
- [x] **Dado que** uno o más contenedores entran en estado de 'Retraso', **Cuando** el sistema procesa las notificaciones diarias, **Entonces** recibo un correo electrónico consolidado con la lista de IDs, fechas de ingreso y días de retraso.
- [x] **Dado que** el servidor de correo presenta una caída temporal, **Cuando** el sistema intenta enviar la alerta, **Entonces** el envío se encola y reintenta cada hora hasta que se confirma la entrega exitosa.

---

## 3. Requerimientos No Funcionales

| Categoría | Especificación Técnica |
| :--- | :--- |
| **Seguridad** | El sistema debe integrarse con el Active Directory del puerto para la autenticación y contar con control de acceso basado en roles (RBAC). |
| **Rendimiento** | La búsqueda y actualización de estado de contenedores debe realizarse en menos de 1 segundo para no interrumpir el flujo logístico de los andenes. |
| **Escalabilidad** | El módulo debe ser capaz de procesar el registro simultáneo de hasta 500 contenedores por hora provenientes de diferentes dispositivos móviles. |
| **Base de Datos** | Se requiere que las tablas de rastreo soporten concurrencia alta y utilicen índices optimizados para filtrar por fecha y estado en bases de datos relacionales robustas. |
| **Mantenibilidad** | La lógica de notificación de correos debe ser un microservicio independiente (desacoplado del registro de contenedores) para facilitar su mantenimiento y actualizaciones. |
