#!/usr/bin/env python3
"""Genera GeoUAL.aia para Kodular/App Inventor 2
Fixes aplicados:
  - ensure_ascii=True en JSON (evita problemas con acentos en parser Java)
  - Sin colores &H en SCM (eliminados BackgroundColor/TextColor)
  - project.properties minimo sin theme/color
  - Textos en BKY sin caracteres no-ASCII
  - Uuid "0" en Form y negativos en componentes
  - assets/ directorio incluido
"""

import zipfile, json

OUTPUT = "/Users/antonio/Desktop/negocio-electronico/tr-2/GeoUAL.aia"

# ─── project.properties ────────────────────────────────────────────────────
PROPS = """\
#
#Mon Jan 01 00:00:00 UTC 2026
main=appinventor.ai_user.GeoUAL.Screen1
name=GeoUAL
assets=../assets
source=../src
build=../build
versioncode=1
versionname=1.0
useslocation=true
aname=GeoUAL
"""

# ─── Screen1.scm ─────────────────────────────────────────────────────────────
# IMPORTANTE: ensure_ascii=True para evitar que el parser Java de Kodular falle
# con caracteres Unicode (e, o, n con tildes). Sin &H colores para evitar unquote error.
SCM_DATA = {
    "authURL": ["ai2.appinventor.mit.edu"],
    "YaVersion": "2",
    "Source": "Form",
    "Properties": {
        "$Name": "Screen1",
        "$Type": "Form",
        "$Version": "29",
        "AppName": "GeoUAL",
        "Title": "GeoUAL",
        "Scrollable": "True",
        "Uuid": "0",
        "$Components": [
            {
                "$Name": "lblTitulo", "$Type": "Label", "$Version": "5",
                "FontBold": "True", "FontSize": "18.0",
                "Text": "GeoUAL - Universidad de Almeria",
                "TextAlignment": "1", "Width": "-2", "Uuid": "-101"
            },
            {
                "$Name": "HA1", "$Type": "HorizontalArrangement", "$Version": "3",
                "Width": "-2", "Uuid": "-102",
                "$Components": [
                    {"$Name": "LabelLat0", "$Type": "Label", "$Version": "5",
                     "FontBold": "True", "Text": "Latitud: ", "Uuid": "-103"},
                    {"$Name": "lblLat", "$Type": "Label", "$Version": "5",
                     "Text": "--", "Uuid": "-104"}
                ]
            },
            {
                "$Name": "HA2", "$Type": "HorizontalArrangement", "$Version": "3",
                "Width": "-2", "Uuid": "-105",
                "$Components": [
                    {"$Name": "LabelLon0", "$Type": "Label", "$Version": "5",
                     "FontBold": "True", "Text": "Longitud: ", "Uuid": "-106"},
                    {"$Name": "lblLon", "$Type": "Label", "$Version": "5",
                     "Text": "--", "Uuid": "-107"}
                ]
            },
            {
                "$Name": "btnActualizar", "$Type": "Button", "$Version": "7",
                "Text": "Actualizar GPS", "Width": "-2", "Uuid": "-108"
            },
            {
                "$Name": "txtNombre", "$Type": "TextBox", "$Version": "6",
                "Hint": "Nombre del elemento (ej: Despacho A-123)",
                "Width": "-2", "Uuid": "-109"
            },
            {
                "$Name": "btnGuardar", "$Type": "Button", "$Version": "7",
                "Text": "Guardar Posicion", "Width": "-2", "Uuid": "-110"
            },
            {
                "$Name": "lblListaTitulo", "$Type": "Label", "$Version": "5",
                "FontBold": "True", "Text": "Elementos guardados:", "Uuid": "-111"
            },
            {
                "$Name": "listElementos", "$Type": "ListView", "$Version": "4",
                "Height": "200", "Width": "-2", "Uuid": "-112"
            },
            {
                "$Name": "HA3", "$Type": "HorizontalArrangement", "$Version": "3",
                "Width": "-2", "Uuid": "-113",
                "$Components": [
                    {"$Name": "btnVerMapa", "$Type": "Button", "$Version": "7",
                     "Text": "Ver en Mapa", "Uuid": "-114"},
                    {"$Name": "btnEliminar", "$Type": "Button", "$Version": "7",
                     "Text": "Eliminar", "Uuid": "-115"}
                ]
            },
            {"$Name": "gps",   "$Type": "LocationSensor",  "$Version": "3", "Uuid": "-201"},
            {"$Name": "db",    "$Type": "TinyDB",           "$Version": "2", "Uuid": "-202"},
            {"$Name": "maps",  "$Type": "ActivityStarter",  "$Version": "6", "Uuid": "-203"},
            {"$Name": "notif", "$Type": "Notifier",         "$Version": "5", "Uuid": "-204"},
        ]
    }
}

