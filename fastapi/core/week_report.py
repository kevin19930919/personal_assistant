import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

class WeekReport():

    emailfrom = "kevin_tsai@leadtek.com"
    emailto = "frank_liu@leadtek.com.tw"
    username = "kevin19930919@gmail.com"
    password = "qjhuqjoqsvettkqj"
    
    @classmethod
    def mail_info(cls):
        message = MIMEMultipart()
        message["From"] = cls.emailfrom
        message["To"] = cls.emailto
        message["Subject"] = "weekly_report_kevin_tsai"
        contents = """
        Dear Frank:
            weekly report is in email attachment.

        Best regards,
        kevin tsai
        """
        message.attach(MIMEText(contents))
        return message
    
    @classmethod
    def send_mail(cls,fileToSend):
        msg = cls.mail_info()
    
        ctype, encoding = mimetypes.guess_type(fileToSend)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"

        maintype, subtype = ctype.split("/", 1)


        fp = open(fileToSend, "rb")
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)

        attachment.add_header("Content-Disposition", "attachment", filename=fileToSend.split('/')[-1])
        msg.attach(attachment)
        
        try:
            with smtplib.SMTP_SSL(host="smtp.gmail.com", port="465") as server: 
                print("login mail server........")
                server.login(cls.username,cls.password)
                print('sending mail')
                server.sendmail(cls.emailfrom, cls.emailto, msg.as_string())
                print('sending mail success')
        except Exception as e:
            print(e)