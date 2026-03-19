"""
Demo del prototipo de DLT (Blockchain)
Muestra: append, prueba de trabajo y marcas de tiempo.
"""

from blockchain import Blockchain


def separador(titulo: str = ""):
    linea = "=" * 60
    if titulo:
        print(f"\n{linea}\n  {titulo}\n{linea}")
    else:
        print(linea)


# ----------------------------------------------------------------------
# 1. Crear la cadena (genera el bloque génesis automáticamente)
# ----------------------------------------------------------------------
separador("DEMO BLOCKCHAIN — Prueba de Trabajo (dificultad 4 ceros)")

cadena = Blockchain()

# ----------------------------------------------------------------------
# 2. Agregar bloques con la operación append
# ----------------------------------------------------------------------
separador("Agregando bloques con append()")

transacciones = [
    {"de": "Alice", "para": "Bob",   "monto": 50},
    {"de": "Bob",   "para": "Carol", "monto": 25},
    {"de": "Carol", "para": "Dave",  "monto": 10},
    "Registro: contrato_001 firmado por Alice y Bob",
]

for tx in transacciones:
    cadena.append(tx)

# ----------------------------------------------------------------------
# 3. Mostrar la cadena completa
# ----------------------------------------------------------------------
cadena.imprimir_cadena()

# ----------------------------------------------------------------------
# 4. Validar la cadena
# ----------------------------------------------------------------------
separador("Validación de la cadena")
if cadena.es_valida():
    print("  ✓ La cadena es VÁLIDA — todos los bloques son íntegros.")
else:
    print("  ✗ La cadena es INVÁLIDA.")

# ----------------------------------------------------------------------
# 5. Simular una manipulación y re-validar
# ----------------------------------------------------------------------
separador("Simulación de manipulación (ataque de integridad)")

print("  Modificando los datos del bloque #1...")
cadena[1].datos = {"de": "Alice", "para": "Eve", "monto": 9999}  # datos alterados

if cadena.es_valida():
    print("  ✓ La cadena sigue siendo válida (inesperado).")
else:
    print("  ✗ ¡Manipulación detectada! La cadena YA NO ES válida.")

separador()
print("  Fin de la demo.\n")
