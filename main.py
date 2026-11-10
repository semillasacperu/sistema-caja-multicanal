# ==========================================
# PUNTO DE ENTRADA PRINCIPAL (main.py)
# ==========================================

import caja
from promociones import crear_gestor_promociones

def mostrar_menu():
    print("\n" + "="*45)
    print("   SISTEMA DE CAJA Y ARQUEO MULTICANAL")
    print("="*45)
    print("1. Registrar Venta Estándar")
    print("2. Registrar Venta con Promoción / Comisión (Nonlocal)")
    print("3. Visualizar Arqueo de Caja Actual")
    print("4. Reiniciar Caja (Apertura de Nuevo Turno)")
    print("5. Salir del Sistema")
    print("="*45)

def ejecutar_sistema():
    # Instanciamos el closure con una comisión simulada del 1.5% para billeteras digitales
    gestor_promos = crear_gestor_promociones(tasa_comision=0.015)
    
    while True:
        mostrar_menu()
        
        # Variable local de selección de menú
        opcion = input("Seleccione una opción (1-5): ").strip()
        
        if opcion == "1":
            print("\n--- REGISTRO DE VENTA ESTÁNDAR ---")
            try:
                # Variables locales efímeras por transacción
                monto_venta = float(input("Ingrese el monto de la venta (S/.): "))
                medio_pago = input("Ingrese el medio de pago (efectivo / yape / plin): ")
                confirmacion = input("¿Confirmar transacción? (s/n): ").strip().lower()
                
                if confirmacion == 's':
                    caja.registrar_venta(monto_venta, medio_pago)
                    print(f"[ÉXITO] Venta de S/. {monto_venta:.2f} registrada correctamente en [{medio_pago.upper()}].")
                else:
                    print("[CANCELADO] La transacción fue anulada por el operador.")
                    
            except ValueError as e:
                print(f"[ERROR DE VALIDACIÓN]: Entrada incorrecta. Verifique los datos ingresados. Detalle: {e}")
                
        elif opcion == "2":
            print("\n--- REGISTRO DE VENTA CON PROMOCIÓN ---")
            try:
                # Variables locales para la transacción promocional
                monto_venta = float(input("Ingrese el monto base de la venta (S/.): "))
                medio_pago = input("Ingrese el medio de pago (efectivo / yape / plin): ").strip()
                
                es_digital = medio_pago.lower() in ["yape", "plin", "digital"]
                
                input_dto = input("¿Aplicar promoción de descuento del 5%? (s/n): ").strip().lower()
                aplicar_descuento = (input_dto == 's')
                
                confirmacion = input("¿Confirmar venta con promoción? (s/n): ").strip().lower()
                
                if confirmacion == 's':
                    # Ejecución de función anidada con alcance nonlocal
                    resultado_promo = gestor_promos(monto_venta, es_digital, aplicar_descuento)
                    monto_final = resultado_promo["monto_final"]
                    
                    # Persistencia en variables globales de caja
                    caja.registrar_venta(monto_final, medio_pago)
                    
                    print("\n--- REPORTE DE TRANSACCIÓN ---")
                    print(f"Monto Base Original      : S/. {monto_venta:.2f}")
                    print(f"Descuento Aplicado       : S/. {resultado_promo['descuento_transaccion']:.2f}")
                    print(f"Comisión Pasarela        : S/. {resultado_promo['comision_transaccion']:.2f}")
                    print(f"Monto Final Cobrado      : S/. {monto_final:.2f}")
                    print(f"[ACUMULADO SESIÓN] Descuentos otorgados: S/. {resultado_promo['descuento_acumulado_sesion']:.2f}")
                    print(f"[ACUMULADO SESIÓN] Comisiones pasarela: S/. {resultado_promo['comision_pasarela_sesion']:.2f}")
                else:
                    print("[CANCELADO] Transacción promocional anulada.")
                    
            except ValueError as e:
                print(f"[ERROR DE VALIDACIÓN]: Entrada no numérica o inválida. Detalle: {e}")
                
        elif opcion == "3":
            # Generación de reporte de arqueo claro y formateado
            arqueo = caja.realizar_arqueo()
            print("\n" + "~"*45)
            print("          REPORTE DE ARQUEO DE CAJA")
            print("~"*45)
            print(f" Total de Operaciones Registradas : {arqueo['contador_operaciones']}")
            print(f" Saldo Físico en Gaveta (Efectivo): S/. {arqueo['total_efectivo']:.2f}")
            print(f" Saldo Digital (Yape / Plin)      : S/. {arqueo['total_digital']:.2f}")
            print(f" TOTAL GENERAL EN CAJA            : S/. {arqueo['total_general']:.2f}")
            print("~"*45)
            
        elif opcion == "4":
            confirmacion = input("¿Está completamente seguro de reiniciar la caja a S/. 0.00? (s/n): ").strip().lower()
            if confirmacion == 's':
                caja.reiniciar_caja()
                print("[REINICIO EXITOSO] La caja ha sido puesta a cero para el nuevo turno.")
            else:
                print("[OPERACIÓN ABORTADA] No se realizaron cambios en la caja.")
                
        elif opcion == "5":
            print("\nCerrando sesión de caja. ¡Hasta pronto!")
            break
        else:
            print("\n[ADVERTENCIA] Opción inválida. Por favor, ingrese un número del 1 al 5.")

if __name__ == "__main__":
    ejecutar_sistema()