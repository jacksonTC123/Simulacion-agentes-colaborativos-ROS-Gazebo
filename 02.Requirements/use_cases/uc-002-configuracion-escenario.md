# UC-002: Configurar Escenario de Simulación

## Información Básica
- **Área Temática:** Configuración de Entornos
- **Suceso de Negocio:** Preparación de ambiente para pruebas de algoritmos
- **Índice de Usabilidad:** Satisfacción: 4/5, Importancia: 5/5, Frecuencia: 4/5

## Actores
- **Actor Principal:** Investigador
- **Sistemas Involucrados:** Interfaz Gráfica, Base de Configuraciones

## Visión General
Permite crear y configurar escenarios de simulación definiendo agentes, obstáculos, reglas de interacción y objetivos de colaboración.

## Condiciones Previas
- Usuario autenticado en el sistema
- Módulo de configuración disponible

## Resultado de Terminación
### Satisfactorio
- Escenario configurado y validado
- Configuración guardada persistentemente
- Escenario disponible para simulación

### No Satisfactorio
- Configuración inválida o incompleta
- Error de validación de reglas
- Fallo al guardar configuración

## Descripción del Caso de Uso
### Flujo Principal
1. Investigador selecciona "Nuevo Escenario"
   - Sistema crea escenario vacío
2. Investigador define parámetros globales (tamaño, duración)
   - Sistema valida parámetros en tiempo real
3. Investigador agrega agentes al escenario
   - Sistema muestra agentes en canvas interactivo
4. Investigador configura propiedades de agentes (comportamiento, objetivos)
   - Sistema valida consistencia de configuraciones
5. Investigador agrega obstáculos y elementos del entorno
   - Sistema valida colocación válida
6. Investigador define reglas de interacción y colaboración
   - Sistema verifica reglas consistente
7. Investigador guarda escenario
   - Sistema persiste configuración completa

### Flujos Alternativos
#### Alternativa 1: Editar Escenario Existente
1. Investigador selecciona escenario existente
   - Sistema carga configuración actual
2. Investigador modifica parámetros necesarios
   - Sistema valida cambios
3. Investigador guarda como nueva versión o sobreescribe

## Asociaciones
- **Es requisito para:** UC-001 (Ejecutar Simulación)
- **Utiliza:** UC-004 (Gestionar Agentes)

## Rastreabilidad
- **Requisitos Relacionados:** REQ-002, REQ-003, REQ-007
- **Documentos Asociados:** Manual de Usuario, Especificación de Configuración

## Resumen de Entrada
- Parámetros de escenario
- Configuración de agentes
- Definición de obstáculos
- Reglas de interacción

## Resumen de Salida
- Configuración de escenario validada
- Archivo de configuración persistido
- Metadata del escenario

## Notas
- Debe soportar importación/exportación de configuraciones
- Validación en tiempo real durante configuración
- Interface drag-and-drop para colocación de elementos