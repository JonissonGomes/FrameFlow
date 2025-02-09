from flask_mail import Message
from flask import current_app
from app import mail

def send_email(recipient, video_filename, status, zip_url=None):
    subject = "Status de Processamento de Vídeo"
    
    message_body = f"""
    Olá, somos da FrameFlow e viemos informar sobre o status do seu vídeo.

    O vídeo "{video_filename}" foi processado.
    Status: 
    {status}

    """
    
    if status == "Concluído" and zip_url:
        message_body += f"Você pode baixar os arquivos extraídos aqui clicando no link abaixo \n\n {zip_url}\n"

    msg = Message(subject, sender=current_app.config['MAIL_DEFAULT_SENDER'], recipients=[recipient])
    msg.body = message_body

    try:
        mail.send(msg)
        current_app.logger.info(f"E-mail enviado com sucesso para {recipient}")
    except Exception as e:
        current_app.logger.error(f"Erro ao enviar e-mail: {str(e)}")