# ensure_ascii=True -> escapa todo lo no-ASCII como \uXXXX, evita problemas
SCM = "#|\n$JSON\n" + json.dumps(SCM_DATA, ensure_ascii=True) + "\n|#"

# ─── Block helpers ────────────────────────────────────────────────────────────
def txt(t):
    # Reemplazar caracteres no-ASCII en textos de bloques
    t = (t.replace("ó","o").replace("é","e").replace("á","a")
          .replace("í","i").replace("ú","u").replace("ñ","n")
          .replace("Ó","O").replace("É","E").replace("Á","A"))
    return f'<block type="text"><field name="TEXT">{t}</field></block>'

def num(n):
    return f'<block type="math_number"><field name="NUM">{n}</field></block>'

def bool_val(v):
    return f'<block type="logic_boolean"><field name="BOOL">{"TRUE" if v else "FALSE"}</field></block>'

def empty_list():
    return '<block type="lists_create_with"><mutation items="0"></mutation></block>'

def get_var(name):
    return f'<block type="lexical_variable_get"><field name="VAR">{name}</field></block>'

def set_prop(ct, inst, prop, val):
    return (f'<block type="component_set_get">'
            f'<mutation component_type="{ct}" instance_name="{inst}" '
            f'set_or_get="set" property_name="{prop}" is_generic="false"></mutation>'
            f'<field name="COMPONENT_SELECTOR">{inst}</field>'
            f'<value name="VALUE">{val}</value></block>')

def get_prop(ct, inst, prop):
    return (f'<block type="component_set_get">'
            f'<mutation component_type="{ct}" instance_name="{inst}" '
            f'set_or_get="get" property_name="{prop}" is_generic="false"></mutation>'
            f'<field name="COMPONENT_SELECTOR">{inst}</field></block>')

def call_method(ct, inst, method, *args):
    args_xml = "".join(f'<value name="ARG{i}">{a}</value>' for i, a in enumerate(args))
    return (f'<block type="component_method">'
            f'<mutation component_type="{ct}" instance_name="{inst}" '
            f'method_name="{method}" is_generic="false"></mutation>'
            f'<field name="COMPONENT_SELECTOR">{inst}</field>{args_xml}</block>')

def call_proc(name):
    return f'<block type="procedures_callnoreturn"><mutation name="{name}"></mutation></block>'

def alert(msg_xml):
    return call_method("Notifier", "notif", "ShowAlert", msg_xml)

def eq(a, b):
    return (f'<block type="logic_compare"><field name="OP">EQ</field>'
            f'<value name="A">{a}</value><value name="B">{b}</value></block>')

def text_join(*items):
    items_xml = "".join(f'<value name="ADD{i}">{v}</value>' for i, v in enumerate(items))
    return f'<block type="text_join"><mutation items="{len(items)}"></mutation>{items_xml}</block>'

def text_split(text_xml, delim_xml):
    return (f'<block type="text_split"><mutation mode="SPLIT"></mutation>'
            f'<value name="TEXT">{text_xml}</value>'
            f'<value name="AT">{delim_xml}</value></block>')

def list_select(lst, idx):
    return (f'<block type="lists_select_item">'
            f'<value name="LIST">{lst}</value><value name="NUM">{idx}</value></block>')

