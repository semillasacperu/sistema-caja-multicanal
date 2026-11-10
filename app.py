# ==========================================
# INTERFAZ WEB CON STREAMLIT (app.py)
# ==========================================

import streamlit as st
import caja
from promociones import crear_gestor_promociones

# Configuración inicial de la página web
st.set_page_config(page_title="Sistema de Caja Multicanal", page_icon="💰", layout="centered")

st.title("💰 Sistema de Caja y Arqueo Multicanal")
st.markdown("Bienvenido al panel web de control para comercio local (Efectivo + Yape / Plin).")

# Menú lateral de navegación
st.sidebar.header("Menú de Opciones")
opcion = st.sidebar.selectbox(
    "Selecciona una acción:",
    ["Registrar Venta", "Ver Arqueo de Caja", "Reiniciar Turno"]
)

# Sección principal según la opción elegida
if opcion == "Registrar Venta":
    st.subheader("🛒 Registro de Transacción")
    
    monto = st.number_input("Monto de la venta (S/.)", min_value=0.0, step=0.50, format="%.2f")
    medio_pago = st.selectbox("Medio de pago", ["Efectivo", "Yape", "Plin"])
    
    if st.button("Registrar Cobro"):
        try:
            caja.registrar_venta(monto, medio_pago)
            st.success(f"¡Venta de S/. {monto:.2f} registrada exitosamente en {medio_pago}!")
        except ValueError as e:
            st.error(f"Error: {e}")

elif opcion == "Ver Arqueo de Caja":
    st.subheader("📊 Reporte de Arqueo en Tiempo Real")
    
    arqueo = caja.realizar_arqueo()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Efectivo en Gaveta", f"S/. {arqueo['total_efectivo']:.2f}")
    col2.metric("Recaudación Digital", f"S/. {arqueo['total_digital']:.2f}")
    col3.metric("Total General", f"S/. {arqueo['total_general']:.2f}")
    
    st.info(f"Cantidad total de operaciones en el turno: **{arqueo['contador_operaciones']}**")

elif opcion == "Reiniciar Turno":
    st.subheader("🔄 Apertura de Nuevo Turno")
    if st.button("Reiniciar Caja a Cero"):
        caja.reiniciar_caja()
        st.warning("La caja ha sido reiniciada correctamente.")