from flask import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from werkzeug.exceptions import BadRequest
name = None
subject = None
email = None
message = None


app = Flask(__name__)


@app.route('/contact/', methods=['get'])
def contact():
    f = open('data.log', 'a')
    try:
        name = str(request.args['name'])
        subject = str(request.args['subject'])
        email = str(request.args['email'])
        message = str(request.args['msg'])
        f.write(
            f"name: \"{name}\"\nsubject: \"{subject}\"\nemail: \"{email}\"\nmessage: \"{message}\"\n")
        sendMail(name, email, subject, message)
        return jsonify(
            {
                "status": "success",
                "name": name,
                "email": email,
                "message": message
            }
        )

    except BadRequest:
        e = BadRequest("you must provide name, email, subject and message")
        raise e

    except Exception:
        pass


def sendMail(name, email, subject, message):
    p = open("secret.txt", "r+")
    senderAddress = str(p.readlines()[0])
    p.seek(0)
    senderPass = str(p.readlines()[1])
    p.seek(0)
    recieverAddress = str(p.readlines()[2])
    mailContent = f'''
        hey,
        {name} tried to contact you through your website
        {name}\'s email: {email}
        message: {message}
        Thank you,
        your bot
    '''
    message = MIMEMultipart()
    message['To'] = recieverAddress
    message['From'] = senderAddress
    message['Subject'] = subject
    message.attach(MIMEText(mailContent, 'plain'))
    session = smtplib.SMTP("smtp.gmail.com", 587)
    session.ehlo()
    session.starttls()
    session.login(senderAddress, senderPass)
    msg = message.as_string()
    session.sendmail(senderAddress, recieverAddress, msg)
    session.close()
    print("mailsent")
    return "mail sent"


if __name__ == "__main__":
    # sendMail("me", "email", "subject", "message")
    app.run(debug=True)