def add_to_list(lst, item):
    return (f'<block type="lists_add_items"><mutation items="1"></mutation>'
            f'<value name="LIST">{lst}</value><value name="ITEM0">{item}</value></block>')

def remove_from_list(lst, idx):
    return (f'<block type="lists_remove_item">'
            f'<value name="LIST">{lst}</value><value name="INDEX">{idx}</value></block>')

def local_var(name, init, body):
    return (f'<block type="local_declaration_statement">'
            f'<mutation><localname name="{name}"></localname></mutation>'
            f'<value name="DECL0">{init}</value>'
            f'<statement name="STACK">{body}</statement></block>')

def if_else(cond, then, els=None):
    e  = f'<statement name="ELSE">{els}</statement>' if els else ""
    ea = ' else="1"' if els else ""
    return (f'<block type="controls_if"><mutation{ea}></mutation>'
            f'<value name="IF0">{cond}</value>'
            f'<statement name="DO0">{then}</statement>{e}</block>')

def if_elif_else(c1, t1, c2, t2, els):
    return (f'<block type="controls_if"><mutation elseif="1" else="1"></mutation>'
            f'<value name="IF0">{c1}</value><statement name="DO0">{t1}</statement>'
            f'<value name="IF1">{c2}</value><statement name="DO1">{t2}</statement>'
            f'<statement name="ELSE">{els}</statement></block>')

def seq(*blocks):
    """Encadena bloques statement con <next>"""
    blocks = [b for b in blocks if b]
    if not blocks: return ""
    result = blocks[-1]
    for b in reversed(blocks[:-1]):
        p = b.rfind('</block>')
        result = b[:p] + '<next>' + result + '</next>' + b[p:]
    return result

def event(ct, inst, ev, body, x=10, y=10):
    return (f'<block type="component_event" x="{x}" y="{y}">'
            f'<mutation component_type="{ct}" instance_name="{inst}" event_name="{ev}"></mutation>'
            f'<field name="COMPONENT_SELECTOR">{inst}</field>'
            f'<statement name="DO">{body}</statement></block>')

def proc_def(name, body, x=10, y=10):
    return (f'<block type="procedures_defnoreturn" x="{x}" y="{y}">'
            f'<field name="NAME">{name}</field>'
            f'<statement name="STACK">{body}</statement></block>')

# ─── Procedure: CargarLista ──────────────────────────────────────────────────
proc_cargar = proc_def("CargarLista",
    set_prop("ListView", "listElementos", "Elements",
        call_method("TinyDB", "db", "GetValue", txt("elementos"), empty_list())),
    x=1200, y=10)

# ─── Screen1.Initialize ──────────────────────────────────────────────────────
block_init = event("Form", "Screen1", "Initialize",
    seq(set_prop("LocationSensor", "gps", "Enabled", bool_val(True)),
        call_proc("CargarLista")),
    x=10, y=10)

# ─── btnActualizar.Click ─────────────────────────────────────────────────────
block_actualizar = event("Button", "btnActualizar", "Click",
    seq(set_prop("Label", "lblLat", "Text",
            get_prop("LocationSensor", "gps", "Latitude")),
        set_prop("Label", "lblLon", "Text",
            get_prop("LocationSensor", "gps", "Longitude"))),
    x=10, y=180)

# ─── btnGuardar.Click ────────────────────────────────────────────────────────
guardar_inner = seq(
    add_to_list(get_var("lista"), get_var("entrada")),
    call_method("TinyDB", "db", "StoreValue", txt("elementos"), get_var("lista")),
    call_proc("CargarLista"),
    set_prop("TextBox", "txtNombre", "Text", txt("")),
    alert(txt("Guardado correctamente")))

guardar_else = local_var("lista",
    call_method("TinyDB", "db", "GetValue", txt("elementos"), empty_list()),
    local_var("entrada",
        text_join(
            get_prop("TextBox", "txtNombre", "Text"),
            txt("|"),
            get_prop("LocationSensor", "gps", "Latitude"),
            txt(","),
            get_prop("LocationSensor", "gps", "Longitude")),
        guardar_inner))

