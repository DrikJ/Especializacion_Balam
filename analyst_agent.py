import os
from crewai import Agent, Task, Crew, Process
from pydantic import BaseModel, Field
from typing import List

# Parte 2: Formato de Salida Estructurado (JSON)
class AcceptanceCriterion(BaseModel):
    dado_que: str = Field(description="Contexto o estado inicial (Given)")
    cuando: str = Field(description="Acción que dispara el evento (When)")
    entonces: str = Field(description="Resultado esperado (Then)")

class UserStory(BaseModel):
    rol: str = Field(description="Rol del usuario (Como...)")
    accion: str = Field(description="Acción a realizar (Quiero...)")
    beneficio: str = Field(description="Beneficio o valor esperado (Para...)")
    criterios_aceptacion: List[AcceptanceCriterion] = Field(description="Lista de criterios de aceptación")

class NonFunctionalRequirement(BaseModel):
    categoria: str = Field(description="Categoría (seguridad, rendimiento, escalabilidad, base de datos, mantenibilidad)")
    especificacion: str = Field(description="Detalle del requerimiento no funcional")

class ProductBacklog(BaseModel):
    requerimientos_funcionales: List[UserStory]
    requerimientos_no_funcionales: List[NonFunctionalRequirement]

# Configuración de Gemini
import os
from dotenv import load_dotenv

load_dotenv() # Carga las variables del archivo .env
os.environ["PYTHONIOENCODING"] = "utf-8" # Soluciona el error de codificación de emojis en la terminal de Windows

from crewai import LLM
llm_gemini = LLM(
    model="gemini/gemini-1.5-pro", # Usando el modelo pro de Gemini
    api_key=os.getenv("GEMINI_API_KEY") # Lee la API Key de forma segura desde el .env
)

# Parte 1: Diseño y Calibración del Agente (Balam_Analyst)
balam_analyst = Agent(
    role="Senior Scrum Master & Requirements Analyst",
    goal="Transformar una idea de negocio vaga expresada en lenguaje natural en un Product Backlog formal con historias de usuario, criterios de aceptación y especificaciones técnicas bajo el estándar Scrum, sin dejar espacio para la ambigüedad.",
    backstory=(
        "Eres Balam_Analyst, un Scrum Master Senior con más de 15 años de experiencia en levantamiento "
        "de requerimientos y gestión ágil de proyectos de software. Eres experto en evitar el fracaso de "
        "los proyectos a través de definiciones de requerimientos precisas y exhaustivas. "
        "Tu trabajo exige desglosar sistemas en dos categorías estrictas: "
        "1) Requerimientos Funcionales (RF): Siempre redactados bajo el formato estándar de Historia de Usuario: "
        "'Como [Rol], quiero [Acción], para [Beneficio]'. "
        "Cada RF DEBE incluir de forma obligatoria al menos 2 Criterios de Aceptación claros en formato "
        "'Dado que / Cuando / Entonces' o lista de verificación. "
        "2) Requerimientos No Funcionales (RNF): Especificando seguridad, rendimiento, escalabilidad, "
        "arquitectura de base de datos y mantenibilidad. No toleras la vaguedad, las suposiciones ni la falta de contexto."
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm_gemini
)

def analyze_case(case_id: str, case_description: str):
    # Tarea 1: Generación del archivo JSON (Para el futuro agente Developer)
    task_json = Task(
        description=(
            f"Analiza la siguiente idea de negocio y extrae un product backlog estructurado:\n"
            f"Idea: '{case_description}'\n\n"
            f"Reglas estrictas:\n"
            f"- Debes desglosar los Requerimientos Funcionales en historias de usuario identificando rol, acción y beneficio.\n"
            f"- Genera al menos 2 criterios de aceptación por historia en formato 'Dado que / Cuando / Entonces'.\n"
            f"- Identifica Requerimientos No Funcionales en categorías de seguridad, rendimiento, escalabilidad, base de datos y mantenibilidad."
        ),
        expected_output="Un objeto JSON estructurado representando el Product Backlog completo sin texto adicional, solo el JSON puro.",
        agent=balam_analyst,
        output_json=ProductBacklog,
        output_file=f"outputs_backlog/backlog_{case_id}.json"
    )

    # Tarea 2: Generación del documento Markdown (Para Human-in-the-Loop)
    task_markdown = Task(
        description=(
            f"Utilizando el conocimiento de la tarea anterior para la idea de negocio: '{case_description}', "
            f"redacta un documento profesional en Markdown estructurado para ser presentado al cliente o un desarrollador humano.\n"
            f"El documento debe contener:\n"
            f"1. Título del Proyecto y Resumen.\n"
            f"2. Requerimientos Funcionales: Formato de Historia de Usuario ('Como... Quiero... Para...') y sus Criterios de Aceptación ('Dado que... Cuando... Entonces...').\n"
            f"3. Requerimientos No Funcionales: Clasificados claramente.\n"
            f"Asegúrate de que la presentación sea impecable y fácil de leer."
        ),
        expected_output="Un documento Markdown profesional detallando el Product Backlog completo de manera clara y amigable.",
        agent=balam_analyst,
        output_file=f"outputs_backlog/BACKLOG_{case_id}.md"
    )

    crew = Crew(
        agents=[balam_analyst],
        tasks=[task_json, task_markdown],
        process=Process.sequential,
        verbose=True
    )
    
    print(f"=== Ejecutando Caso {case_id} ===")
    result = crew.kickoff()
    return result

if __name__ == "__main__":
    # Crear directorio para las salidas si no existe
    os.makedirs("outputs_backlog", exist_ok=True)
    
    # Parte 3: Validación con Casos de Uso Reales de Colima
    caso_a = "Quiero un sistema para que una veterinaria local gestione citas de mascotas, historiales médicos y cobros de servicios"
    caso_b = "Necesito un módulo que rastree el ingreso de contenedores en una bodega aduanera del puerto de Manzanillo y notifique retrasos por correo"
    
    # Descomentar para ejecutar (requiere configuración de variables de entorno OPENAI_API_KEY o similares para el LLM)
    analyze_case("A", caso_a)
    analyze_case("B", caso_b)
    
    print("Configuración lista. Ejecuta este script teniendo un proveedor LLM configurado para CrewAI.")
