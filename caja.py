# ==========================================
# MÓDULO DE CAJA Y ARQUEO (Ámbito Global)
# ==========================================

# Variables globales del turno
total_efectivo = 0.0
total_digital = 0.0  # Acumulado Yape / Plin
contador_operaciones = 0

def registrar_venta(monto_venta: float, medio_pago: str):
    """
    Registra una transacción actualizando las variables globales del negocio.
    Emplea la instrucción 'global' para modificar el estado persistente del turno.
    """
    global total_efectivo, total_digital, contador_operaciones
    
    if monto_venta <= 0:
        raise ValueError("El monto de la venta debe ser mayor estrictamente a cero.")
        
    medio = medio_pago.strip().lower()
    
    if medio == "efectivo":
        total_efectivo += monto_venta
    elif medio in ["yape", "plin", "digital"]:
        total_digital += monto_venta
    else:
        raise ValueError("Medio de pago no reconocido. Utilice 'efectivo' o 'yape/plin'.")
        
    contador_operaciones += 1

def realizar_arqueo() -> dict:
    """Consolida y devuelve el estado actual del arqueo de caja."""
    global total_efectivo, total_digital, contador_operaciones
    total_general = total_efectivo + total_digital
    
    return {
        "total_efectivo": total_efectivo,
        "total_digital": total_digital,
        "total_general": total_general,
        "contador_operaciones": contador_operaciones
    }

def reiniciar_caja():
    """Reinicia los contadores globales para iniciar un nuevo turno de trabajo."""
    global total_efectivo, total_digital, contador_operaciones
    total_efectivo = 0.0
    total_digital = 0.0
    contador_operaciones = 0