block_guardar = event("Button", "btnGuardar", "Click",
    if_elif_else(
        eq(get_prop("TextBox", "txtNombre", "Text"), txt("")),
        alert(txt("Introduce un nombre")),
        eq(get_prop("LocationSensor", "gps", "Latitude"), num(0)),
        alert(txt("Esperando GPS...")),
        guardar_else),
    x=10, y=350)

# ─── btnVerMapa.Click ────────────────────────────────────────────────────────
ver_inner = seq(
    set_prop("ActivityStarter", "maps", "Action",
        txt("android.intent.action.VIEW")),
    set_prop("ActivityStarter", "maps", "DataUri",
        text_join(txt("geo:"), get_var("lat"), txt(","), get_var("lon"),
                  txt("?q="), get_var("lat"), txt(","), get_var("lon"),
                  txt("("), get_var("nombre"), txt(")"))),
    call_method("ActivityStarter", "maps", "StartActivity"))

ver_else = local_var("partes",
    text_split(get_prop("ListView", "listElementos", "Selection"), txt("|")),
    local_var("nombre", list_select(get_var("partes"), num(1)),
        local_var("coords",
            text_split(list_select(get_var("partes"), num(2)), txt(",")),
            local_var("lat", list_select(get_var("coords"), num(1)),
                local_var("lon", list_select(get_var("coords"), num(2)),
                    ver_inner)))))

block_ver_mapa = event("Button", "btnVerMapa", "Click",
    if_else(eq(get_prop("ListView", "listElementos", "SelectionIndex"), num(0)),
            alert(txt("Selecciona un elemento")),
            ver_else),
    x=600, y=10)

# ─── btnEliminar.Click ───────────────────────────────────────────────────────
eliminar_else = local_var("lista",
    call_method("TinyDB", "db", "GetValue", txt("elementos"), empty_list()),
    seq(remove_from_list(get_var("lista"),
            get_prop("ListView", "listElementos", "SelectionIndex")),
        call_method("TinyDB", "db", "StoreValue", txt("elementos"), get_var("lista")),
        call_proc("CargarLista"),
        alert(txt("Elemento eliminado"))))

block_eliminar = event("Button", "btnEliminar", "Click",
    if_else(eq(get_prop("ListView", "listElementos", "SelectionIndex"), num(0)),
            alert(txt("Selecciona un elemento")),
            eliminar_else),
    x=600, y=400)

# ─── BKY ─────────────────────────────────────────────────────────────────────
BKY = ('<xml xmlns="http://www.w3.org/1999/xhtml">'
       + proc_cargar + block_init + block_actualizar
       + block_guardar + block_ver_mapa + block_eliminar
       + '</xml>')

# ─── Write .aia ───────────────────────────────────────────────────────────────
with zipfile.ZipFile(OUTPUT, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr("youngandroidproject/project.properties", PROPS)
    z.writestr("assets/", "")
    z.writestr("src/appinventor/ai_user/GeoUAL/Screen1.bky", BKY)
    z.writestr("src/appinventor/ai_user/GeoUAL/Screen1.scm", SCM)

print(f"Creado: {OUTPUT}")

# Verificar
from xml.etree import ElementTree as ET
with zipfile.ZipFile(OUTPUT) as z:
    bky = z.read('src/appinventor/ai_user/GeoUAL/Screen1.bky').decode()
    scm = z.read('src/appinventor/ai_user/GeoUAL/Screen1.scm').decode()
    for f in z.namelist():
        print(f"  {f}")

try:
    ET.fromstring(bky)
    print("BKY XML: OK")
except Exception as e:
    print(f"BKY XML ERROR: {e}")

json_str = scm.split("$JSON\n")[1].split("\n|#")[0]
try:
    json.loads(json_str)
    print("SCM JSON: OK")
    # Verificar no hay caracteres no-ASCII
    json_str.encode('ascii')
    print("SCM ASCII: OK (sin caracteres Unicode)")
except UnicodeEncodeError as e:
    print(f"SCM contiene non-ASCII: {e}")
except Exception as e:
    print(f"SCM JSON ERROR: {e}")
