# Simulación 2D de Agentes Colaborativos

Simulación discreta en cuadrícula para flotas de robots transportadores con:

* Planificación espacio-tiempo segun necesidades del usuario.
* Prevención de colisiones con reservas de celda y trayectorias.
* Ciclo operativo por robot: ir a destino → descargar → volver a inicio → cargar (tiempos configurables).
* Escalado de velocidad del sistema y configuracion de avance de robots.
* Contadores individuales de descargas y panel de resultados.
* Prevencion de errores por posicion o rutas imposibles.

## Requisitos

* Python 3.10+
* `pygame` 

Instalación rápida:

```bash
python -m pip install pygame
```

## Estructura mínima

```
src/
 ├─ infrastructure/
 │   └─ Simulacion_2D
 │       └ sim2d.py
 └─ index.console.py
```

## Ejecución

Desde la raíz:

```bash
python src/index.console.py
```

Se abrirá una ventana a pantalla completa.

---

## Vista general de la interfaz

* **Panel izquierdo**

  * `Iniciar simulación`: valida configuración y arranca.
  * `Reiniciar`: reinicia la corrida y devuelve robots a posiciones iniciales (conserva configuracion del mapa y robots).
  * `Cerrar`: cierra la aplicación.

* **Zona central**

  * Mapa en cuadrícula.
  * Etiquetas azules: celdas de **inicio** y **destino** por robot.
  * Robots: cuadrados coloreados (colores distintos por robot).
  * Texto superior: `Modo | Tiempo restante | Avance`.

* **Panel derecho (parámetros)**

  * `Tiempo de Descarga (seg)`: tiempo de descarga en destino.
  * `Tiempo de Carga (seg)`: tiempo de carga en inicio.
  * `Tiiempo de Operación (seg)`: duración total de la simulación.
  * `Cantidad de Robots`: cantidad de robots (solo modificable en modo SETUP).
  * `Velocidad Robot (pasos/seg)`: cuadros de avance por segundo
  * `Velocidad de sistema`: factor global que acelera tiempos y el ritmo del simulador.

Cada control tiene botones `−` y `+`. Con **Shift** se aplica un paso mayor.

---

## Mapa y obstáculos

* El mapa viene con obstacuos por defecto.
* Puedes **dibujar obstáculos** con el **botón derecho** del mouse:

  * Clic y arrastrar: agrega obstáculos.
  * `Shift` mientras arrastras: borra obstáculos.
  * No se permite poner obstáculos sobre las celdas de inicio/destino asignadas.

---

## Asignación de robots

* **Seleccionar robot**: teclas `1` a `9` (en modo SETUP).
* **Fijar inicio**: clic izquierdo sobre una celda libre.
* **Fijar destino**: `Shift` + clic izquierdo sobre una celda libre.
* Si **no asignas destino**, por defecto será el **mismo que el inicio**.

Restricciones automáticas:

* La **celda de inicio** de un robot queda reservada para ese robot.
* La **celda de destino** de un robot queda reservada para ese robot.
* Otro robot no puede usar dichas celdas.

---

## Controles rápidos

* **Mouse (zona de mapa)**

  * Clic izquierdo: asigna **inicio** al robot seleccionado.
  * `Shift` + clic izquierdo: asigna **destino**.
  * Botón derecho + arrastrar: **agregar** obstáculos.
  * `Shift` + botón derecho + arrastrar: **borrar** obstáculos.

* **Teclado**

  * `1`–`9`: elegir robot activo (modo SETUP).
  * `S`: iniciar simulación.
  * `Esc`: salir.

* **Botones (panel izquierdo)**

  * Iniciar simulación / Reiniciar / Cerrar.

---

## Lógica de movimiento

* Planificación **A*** en espacio-tiempo con horizonte adaptativo.
* **Reserva de celdas** por tiempo y **bloqueo de aristas inversas** para evitar choques y cruces de frente.
* Al **llegar** al destino/inicio, la celda queda **ocupada estáticamente** mientras dura la descarga/carga, impidiendo que otro robot la use.
* Si algún robot **no encuentra ruta**, aparece un aviso y se vuelve a SETUP.

---

## Velocidades y tiempos

  * Ejemplo: con velocidad de sistema = 10, una descarga de 5 s se completa en ~0.5 s reales y el movimiento también corre 10×.

---

## Resultados

Al completar el tiempo de operación:

* Se muestra un **resumen** con el número de **descargas por robot** y el **total**.
* Tras cerrar el resumen, `Reiniciar` devuelve los robots a sus inicios y conserva el mapa actual.

---

## Flujo recomendado

1. Ajusta parámetros en el panel derecho.
2. Selecciona cantidad de robots (`1`–`9`) y asigna **inicio** (clic).
3. Asigna **destino** (`Shift` + clic).
4. Ajusta tiempos y ejecuta `Iniciar simulación`.
5. Observa el conteo restante y el avance. Ajusta velocidades si lo deseas.
6. Al finalizar, revisa el panel de resultados.
7. `Reiniciar` para otra ejecucion con el mismo mapa.

---

## Consejos y solución de problemas

* **“Sin ruta”**: abre pasillos retirando obstáculos; evita que distintos robots compartan la misma celda de inicio/destino.
* **Ventana pequeña**: la interfaz se escala a tu pantalla. Si tienes múltiples monitores, arrástrala al deseado.

---

## Licencia

Uso académico/demostrativo.
