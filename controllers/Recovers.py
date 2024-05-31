import os
import random
import string
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from models.user import UserModel
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    create_refresh_token,
    get_jwt,
)

recovery_codes = {}

class SendRecoverEmail(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "email", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "mode", type=str, required=True, help="This field cannot be blank."
    )

    def post(self):
        data = SendRecoverEmail.parser.parse_args()
        email = data["email"]
        mode = data["mode"]

        if not UserModel.is_valid_email(email):
            return {"message": "Invalid email format"}, 400

        existing_user = UserModel.query.filter_by(
            email=email, is_active=True
        ).one_or_none()
        if existing_user is None:
            return {"message": "A user with that email does not exist"}, 400

        # Generar un código de recuperación aleatorio
        recovery_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        recovery_codes[email] = {
            'code': recovery_code,
            'expiration': datetime.datetime.now() + datetime.timedelta(minutes=15)
        }

        # Enviar el correo de recuperación
        if mode == "1":
            subject = "Recuperación de contraseña"
            content = f'Su código de recuperación es: {recovery_code}. Este código expirará en 15 minutos.'
        elif mode == "2":
            subject = "Recuperación de token 2fa"
            content = f'Su código de recuperación es: {recovery_code}. Este código expirará en 15 minutos.'
        
        try:
            # Enviar el correo electrónico usando smtplib
            self.send_email(email, subject, content)
            return {'message': 'Recovery email sent successfully', 'email': email}, 200
        except Exception as e:
            print(e)
            return {'message': 'An error occurred sending the email'}, 500
        
    def send_email(self, to_email, subject, content):
        from_email = os.getenv('EMAIL_USER')
        password = os.getenv('EMAIL_PASS')
        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port = os.getenv('SMTP_PORT')

        # Crear el mensaje
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(content, 'plain'))

        # Conectar al servidor SMTP y enviar el correo
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)
        server.quit()

class VerifyRecoveryCode(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "email", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "recoverCode", type=str, required=True, help="This field cannot be blank."
    )

    def post(self):
        data = VerifyRecoveryCode.parser.parse_args()
        email = data['email']
        recover_code = data['recoverCode']

        # Verificar si el correo existe en los códigos de recuperación
        if email not in recovery_codes:
            return {"message": "Invalid recovery code or email"}, 400

        recovery_data = recovery_codes[email]

        # Verificar si el código es correcto y no ha expirado
        if recovery_data['code'] != recover_code:
            return {"message": "Invalid recovery code"}, 400

        if datetime.datetime.now() > recovery_data['expiration']:
            return {"message": "Recovery code has expired"}, 400

        return {"message": "Recovery code is valid"}, 200


class Recover2FA(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=False, help="This field cannot be blank."
    )
    parser.add_argument(
        "email", type=str, required=False, help="This field cannot be blank."
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be blank."
    )

    def post(self):
        data = Recover2FA.parser.parse_args()
        email = data["email"]
        name = data["name"]
        password = data["password"]



        if not email and not name:
            return {"message": "Invalid credentials"}, 401

        user_email = UserModel.query.filter_by(
            email=email, is_active=True
        ).one_or_none()
        user_name = UserModel.query.filter_by(name=name, is_active=True).one_or_none()

        if user_email is None and user_name is None:
            return {"message": "Invalid credentials"}, 401

        user = user_email if user_email is not None else user_name
        if not user or not user.check_password(password):
            return {"message": "Invalid credentials"}, 401

        access_token = create_access_token(identity=user.json())
        refresh_token = create_refresh_token(identity=user.json())
        return {
            "user": user.json(),
            "access_token": access_token,
            "refresh_token": refresh_token,
        }, 200
    
