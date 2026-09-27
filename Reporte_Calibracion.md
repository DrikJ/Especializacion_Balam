# Reporte de Calibración de Prompts - Balam_Analyst

## 1. Ajustes en el Backstory y Goal
Para lograr que el agente `Balam_Analyst` no omitiera detalles cruciales (como los criterios de aceptación y los Requerimientos No Funcionales), se realizaron los siguientes ajustes en su definición dentro de CrewAI:

- **Estructura Estricta (Goal y Backstory)**: Se configuró el `goal` y el `backstory` no solo para darle una personalidad, sino para impartir **instrucciones obligatorias**. Originalmente, un prompt vago como "extrae requerimientos" resultaba en viñetas simples. Al agregar la instrucción: *"Cada RF DEBE incluir de forma obligatoria al menos 2 Criterios de Aceptación claros en formato 'Dado que / Cuando / Entonces'"*, se restringió la libertad del LLM para simplificar el resultado.
- **Definición Explícita de Categorías RNF**: En las primeras iteraciones, el LLM ignoraba áreas como escalabilidad. Se agregó en el `backstory` y en la descripción del `Task` la lista explícita que debe buscar: *"seguridad, rendimiento, escalabilidad, arquitectura de base de datos y mantenibilidad"*. Al listar explícitamente estas cinco áreas, el agente se ve forzado a incluirlas en el JSON.
- **Pydantic Models para JSON**: El mayor ajuste técnico fue usar la clase `BaseModel` de Pydantic con descripciones de campos (usando `Field`). Esto forza al agente, mediante la funcionalidad `output_json` de CrewAI, a completar una estructura de datos estática donde los arreglos de `criterios_aceptacion` y `requerimientos_no_funcionales` no pueden estar vacíos ni tener formatos arbitrarios.

## 2. Ejemplo de "Alucinación" y Corrección mediante el Prompt

**Escenario (Caso A - Veterinaria):**
*Requerimiento Ambiguo Generado (Antes de calibrar):* 
*"El sistema debe ser rápido y guardar citas en la nube."*

*Problema:* 
Este requerimiento era demasiado vago (alucinaba una "nube" no especificada) y mezclaba requerimientos funcionales (guardar citas) con no funcionales (rápido, nube). Además, no tenía Criterios de Aceptación.

*Corrección Aplicada:*
1. Se ajustó la descripción del `Task` exigiendo: *"Debes desglosar los Requerimientos Funcionales en historias de usuario identificando rol, acción y beneficio"*.
2. Se configuraron modelos de Pydantic específicos para dividir las características. 
3. Se añadió la regla: *"No toleras la vaguedad, las suposiciones ni la falta de contexto."* en el backstory.

*Resultado tras la calibración:*
**Requerimiento Funcional (RF):**
- **Como** Recepcionista de la veterinaria.
- **Quiero** agendar una cita para una mascota seleccionando fecha, hora y doctor.
- **Para** mantener un control organizado y evitar empalmes.
- **Criterio de Aceptación 1:** *Dado que* estoy en el módulo de citas, *Cuando* selecciono un horario ya ocupado, *Entonces* el sistema muestra un mensaje de error "Horario no disponible".
- **Criterio de Aceptación 2:** *Dado que* ingreso los datos correctamente, *Cuando* presiono "Guardar", *Entonces* la cita aparece en el calendario principal.

**Requerimiento No Funcional (RNF - Rendimiento):**
- *El calendario principal debe cargar los datos de las citas del mes en menos de 2 segundos con hasta 1000 registros.*
