"""
Prototipo de DLT (Blockchain)
- Operación append para agregar bloques
- Prueba de trabajo simple (Proof of Work) con dificultad de 4 ceros
- Sistema de marca de tiempo (timestamp)
"""

import hashlib
import time
import json


DIFICULTAD = 4  # El hash debe comenzar con 4 ceros: "0000..."
PREFIJO_POW = "0" * DIFICULTAD


class Bloque:
    """Representa un bloque individual en la cadena."""

    def __init__(self, indice: int, datos, hash_previo: str):
        self.indice = indice
        self.marca_tiempo = time.time()  # timestamp UNIX
        self.datos = datos
        self.hash_previo = hash_previo
        self.nonce = 0
        self.hash = self._minar()

    # ------------------------------------------------------------------
    # Cálculo del hash
    # ------------------------------------------------------------------

    def _calcular_hash(self) -> str:
        """Devuelve el SHA-256 del bloque con el nonce actual."""
        contenido = json.dumps({
            "indice": self.indice,
            "marca_tiempo": self.marca_tiempo,
            "datos": self.datos,
            "hash_previo": self.hash_previo,
            "nonce": self.nonce,
        }, sort_keys=True)
        return hashlib.sha256(contenido.encode()).hexdigest()

    # ------------------------------------------------------------------
    # Prueba de trabajo (Proof of Work)
    # ------------------------------------------------------------------

    def _minar(self) -> str:
        """Incrementa el nonce hasta que el hash comience con PREFIJO_POW."""
        print(f"  Minando bloque #{self.indice}...", end=" ", flush=True)
        inicio = time.time()

        hash_candidato = self._calcular_hash()
        while not hash_candidato.startswith(PREFIJO_POW):
            self.nonce += 1
            hash_candidato = self._calcular_hash()

        duracion = time.time() - inicio
        print(f"listo en {duracion:.3f}s  (nonce={self.nonce})")
        return hash_candidato

    # ------------------------------------------------------------------
    # Representación
    # ------------------------------------------------------------------

    def marca_tiempo_legible(self) -> str:
        """Convierte el timestamp UNIX a formato ISO 8601."""
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.marca_tiempo))

    def __repr__(self) -> str:
        return (
            f"Bloque #{self.indice}\n"
            f"  Marca de tiempo : {self.marca_tiempo_legible()}\n"
            f"  Datos           : {self.datos}\n"
            f"  Nonce           : {self.nonce}\n"
            f"  Hash previo     : {self.hash_previo}\n"
            f"  Hash            : {self.hash}\n"
        )


# ----------------------------------------------------------------------

class Blockchain:
    """Cadena de bloques con operación append y validación."""

    def __init__(self):
        self._cadena: list[Bloque] = []
        print("=== Creando bloque génesis ===")
        self._cadena.append(self._crear_genesis())

    # ------------------------------------------------------------------
    # Bloque génesis
    # ------------------------------------------------------------------

    def _crear_genesis(self) -> Bloque:
        """El primer bloque usa hash previo de ceros."""
        return Bloque(
            indice=0,
            datos="Bloque Génesis",
            hash_previo="0" * 64,
        )

    # ------------------------------------------------------------------
    # Operación append
    # ------------------------------------------------------------------

    def append(self, datos) -> Bloque:
        """Agrega un nuevo bloque al final de la cadena."""
        ultimo = self._cadena[-1]
        nuevo = Bloque(
            indice=len(self._cadena),
            datos=datos,
            hash_previo=ultimo.hash,
        )
        self._cadena.append(nuevo)
        return nuevo

    # ------------------------------------------------------------------
    # Validación de la cadena
    # ------------------------------------------------------------------

    def es_valida(self) -> bool:
        """
        Verifica la integridad de toda la cadena:
        1. Cada hash debe cumplir la prueba de trabajo.
        2. Cada hash_previo debe coincidir con el hash del bloque anterior.
        """
        for i in range(1, len(self._cadena)):
            actual = self._cadena[i]
            anterior = self._cadena[i - 1]

            # Re-calcula el hash esperado
            contenido = json.dumps({
                "indice": actual.indice,
                "marca_tiempo": actual.marca_tiempo,
                "datos": actual.datos,
                "hash_previo": actual.hash_previo,
                "nonce": actual.nonce,
            }, sort_keys=True)
            hash_esperado = hashlib.sha256(contenido.encode()).hexdigest()

            if actual.hash != hash_esperado:
                print(f"  ✗ Hash inválido en bloque #{actual.indice}")
                return False
            if not actual.hash.startswith(PREFIJO_POW):
                print(f"  ✗ Prueba de trabajo fallida en bloque #{actual.indice}")
                return False
            if actual.hash_previo != anterior.hash:
                print(f"  ✗ Eslabón roto entre bloque #{i-1} y #{i}")
                return False

        return True

    # ------------------------------------------------------------------
    # Acceso e información
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        return len(self._cadena)

    def __getitem__(self, indice: int) -> Bloque:
        return self._cadena[indice]

    def __iter__(self):
        return iter(self._cadena)

    def imprimir_cadena(self):
        """Muestra todos los bloques de la cadena."""
        print("\n" + "=" * 60)
        print(f"  CADENA DE BLOQUES  ({len(self._cadena)} bloque(s))")
        print("=" * 60)
        for bloque in self._cadena:
            print(bloque)
