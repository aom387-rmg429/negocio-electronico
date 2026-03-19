mod blockchain;
use blockchain::Blockchain;

fn separador(titulo: &str) {
    let linea = "=".repeat(60);
    if titulo.is_empty() {
        println!("{}", linea);
    } else {
        println!("\n{}\n  {}\n{}", linea, titulo, linea);
    }
}

fn main() {
    // ── 1. Crear la cadena (genera el bloque génesis) ─────────────────────
    separador("DEMO BLOCKCHAIN — Prueba de Trabajo (dificultad 4 ceros)");

    let mut cadena = Blockchain::nueva();

    // ── 2. Agregar bloques con la operación append ────────────────────────
    separador("Agregando bloques con append()");

    let transacciones = vec![
        r#"{"de":"Alice","para":"Bob","monto":50}"#.to_string(),
        r#"{"de":"Bob","para":"Carol","monto":25}"#.to_string(),
        r#"{"de":"Carol","para":"Dave","monto":10}"#.to_string(),
        "Registro: contrato_001 firmado por Alice y Bob".to_string(),
    ];

    for tx in transacciones {
        cadena.append(tx);
    }

    // ── 3. Mostrar la cadena completa ─────────────────────────────────────
    cadena.imprimir_cadena();

    // ── 4. Validar la cadena ──────────────────────────────────────────────
    separador("Validación de la cadena");
    if cadena.es_valida() {
        println!("  ✓ La cadena es VÁLIDA — todos los bloques son íntegros.");
    } else {
        println!("  ✗ La cadena es INVÁLIDA.");
    }

    // ── 5. Simular una manipulación y re-validar ──────────────────────────
    separador("Simulación de manipulación (ataque de integridad)");
    println!("  Modificando los datos del bloque #1...");

    if let Some(bloque) = cadena.get_mut(1) {
        bloque.datos = r#"{"de":"Alice","para":"Eve","monto":9999}"#.to_string();
    }

    if cadena.es_valida() {
        println!("  ✓ La cadena sigue siendo válida (inesperado).");
    } else {
        println!("  ✗ ¡Manipulación detectada! La cadena YA NO ES válida.");
    }

    separador("");
    println!("  Fin de la demo.\n");
}
