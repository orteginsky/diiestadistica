from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import smtplib
import os

from diiestadistica.core.logging_config import setup_logger
from diiestadistica.core.settings import settings

logger = setup_logger(__name__)

def enviar_correo(ruta_carpeta: str, destinatario: str = settings.email_destinatario):
    ruta_archivo = os.path.normpath(os.path.join(ruta_carpeta,"informes.zip"))
    ruta_tabla = os.path.normpath(os.path.join(ruta_carpeta,"mapre.xlsx"))
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_firma = os.path.join(ruta_actual, "firma.html")

    nombre_hoja = 'Matricula Global'
    dataframe = pd.read_excel(ruta_tabla, sheet_name=nombre_hoja)

    dataframe[["Hombres", "Mujeres", "Total"]] = dataframe[["Hombres", "Mujeres", "Total"]].map(
        lambda x: f"{x:,}".replace(",", " ")
    )

    html_tabla = dataframe.to_html(index=False, escape=False, border=1, justify='center')
    html_tabla = html_tabla.replace("<thead>", '<thead style="background-color: #5A1236; color: white;">')

    with open(ruta_firma, "r", encoding="utf-8") as f:
        firma_html = f.read()

    mensaje_principal = """
    <p>Estimado/a,</p>
    <p>Le compartimos los archivos correspondientes. Favor de NO responder a este correo .</p>
    <p>A continuación, se muestra la tabla de matrícula preliminar:</p>
    """

    asunto = "Matricula Preeliminar"
    cuerpo = "Hola"

    mensaje = MIMEMultipart()
    mensaje["From"] = settings.email_remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto
    mensaje.attach(MIMEText(cuerpo, "plain"))

    html_final = mensaje_principal + html_tabla + firma_html
    parte_html = MIMEText(html_final, "html")
    mensaje.attach(parte_html)

    _, nombre_archivo = os.path.split(ruta_archivo)
    with open(ruta_archivo, "rb") as f:
        adjunto = MIMEApplication(f.read(), Name=nombre_archivo)
        adjunto['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
        mensaje.attach(adjunto)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
        servidor.login(settings.email_remitente, settings.email_password)
        servidor.sendmail(mensaje["From"], mensaje["To"], mensaje.as_string())

    logger.info("Correo enviado correctamente.")
