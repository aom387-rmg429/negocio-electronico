# TR-2: App de Geoposicionamiento UAL (Kodular)

## Descripción
Aplicación Android desarrollada con **Kodular** que permite geoposicionar elementos urbanísticos o despachos de la Universidad de Almería (UAL), asociándoles un nombre y su posición GPS.

## Funcionalidades
- Capturar la posición GPS actual del dispositivo.
- Asignar un nombre descriptivo al elemento (edificio, despacho, punto de interés, etc.).
- Guardar la localización con su nombre en una lista persistente.
- Visualizar todos los elementos guardados con sus coordenadas.
- Mostrar los elementos en un mapa interactivo (Google Maps).
- Eliminar elementos de la lista.

## Componentes Kodular utilizados

| Componente | Uso |
|---|---|
| `LocationSensor` | Obtener latitud/longitud del GPS |
| `TinyDB` | Almacenamiento local persistente |
| `ListView` | Mostrar la lista de elementos guardados |
| `TextBox` | Introducir el nombre del elemento |
| `Button` | Guardar, ver mapa, eliminar |
| `ActivityStarter` | Abrir Google Maps con las coordenadas |
| `Label` | Mostrar coordenadas en pantalla |
| `Notifier` | Confirmaciones y alertas al usuario |

## Cómo importar el proyecto en Kodular

1. Acceder a [https://creator.kodular.io](https://creator.kodular.io)
2. Iniciar sesión o crear una cuenta.
3. En la pantalla principal, pulsar **Import project (.aia) from computer**.
4. Seleccionar el archivo `GeoUAL.aia` incluido en esta carpeta.
5. El proyecto se cargará con todos los bloques y pantallas configurados.

## Estructura del archivo .aia

```
GeoUAL.aia
├── Screen1 (Pantalla principal)
│   ├── Componentes visuales (UI)
│   └── Bloques de programación
└── assets/
    └── (recursos de la app)
```

## Lógica principal (bloques)

### Guardar elemento
1. El usuario escribe el nombre en el TextBox.
2. Pulsa "Guardar Posición".
3. `LocationSensor` captura lat/lon actuales.
4. Se construye una cadena `"Nombre|lat,lon"` y se añade a `TinyDB`.
5. Se actualiza el `ListView`.

### Ver en mapa
1. El usuario selecciona un elemento del ListView.
2. Se extrae la latitud y longitud.
3. `ActivityStarter` lanza Google Maps con `geo:lat,lon?q=lat,lon(Nombre)`.

### Eliminar elemento
1. El usuario selecciona un elemento.
2. Se elimina de `TinyDB` y se refresca el ListView.

## Requisitos
- Android 5.0 o superior.
- Permiso de ubicación activado.
- Google Maps instalado (para la visualización en mapa).
