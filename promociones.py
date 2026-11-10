# ==========================================
# MÓDULO DE PROMOCIONES Y PASARELAS (Nonlocal)
# ==========================================

def crear_gestor_promociones(tasa_comision: float = 0.0):
    """
    Fábrica de funciones que encapsula estados intermedios utilizando 'nonlocal'.
    Permite llevar el control de descuentos y comisiones por pasarela por sesión.
    """
    descuento_acumulado = 0.0
    comision_pasarela = 0.0  # Acumulador intermedio solicitado
    
    def procesar_promocion(monto_base: float, es_digital: bool, aplicar_descuento: bool):
        nonlocal descuento_acumulado, comision_pasarela
        
        monto_actual = monto_base
        descuento_transaccion = 0.0
        
        # Lógica de descuento promocional
        if aplicar_descuento:
            descuento_transaccion = monto_base * 0.05  # 5% de descuento comercial
            descuento_acumulado += descuento_transaccion
            monto_actual -= descuento_transaccion
            
        # Lógica de recargo / comisión por pasarela digital
        comision_transaccion = 0.0
        if es_digital and tasa_comision > 0:
            comision_transaccion = monto_actual * tasa_comision
            comision_pasarela += comision_transaccion
            # Nota: El cliente paga el monto_actual, la comisión reduce el neto recibido digitalmente
            
        return {
            "monto_final": monto_actual,
            "descuento_transaccion": descuento_transaccion,
            "descuento_acumulado_sesion": descuento_acumulado,
            "comision_transaccion": comision_transaccion,
            "comision_pasarela_sesion": comision_pasarela
        }
        
    return procesar_promocion