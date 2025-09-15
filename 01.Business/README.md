# Documento de Visión – Plataforma de Simulación de Agentes Colaborativos  

**Versión:** 1.1  
**Fecha:** 2025-09-14  

---

## Propósito  
Este documento establece la visión del proyecto **Plataforma de Simulación de Agentes Colaborativos**, que servirá como guía de alto nivel para el Product Owner, el Development Team y los Stakeholders.  
Su objetivo es alinear expectativas, definir alcance inicial, identificar riesgos y orientar la construcción del **Product Backlog** en Scrum.  

---

## Alcance  
El producto será una **plataforma web** que permitirá simular sistemas multi-agente en entornos 2D/3D con soporte para:  
- Agentes colaborativos.  
- Interfaz web intuitiva y accesible.  
- Integración con **ROS 2**.  
- Panel de métricas y análisis.  
- Escenarios preconfigurados para docencia e investigación.  

**No incluido en el MVP:**  
- Integración avanzada con hardware físico.  
- Funcionalidades móviles.  
- Colaboración multiusuario en tiempo real.  

---

## Stakeholders principales  
- **Académicos** → validación rigurosa, exportación de métricas.  
- **Estudiantes** → entornos simples y preconfigurados.  
- **Startups** → prototipado rápido y económico.  
- **Equipo de desarrollo** → mantenimiento y evolución de la plataforma.  

---

## Épicas de alto nivel (Product Backlog)  
1. Simulación en tiempo real con múltiples agentes.  
2. Configuración de escenarios vía interfaz web.  
3. Integración con **ROS 2**.  
4. Panel de métricas de colaboración y rendimiento.  
5. Librerías de algoritmos colaborativos base.  

---

## Supuestos y dependencias  
- Usuarios con conexión estable a internet.  
- Compatibilidad con **ROS 2 Humble** o superior.  
- Navegadores con soporte **WebGL/WebAssembly**.  
- Dependencias: Three.js, WebAssembly, hosting en la nube.  

---

## Restricciones  
- Hasta **100 agentes por simulación** en el MVP.  
- Tiempo de respuesta de la interfaz: **<100 ms**.  
- Cumplimiento de **WCAG 2.1** (accesibilidad).  

---

## Criterios de éxito  
- **Funcionales:**  
  - Simulaciones en tiempo real con ≥20 agentes.  
  - Exportación de métricas clave (tiempo de convergencia, eficiencia colaborativa).  
  - Ejecución de un algoritmo de ROS dentro de la simulación.  

- **De negocio:**  
  - 3 universidades piloto usando la plataforma en 6 meses.  
  - ≥80% de feedback positivo en encuestas de usabilidad.  
  - Reducción de ≥50% en costos frente a hardware físico.  

---

## Trazabilidad ágil  
- La visión se descompone en **épicas** → historias de usuario → backlog priorizado.  
- La validación se realizará en **Sprint Reviews** con los stakeholders.  

---

## Validación y aprobación  
- Revisión inicial por el Product Owner.  
- Actualización iterativa durante los Sprints.  
- Aprobación en Sprint Reviews si los stakeholders confirman alineación con las metas.  

---
