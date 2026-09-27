# Product Backlog: Sistema de Gestión Veterinaria

## 1. Resumen del Proyecto
Desarrollo de un sistema de información para que una veterinaria local pueda gestionar de manera eficiente las citas de las mascotas, consultar e ingresar notas en sus historiales médicos, y procesar los cobros por los servicios brindados.

---

## 2. Requerimientos Funcionales (Historias de Usuario)

### RF01: Gestión de Citas
**Como** Recepcionista de veterinaria,  
**Quiero** gestionar citas de mascotas (crear, ver, editar, cancelar),  
**Para** organizar el flujo de atención y evitar empalmes en la agenda.

**Criterios de Aceptación:**
- [x] **Dado que** estoy autenticado en el sistema como recepcionista, **Cuando** intento agendar una cita en un horario ya ocupado por otro doctor, **Entonces** el sistema muestra un error indicando 'Horario no disponible' y me impide guardar la cita.
- [x] **Dado que** estoy en el formulario de nueva cita, **Cuando** completo todos los datos requeridos (dueño, mascota, motivo, fecha) y presiono guardar, **Entonces** la cita aparece inmediatamente en el calendario del día.

### RF02: Historial Médico
**Como** Médico Veterinario,  
**Quiero** registrar y consultar el historial médico de las mascotas,  
**Para** dar seguimiento a tratamientos, vacunas y diagnósticos previos.

**Criterios de Aceptación:**
- [x] **Dado que** estoy viendo el perfil de una mascota, **Cuando** agrego una nueva nota de consulta y guardo, **Entonces** la nota se agrega al historial en orden cronológico con la fecha actual y mi firma digital.
- [x] **Dado que** busco una mascota en el sistema, **Cuando** escribo el nombre del dueño o el ID de la mascota, **Entonces** el sistema muestra el expediente completo incluyendo alergias y vacunas aplicadas.

### RF03: Módulo de Cobros
**Como** Administrador,  
**Quiero** generar cobros por servicios y productos veterinarios,  
**Para** llevar el control financiero y emitir comprobantes a los clientes.

**Criterios de Aceptación:**
- [x] **Dado que** estoy en el módulo de cobros, **Cuando** agrego servicios de consulta y vacunas y selecciono 'Procesar Pago', **Entonces** el sistema calcula el total incluyendo impuestos y genera un ticket digital.
- [x] **Dado que** se ha completado un pago exitosamente, **Cuando** reviso el reporte de caja del día, **Entonces** el pago se refleja en el total de ingresos de la fecha actual.

---

## 3. Requerimientos No Funcionales

| Categoría | Especificación Técnica |
| :--- | :--- |
| **Seguridad** | Todas las contraseñas de usuarios deben ser almacenadas utilizando hash (e.g., bcrypt) y la comunicación debe ser mediante HTTPS. |
| **Rendimiento** | El módulo del calendario de citas debe cargar y renderizar en pantalla en menos de 2 segundos, incluso con 500 citas agendadas en el mes. |
| **Escalabilidad** | La arquitectura del backend debe soportar un incremento del 200% de usuarios concurrentes sin degradar el tiempo de respuesta, preparándose para futuras sucursales. |
| **Base de Datos** | Se realizarán respaldos automatizados de la base de datos (historias clínicas y pagos) cada 24 horas en un servidor en la nube seguro. |
| **Mantenibilidad** | El código del backend debe seguir el estándar RESTful, estar documentado con Swagger/OpenAPI y tener una cobertura de pruebas unitarias superior al 70%. |
