import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import io
from datetime import datetime

# Configuración de la página de Streamlit
st.set_page_config(page_title="Generador de Solicitud - SATT", page_icon="📄")

st.title("📄 Generador de Solicitud de Suspensión")
st.markdown("Completa los datos para generar tu documento en PDF.")

# ====== FORMULARIO DE ENTRADA ======
with st.form("datos_solicitud"):
    col1, col2 = st.columns(2)
    
    with col1:
        expediente = st.text_input("Número de expediente coactivo")
        nombres = st.text_input("Apellidos y nombres")
        dni = st.text_input("Número de DNI")
        direccion = st.text_input("Dirección")
        n_papeleta = st.text_input("Número de papeleta")
        cod_infraccion = st.text_input("Código de infracción")

    with col2:
        concepto = st.text_input("Concepto de papeleta")
        f_imposicion = st.text_input("Fecha de imposición")
        f_notificacion = st.text_input("Fecha de notificación de resolución")
        n_resolucion = st.text_input("Número de resolución de multa")
        f_solicitud = st.text_input("Fecha de solicitud", value=datetime.now().strftime("%d/%m/%Y"))

    submit_button = st.form_submit_button("Generar PDF")

# ====== LÓGICA DE GENERACIÓN DE PDF ======
def generar_pdf(datos):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=60, rightMargin=60, topMargin=60, bottomMargin=40)
    
    styles = getSampleStyleSheet()
    style_normal = ParagraphStyle(name="NormalJustify", parent=styles["Normal"], alignment=TA_JUSTIFY, fontSize=11, leading=16)
    style_bold = ParagraphStyle(name="Bold", parent=styles["Normal"], fontSize=11, leading=16, fontName="Helvetica-Bold")
    style_right = ParagraphStyle(name="Right", parent=styles["Normal"], alignment=TA_RIGHT, fontSize=11, leading=16)
    style_center = ParagraphStyle(name="Center", parent=styles["Normal"], alignment=TA_CENTER, fontSize=11, leading=16)

    texto = []
    # Contenido (Misma lógica que tu script original)
    texto.append(Paragraph(f"<b>Sumilla:</b> Solicitud de suspensión de la ejecución coactiva del expediente {datos['expediente']}", style_right))
    texto.append(Spacer(1, 20))
    texto.append(Paragraph("<b>GERENTE DE OPERACIONES SAT - TRUJILLO</b>", style_normal))
    texto.append(Spacer(1, 10))
    texto.append(Paragraph(f"Yo, {datos['nombres']}, identificado con DNI N° {datos['dni']}, con domicilio procesal en {datos['direccion']}, Trujillo, departamento de La Libertad; ante usted me presento y expongo:", style_normal))
    texto.append(Spacer(1, 10))
    
    texto.append(Paragraph("<b>I. PETITORIO</b>", style_bold))
    texto.append(Paragraph(f"Recurro a su despacho con la finalidad de solicitar la <b>SUSPENSIÓN DE LA EJECUCIÓN COACTIVA</b> del expediente {datos['expediente']}, que contiene la papeleta N° {datos['n_papeleta']} con código de infracción {datos['cod_infraccion']}.", style_normal))
    texto.append(Spacer(1, 10))

    texto.append(Paragraph("<b>II. FUNDAMENTO DE HECHO</b>", style_bold))
    texto.append(Paragraph(f"2.1. Que, se me presume la comisión de la infracción {datos['cod_infraccion']}: “{datos['concepto']}”, contenida en la papeleta N° {datos['n_papeleta']}, con fecha de imposición {datos['f_imposicion']}.", style_normal))
    texto.append(Spacer(1, 10))
    texto.append(Paragraph(f"2.2. Que, con fecha {datos['f_notificacion']}, la administración tributaria me notifica la resolución de gerencia n° {datos['n_resolucion']}-SATT, donde se resuelve imponer la sanción pecuniaria respectiva, y que tras notificada se declara firme la vía administrativa.", style_normal))
    texto.append(Spacer(1, 10))

    texto.append(Paragraph("<b>III. FUNDAMENTACIÓN JURÍDICA</b>", style_bold))
    texto.append(Paragraph("3.1. Que el Artículo 253.- Prescripción de la exigibilidad de las multas impuestas del TUO de la Ley 27444...", style_normal))
    texto.append(Spacer(1, 10))
    
    # ... (Aquí puedes completar el resto de párrafos de tu script original siguiendo este formato)
    
    texto.append(Paragraph(f"Trujillo, {datos['f_solicitud']}", style_right))
    texto.append(Spacer(1, 40))
    texto.append(Paragraph("_________________________________", style_center))
    texto.append(Paragraph(f"{datos['nombres']}", style_center))
    texto.append(Paragraph(f"DNI N° {datos['dni']}", style_center))

    doc.build(texto)
    buffer.seek(0)
    return buffer

if submit_button:
    if not nombres or not dni:
        st.error("Por favor, completa al menos el nombre y el DNI.")
    else:
        datos = {
            "expediente": expediente, "nombres": nombres, "dni": dni, "direccion": direccion,
            "n_papeleta": n_papeleta, "cod_infraccion": cod_infraccion, "concepto": concepto,
            "f_imposicion": f_imposicion, "f_notificacion": f_notificacion, 
            "n_resolucion": n_resolucion, "f_solicitud": f_solicitud
        }
        pdf_resultado = generar_pdf(datos)
        
        st.success("✅ PDF generado con éxito")
        st.download_button(
            label="⬇️ Descargar Solicitud PDF",
            data=pdf_resultado,
            file_name=f"Solicitud_{dni}.pdf",
            mime="application/pdf"
        )
