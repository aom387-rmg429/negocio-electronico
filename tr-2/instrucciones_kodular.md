# Instrucciones paso a paso — Kodular GeoUAL

## 1. Crear el proyecto en Kodular

1. Ir a https://creator.kodular.io e iniciar sesión.
2. **New Project** → nombre: `GeoUAL`.

---

## 2. Diseño de la interfaz (Designer)

### Componentes a añadir (en orden):

#### Barra superior
- `Label` → Text: `"GeoUAL - Universidad de Almería"`, FontBold: true, FontSize: 18

#### Sección GPS
- `Label` → Text: `"Latitud:"` + `Label` (id: `lblLat`) → Text: `"--"`
- `Label` → Text: `"Longitud:"` + `Label` (id: `lblLon`) → Text: `"--"`
- `Button` (id: `btnActualizar`) → Text: `"Actualizar GPS"`

#### Sección guardar
- `TextBox` (id: `txtNombre`) → Hint: `"Nombre del elemento (ej: Despacho A-123)"`
- `Button` (id: `btnGuardar`) → Text: `"Guardar Posición"`

#### Lista de elementos
- `Label` → Text: `"Elementos guardados:"`
- `ListView` (id: `listElementos`)
- `Button` (id: `btnVerMapa`) → Text: `"Ver en Mapa"`
- `Button` (id: `btnEliminar`) → Text: `"Eliminar seleccionado"`

#### Componentes no visibles
- `LocationSensor` (id: `gps`)
- `TinyDB` (id: `db`)
- `ActivityStarter` (id: `maps`)
- `Notifier` (id: `notif`)

---

## 3. Bloques de programación (Blocks)

### Bloque: Al iniciar la app (Screen1.Initialize)
```
when Screen1.Initialize
  set gps.Enabled = true
  call CargarLista()
```

### Bloque: Actualizar GPS (btnActualizar.Click)
```
when btnActualizar.Click
  set gps.Enabled = true
  set lblLat.Text = gps.Latitude
  set lblLon.Text = gps.Longitude
```

### Bloque: Guardar posición (btnGuardar.Click)
```
when btnGuardar.Click
  if txtNombre.Text = "" then
    call notif.ShowAlert("Introduce un nombre para el elemento")
  else if gps.Latitude = 0 then
    call notif.ShowAlert("Esperando señal GPS...")
  else
    let entrada = join(txtNombre.Text, "|", gps.Latitude, ",", gps.Longitude)
    let lista = db.GetValue("elementos", [])
    add entrada to lista
    call db.StoreValue("elementos", lista)
    call CargarLista()
    set txtNombre.Text = ""
    call notif.ShowAlert("Elemento guardado correctamente")
```

### Procedimiento: CargarLista
```
procedure CargarLista
  let lista = db.GetValue("elementos", [])
  set listElementos.Elements = lista
```

### Bloque: Ver en mapa (btnVerMapa.Click)
```
when btnVerMapa.Click
  if listElementos.SelectionIndex = 0 then
    call notif.ShowAlert("Selecciona un elemento de la lista")
  else
    let partes = split(listElementos.Selection, "|")
    let nombre = select item 1 of partes
    let coords = split(select item 2 of partes, ",")
    let lat = select item 1 of coords
    let lon = select item 2 of coords
    set maps.Action = "android.intent.action.VIEW"
    set maps.DataUri = join("geo:", lat, ",", lon, "?q=", lat, ",", lon, "(", nombre, ")")
    call maps.StartActivity()
```

### Bloque: Eliminar elemento (btnEliminar.Click)
```
when btnEliminar.Click
  if listElementos.SelectionIndex = 0 then
    call notif.ShowAlert("Selecciona un elemento para eliminar")
  else
    let lista = db.GetValue("elementos", [])
    remove item listElementos.SelectionIndex from lista
    call db.StoreValue("elementos", lista)
    call CargarLista()
    call notif.ShowAlert("Elemento eliminado")
```

---

## 4. Exportar el proyecto como .aia

1. En Kodular Creator: **Project → Export project (.aia) to my computer**
2. Guardar el archivo como `GeoUAL.aia` en la carpeta `tr-2/`.

## 5. Generar el APK para instalar en Android

1. En Kodular Creator: **Export → Android App (.apk)**
2. Instalar el `.apk` en el dispositivo Android (permitir fuentes desconocidas).

---

## Permisos necesarios (AndroidManifest)
Kodular los añade automáticamente al usar `LocationSensor`:
- `ACCESS_FINE_LOCATION`
- `ACCESS_COARSE_LOCATION`
