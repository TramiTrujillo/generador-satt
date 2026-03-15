import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import io
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Generador de Solicitud - SATT", page_icon="📄")

st.title("📄 Generador de Solicitud de Suspensión")
st.markdown("Completa los datos para generar el documento oficial (Texto íntegro).")

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

    submit_button = st.form_submit_button("Generar PDF con Texto Completo")

def generar_pdf(d):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=60, rightMargin=60, topMargin=60, bottomMargin=40)
    
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    style_normal = ParagraphStyle(name="NormalJustify", parent=styles["Normal"], alignment=TA_JUSTIFY, fontSize=11, leading=16)
    style_bold = ParagraphStyle(name="Bold", parent=styles["Normal"], fontSize=11, leading=16, fontName="Helvetica-Bold")
    style_right = ParagraphStyle(name="Right", parent=styles["Normal"], alignment=TA_RIGHT, fontSize=11, leading=16)
    style_center = ParagraphStyle(name="Center", parent=styles["Normal"], alignment=TA_CENTER, fontSize=11, leading=16)
    style_italic_indented = ParagraphStyle(name="ItalicIndented", parent=style_normal, leftIndent=30, fontSize=11, leading=16)

    texto = []

    # CONTENIDO EXACTO AL ORIGINAL
    texto.append(Paragraph(f"<b>Sumilla:</b> Solicitud de suspensión de la ejecución coactiva del expediente {d['expediente']}", style_right))
    texto.append(Spacer(1, 20))
    texto.append(Paragraph("<b>GERENTE DE OPERACIONES SAT - TRUJILLO</b>", style_normal))
    texto.append(Spacer(1, 10))

    texto.append(Paragraph(f"Yo, {d['nombres']}, identificado con DNI N° {d['dni']}, con domicilio procesal en {d['direccion']}, Trujillo, departamento de La Libertad; ante usted me presento y expongo:", style_normal))
    texto.append(Spacer(1, 10))

    texto.append(Paragraph("<b>I. PETITORIO</b>", style_bold))
    texto.append(Paragraph(f"Recurro a su despacho con la finalidad de solicitar la <b>SUSPENSIÓN DE LA EJECUCIÓN COACTIVA</b> del expediente {d['expediente']}, que contiene la papeleta N° {d['n_papeleta']} con código de infracción {d['cod_infraccion']}.", style_normal))
    texto.append(Spacer(1, 10))

    texto.append(Paragraph("<b>II. FUNDAMENTO DE HECHO</b>", style_bold))
    texto.append(Paragraph(f"2.1. Que, se me presume la comisión de la infracción {d['cod_infraccion']}: “{d['concepto']}”, contenida en la papeleta N° {d['n_papeleta']}, con fecha de imposición {d['f_imposicion']}.", style_normal))
    texto.append(Spacer(1, 10))
    texto.append(Paragraph(f"2.2. Que, con fecha {d['f_notificacion']}, la administración tributaria me notifica la resolución de gerencia n° {d['n_resolucion']}-SATT, donde se resuelve imponer la sanción pecuniaria respectiva, y que tras notificada se declara firme la vía administrativa.", style_normal))
    texto.append(Spacer(1, 10))

    texto.append(Paragraph("<b>III. FUNDAMENTACIÓN JURÍDICA</b>", style_bold))
    texto.append(Paragraph("3.1. Que el Artículo 253.- Prescripción de la exigibilidad de las multas impuestas del TUO de la Ley 27444 – Ley del procedimiento administrativo general (D.S. 004-2019-JUS), en su numeral 1.", style_normal))
    texto.append(Spacer(1, 8))

    texto.append(Paragraph("<i>La facultad de la autoridad para exigir por la vía de ejecución forzosa el pago de las multas impuestas por la comisión de una infracción administrativa prescribe en el plazo que establezcan las leyes especiales...</i>", style_italic_indented))
    texto.append(Spacer(1, 8))

    texto.append(Paragraph("<i>a) Que el acto administrativo mediante el cual se impuso la multa, o aquel que puso fin a la vía administrativa, quedó firme.</i>", style_italic_indented))
    texto.append(Spacer(1, 8))

    texto.append(Paragraph(f"A la fecha de presentación de esta solicitud ya han transcurrido más de dos años de haberse declarado firme la vía administrativa desde notificada la Resolución Gerencial n° {d['n_resolucion']}-SATT.", style_normal))
    texto.append(Spacer(1, 5))
    
    texto.append(Paragraph("3.2. Que el artículo segundo del mismo texto normativo establece que “El cómputo del plazo de prescripción se suspende en los siguientes supuestos: [...]”.", style_normal))
    texto.append(Spacer(1, 8))

    texto.append(Paragraph("<i>a) Con la iniciación del procedimiento de ejecución forzosa, conforme a los mecanismos contemplados en el artículo 207, según corresponda. Dicho cómputo debe reanudarse inmediatamente en caso que se configure alguno de los supuestos de suspensión del procedimiento de ejecución forzosa que contemple el ordenamiento vigente y/o se produzca cualquier causal que determine la paralización del procedimiento por más de veinticinco (25) días hábiles.</i>", style_italic_indented))
    texto.append(Spacer(1, 8))

    texto.append(Paragraph("Por tanto, si bien cada notificación de cobranza interrumpe el plazo prescriptorio, este debe reanudarse a los 25 días hábiles.", style_normal))
    texto.append(Paragraph("3.3. Que según la Ley de Procedimiento de Ejecución Coactiva – Ley Nº 26979, Artículo 16, corresponde suspender el procedimiento cuando la deuda esté prescrita.", style_normal))
    texto.append(Spacer(1, 10))

    texto.append(Paragraph("<b>IV. ANEXOS</b>", style_bold))
    texto.append(Paragraph("4.1. Copia de DNI.", style_normal))
    texto.append(Spacer(1, 10))

    texto.append(Paragraph("Por todo lo expuesto, solicito se conceda la presente y se declare fundada en su oportunidad.", style_normal))
    texto.append(Spacer(1, 20))

    texto.append(Paragraph(f"Trujillo, {d['f_solicitud']}", style_right))
    texto.append(Spacer(1, 40))

    texto.append(Paragraph("_________________________________", style_center))
    texto.append(Paragraph(f"{d['nombres']}", style_center))
    texto.append(Paragraph(f"DNI N° {d['dni']}", style_center))

    doc.build(texto)
    buffer.seek(0)
    return buffer

if submit_button:
    if not nombres or not dni:
        st.error("Por favor, completa al menos el nombre y el DNI.")
    else:
        d = {
            "expediente": expediente, "nombres": nombres, "dni": dni, "direccion": direccion,
            "n_papeleta": n_papeleta, "cod_infraccion": cod_infraccion, "concepto": concepto,
            "f_imposicion": f_imposicion, "f_notificacion": f_notificacion, 
            "n_resolucion": n_resolucion, "f_solicitud": f_solicitud
        }
        pdf_resultado = generar_pdf(d)
        st.success("✅ PDF generado correctamente.")
        st.download_button(
            label="⬇️ Descargar Solicitud PDF",
            data=pdf_resultado,
            file_name=f"Solicitud_Suspension_{dni}.pdf",
            mime="application/pdf"
        )
