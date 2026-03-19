//! Prototipo de DLT (Blockchain)
//! - Operación append
//! - Prueba de trabajo (Proof of Work) con dificultad de 4 ceros
//! - Sistema de marca de tiempo (timestamp)

use chrono::{DateTime, Local, TimeZone};
use sha2::{Digest, Sha256};
use std::time::{Instant, SystemTime, UNIX_EPOCH};

const DIFICULTAD: usize = 4;
const PREFIJO_POW: &str = "0000";

// ─────────────────────────────────────────────────────────────────────────────
// Bloque
// ─────────────────────────────────────────────────────────────────────────────

pub struct Bloque {
    pub indice: u64,
    pub marca_tiempo: u64,   // Unix timestamp en segundos
    pub datos: String,
    pub hash_previo: String,
    pub nonce: u64,
    pub hash: String,
}

impl Bloque {
    /// Crea un nuevo bloque y ejecuta la prueba de trabajo.
    pub fn nuevo(indice: u64, datos: String, hash_previo: String) -> Self {
        let marca_tiempo = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .expect("Error de reloj del sistema")
            .as_secs();

        let mut bloque = Bloque {
            indice,
            marca_tiempo,
            datos,
            hash_previo,
            nonce: 0,
            hash: String::new(),
        };

        bloque.hash = bloque.minar();
        bloque
    }

    // ── Cálculo del hash ────────────────────────────────────────────────────

    pub fn calcular_hash(&self) -> String {
        // Serialización ordenada (mismo orden siempre → hash determinista)
        let contenido = format!(
            r#"{{"datos":{},"hash_previo":"{}","indice":{},"marca_tiempo":{},"nonce":{}}}"#,
            serde_json::to_string(&self.datos).unwrap(),
            self.hash_previo,
            self.indice,
            self.marca_tiempo,
            self.nonce,
        );
        let resultado = Sha256::digest(contenido.as_bytes());
        format!("{:x}", resultado)
    }

    // ── Prueba de trabajo (Proof of Work) ───────────────────────────────────

    fn minar(&mut self) -> String {
        print!("  Minando bloque #{}... ", self.indice);
        let inicio = Instant::now();

        loop {
            let hash = self.calcular_hash();
            if hash.starts_with(PREFIJO_POW) {
                println!(
                    "listo en {:.3}s  (nonce={})",
                    inicio.elapsed().as_secs_f64(),
                    self.nonce
                );
                return hash;
            }
            self.nonce += 1;
        }
    }

    // ── Marca de tiempo legible ─────────────────────────────────────────────

    pub fn marca_tiempo_legible(&self) -> String {
        let dt: DateTime<Local> = Local
            .timestamp_opt(self.marca_tiempo as i64, 0)
            .single()
            .unwrap_or_else(|| Local::now());
        dt.format("%Y-%m-%d %H:%M:%S").to_string()
    }
}

impl std::fmt::Display for Bloque {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "Bloque #{}\n  Marca de tiempo : {}\n  Datos           : {}\n  Nonce           : {}\n  Hash previo     : {}\n  Hash            : {}\n",
            self.indice,
            self.marca_tiempo_legible(),
            self.datos,
            self.nonce,
            self.hash_previo,
            self.hash,
        )
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Blockchain
// ─────────────────────────────────────────────────────────────────────────────

pub struct Blockchain {
    cadena: Vec<Bloque>,
}

impl Blockchain {
    /// Crea la cadena y genera el bloque génesis.
    pub fn nueva() -> Self {
        println!("=== Creando bloque génesis ===");
        let genesis = Bloque::nuevo(0, "Bloque Génesis".to_string(), "0".repeat(64));
        Blockchain { cadena: vec![genesis] }
    }

    // ── Operación append ────────────────────────────────────────────────────

    /// Agrega un nuevo bloque al final de la cadena.
    pub fn append(&mut self, datos: String) -> &Bloque {
        let hash_previo = self.cadena.last().unwrap().hash.clone();
        let indice = self.cadena.len() as u64;
        let bloque = Bloque::nuevo(indice, datos, hash_previo);
        self.cadena.push(bloque);
        self.cadena.last().unwrap()
    }

    // ── Validación ──────────────────────────────────────────────────────────

    /// Verifica integridad completa de la cadena.
    pub fn es_valida(&self) -> bool {
        for i in 1..self.cadena.len() {
            let actual = &self.cadena[i];
            let anterior = &self.cadena[i - 1];

            let hash_esperado = actual.calcular_hash();

            if actual.hash != hash_esperado {
                println!("  ✗ Hash inválido en bloque #{}", actual.indice);
                return false;
            }
            if !actual.hash.starts_with(PREFIJO_POW) {
                println!("  ✗ Prueba de trabajo fallida en bloque #{}", actual.indice);
                return false;
            }
            if actual.hash_previo != anterior.hash {
                println!(
                    "  ✗ Eslabón roto entre bloque #{} y #{}",
                    i - 1,
                    i
                );
                return false;
            }
        }
        true
    }

    // ── Acceso ──────────────────────────────────────────────────────────────

    pub fn len(&self) -> usize {
        self.cadena.len()
    }

    pub fn get_mut(&mut self, indice: usize) -> Option<&mut Bloque> {
        self.cadena.get_mut(indice)
    }

    pub fn imprimir_cadena(&self) {
        let linea = "=".repeat(60);
        println!("\n{}", linea);
        println!("  CADENA DE BLOQUES  ({} bloque(s))", self.cadena.len());
        println!("{}", linea);
        for bloque in &self.cadena {
            println!("{}", bloque);
        }
    }
}
