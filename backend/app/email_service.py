from typing import Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .config import settings
from .logger import green_logger

class EmailService:
    """Service for sending emails"""
    
    def __init__(self):
        self.smtp_server = getattr(settings, 'mail_server', 'smtp.gmail.com')
        self.smtp_port = getattr(settings, 'mail_port', 587)
        self.smtp_username = getattr(settings, 'mail_username', None)
        self.smtp_password = getattr(settings, 'mail_password', None)
        self.from_email = getattr(settings, 'mail_from', None)
    
    def send_email(self, to_email: str, subject: str, body: str, html_body: Optional[str] = None) -> bool:
        """Send an email"""
        try:
            if not self.smtp_username or not self.smtp_password:
                # In development, just log the email
                green_logger.logger.info(f"Email would be sent to {to_email}: {subject}")
                green_logger.logger.info(f"Body: {body}")
                return True
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email or self.smtp_username
            msg['To'] = to_email
            
            # Add text and HTML parts
            text_part = MIMEText(body, 'plain')
            msg.attach(text_part)
            
            if html_body:
                html_part = MIMEText(html_body, 'html')
                msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if getattr(settings, 'mail_tls', True):
                    server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            green_logger.logger.info(f"Email sent successfully to {to_email}")
            return True
        except Exception as e:
            green_logger.log_error(e, {"to_email": to_email, "subject": subject})
            return False
    
    def send_verification_email(self, to_email: str, verification_token: str, username: str) -> bool:
        """Send email verification email"""
        frontend = getattr(settings, "frontend_url", "http://localhost:5173").rstrip("/")
        verification_url = f"{frontend}/verify-email?token={verification_token}"
        
        subject = "Verify your Green Coding Advisor account"
        body = f"""
Hello {username},

Thank you for signing up for Green Coding Advisor!

Please verify your email address by clicking the following link:
{verification_url}

If you didn't create an account, please ignore this email.

Best regards,
Green Coding Advisor Team
"""
        html_body = f"""
<html>
<body>
    <h2>Verify your Green Coding Advisor account</h2>
    <p>Hello {username},</p>
    <p>Thank you for signing up for Green Coding Advisor!</p>
    <p>Please verify your email address by clicking the following link:</p>
    <p><a href="{verification_url}">Verify Email</a></p>
    <p>If you didn't create an account, please ignore this email.</p>
    <p>Best regards,<br>Green Coding Advisor Team</p>
</body>
</html>
"""
        return self.send_email(to_email, subject, body, html_body)
    
    def send_password_reset_email(self, to_email: str, reset_token: str, username: str) -> bool:
        """Send password reset email"""
        frontend = getattr(settings, "frontend_url", "http://localhost:5173").rstrip("/")
        reset_url = f"{frontend}/reset-password?token={reset_token}"
        
        subject = "Reset your Green Coding Advisor password"
        body = f"""
Hello {username},

You requested to reset your password for Green Coding Advisor.

Please click the following link to reset your password:
{reset_url}

This link will expire in 1 hour.

If you didn't request a password reset, please ignore this email.

Best regards,
Green Coding Advisor Team
"""
        html_body = f"""
<html>
<body>
    <h2>Reset your password</h2>
    <p>Hello {username},</p>
    <p>You requested to reset your password for Green Coding Advisor.</p>
    <p>Please click the following link to reset your password:</p>
    <p><a href="{reset_url}">Reset Password</a></p>
    <p>This link will expire in 1 hour.</p>
    <p>If you didn't request a password reset, please ignore this email.</p>
    <p>Best regards,<br>Green Coding Advisor Team</p>
</body>
</html>
"""
        return self.send_email(to_email, subject, body, html_body)

    def send_signup_otp_email(self, to_email: str, otp: str, username: str, expiry_minutes: int) -> bool:
        """Send signup OTP email"""
        subject = "Your Green Coding Advisor verification code"
        body = f"""
Hello {username},

Use the following code to verify your account:
{otp}

This code expires in {expiry_minutes} minutes.

If you didn't create an account, please ignore this email.

Best regards,
Green Coding Advisor Team
"""
        html_body = f"""
<html>
<body>
    <h2>Verify your account</h2>
    <p>Hello {username},</p>
    <p>Use the following code to verify your account:</p>
    <p style="font-size:20px;font-weight:bold;letter-spacing:4px;">{otp}</p>
    <p>This code expires in {expiry_minutes} minutes.</p>
    <p>If you didn't create an account, please ignore this email.</p>
    <p>Best regards,<br>Green Coding Advisor Team</p>
</body>
</html>
"""
        return self.send_email(to_email, subject, body, html_body)


email_service = EmailService()

