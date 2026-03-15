import streamlit as st
from fpdf import FPDF
from datetime import datetime
import io

# --- Configuración de página ---
st.set_page_config(page_title="TramiTRUJILLO - Notas de Venta", page_icon="💰")

# --- Datos fijos ---
EMPRESA = "TramiTRUJILLO"
LEMA = "SIMPLIFICANDO TUS GESTIONES TRIBUTARIAS"
CELULAR = "935534706"
LINK_WA = "https://wa.me/935534706"
DIRECCION = "Psj. Pasaje San Agustín N° 110 - Trujillo"
CORREO = "acarlosa@unitru.edu.pe"

st.title("💰 Sistema de Notas de Venta")
st.markdown(f"**{EMPRESA}** - {LEMA}")

# --- Estado de la aplicación (Para guardar productos temporalmente) ---
if 'productos' not in st.session_state:
    st.session_state.productos = []

# --- Formulario de Datos Generales ---
with st.expander("Datos de la Nota", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        cliente = st.text_input("Cliente:", value="Cliente Varios")
        vendedor = st.text_input("Vendedor:", value="Oficina")
    with col2:
        metodo_pago = st.selectbox("Método de pago:", ["Efectivo", "Transferencia", "Yape/Plin", "Tarjeta"])
        caja = st.text_input("Caja:", value="01")

# --- Formulario de Productos ---
with st.form("agregar_producto"):
    st.markdown("### Agregar Producto")
    c1, c2, c3 = st.columns([3, 1, 1])
    desc = c1.text_input("Descripción del producto")
    cant = c2.number_input("Cant.", min_value=1, value=1)
    prec = c3.number_input("Precio Unit.", min_value=0.0, step=0.1)
    
    if st.form_submit_button("＋ Agregar a la lista"):
        if desc:
            subtotal = cant * prec
            st.session_state.productos.append({
                "desc": desc, "cant": cant, "prec": prec, "subtotal": subtotal
            })
            st.rerun()
        else:
            st.error("Escribe una descripción")

# --- Visualización de la Tabla ---
if st.session_state.productos:
    st.markdown("### Resumen de Venta")
    for i, p in enumerate(st.session_state.productos):
        st.write(f"**{p['cant']}x** {p['desc']} — S/ {p['subtotal']:.2f}")
    
    if st.button("🗑️ Limpiar lista"):
        st.session_state.productos = []
        st.rerun()

    # --- Generación de PDF ---
    def crear_pdf():
        pdf = FPDF('P', 'mm', (120, 250)) # Formato ticket
        pdf.add_page()
        pdf.set_font("Arial", "B", 12)
        
        # Encabezado
        pdf.cell(100, 6, EMPRESA, ln=True, align="C")
        pdf.set_font("Arial", "", 8)
        pdf.cell(100, 4, LEMA, ln=True, align="C")
        pdf.cell(100, 4, DIRECCION, ln=True, align="C")
        pdf.cell(100, 4, f"WhatsApp: {CELULAR}", ln=True, align="C")
        pdf.ln(5)
        
        pdf.set_font("Arial", "B", 10)
        pdf.cell(100, 6, "NOTA DE VENTA ELECTRÓNICA", ln=True, align="C")
        pdf.set_font("Arial", "", 9)
        pdf.cell(100, 5, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
        pdf.cell(100, 5, f"Cliente: {cliente}", ln=True)
        pdf.cell(100, 5, f"Vendedor: {vendedor} | Caja: {caja}", ln=True)
        pdf.ln(2)
        
        # Tabla
        pdf.set_font("Arial", "B", 9)
        pdf.cell(50, 6, "Descripción", border='B')
        pdf.cell(15, 6, "Cant.", border='B', align="R")
        pdf.cell(15, 6, "P.U.", border='B', align="R")
        pdf.cell(20, 6, "Total", border='B', align="R")
        pdf.ln()
        
        pdf.set_font("Arial", "", 9)
        total_final = 0
        for p in st.session_state.productos:
            pdf.cell(50, 6, p['desc'])
            pdf.cell(15, 6, str(p['cant']), align="R")
            pdf.cell(15, 6, f"{p['prec']:.2f}", align="R")
            pdf.cell(20, 6, f"{p['subtotal']:.2f}", align="R")
            pdf.ln()
            total_final += p['subtotal']
        
        pdf.ln(2)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(100, 8, f"TOTAL A PAGAR: S/ {total_final:.2f}", ln=True, align="R")
        pdf.set_font("Arial", "I", 8)
        pdf.cell(100, 5, f"Método de Pago: {metodo_pago}", ln=True, align="R")
        
        pdf.ln(5)
        pdf.set_font("Arial", "", 7)
        pdf.multi_cell(100, 4, "Este documento es una representación interna de venta y no tiene validez legal ante SUNAT.", align="C")
        
        return pdf.output(dest='S').encode('latin-1')

    # Botón de Descarga
    pdf_bytes = crear_pdf()
    st.download_button(
        label="📥 Descargar Nota de Venta (PDF)",
        data=pdf_bytes,
        file_name=f"Nota_{cliente}_{datetime.now().strftime('%H%M')}.pdf",
        mime="application/pdf"
    )
