import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

class EmailService:
    """Email service using SendGrid"""

    def __init__(self, api_key=None, from_email=None):
        self._api_key = api_key or os.environ.get('SENDGRID_API_KEY')
        self._from_email = from_email or os.environ.get('SENDGRID_FROM_EMAIL', 'noreply@studybuddy.edu')

        if not self._api_key:
            raise ValueError("SendGrid API key is required. Set SENDGRID_API_KEY environment variable.")

        self._client = SendGridAPIClient(self._api_key)

    def send_password_reset_email(self, to_email, reset_token, base_url='http://127.0.0.1:5000'):
        """Send password reset email with reset link"""
        reset_link = f"{base_url}/reset_password.html?token={reset_token}"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .container {{
                    background-color: #f9f9f9;
                    border-radius: 10px;
                    padding: 30px;
                    border: 1px solid #ddd;
                }}
                .header {{
                    text-align: center;
                    color: #4CAF50;
                    margin-bottom: 20px;
                }}
                .button {{
                    display: inline-block;
                    padding: 12px 30px;
                    background-color: #4CAF50;
                    color: white !important;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 20px 0;
                    font-weight: bold;
                }}
                .footer {{
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    font-size: 12px;
                    color: #666;
                }}
                .warning {{
                    background-color: #fff3cd;
                    border: 1px solid #ffc107;
                    padding: 10px;
                    border-radius: 5px;
                    margin: 15px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="header">Study Buddy Password Reset</h1>
                <p>Hello,</p>
                <p>We received a request to reset your password for your Study Buddy account. If you didn't make this request, you can safely ignore this email.</p>
                <p>To reset your password, click the button below:</p>
                <div style="text-align: center;">
                    <a href="{reset_link}" class="button">Reset Password</a>
                </div>
                <p>Or copy and paste this link into your browser:</p>
                <p style="word-break: break-all; background-color: #f0f0f0; padding: 10px; border-radius: 3px;">
                    {reset_link}
                </p>
                <div class="warning">
                    <strong>Security Notice:</strong> This link will expire in 30 minutes for security reasons.
                </div>
                <div class="footer">
                    <p>If you didn't request a password reset, please ignore this email or contact support if you have concerns.</p>
                    <p>This is an automated email. Please do not reply to this message.</p>
                    <p>&copy; 2025 Study Buddy. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        plain_content = f"""
        Study Buddy Password Reset

        Hello,

        We received a request to reset your password for your Study Buddy account.

        To reset your password, copy and paste the following link into your browser:
        {reset_link}

        This link will expire in 30 minutes for security reasons.

        If you didn't request a password reset, you can safely ignore this email.

        - Study Buddy Team
        """

        try:
            message = Mail(
                from_email=Email(self._from_email),
                to_emails=To(to_email),
                subject='Study Buddy - Password Reset Request',
                plain_text_content=Content("text/plain", plain_content),
                html_content=Content("text/html", html_content)
            )

            response = self._client.send(message)
            return response.status_code in [200, 201, 202]
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            raise ValueError(f"Failed to send password reset email: {str(e)}")

    def send_password_reset_confirmation(self, to_email):
        """Send confirmation email after successful password reset"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }
                .container {
                    background-color: #f9f9f9;
                    border-radius: 10px;
                    padding: 30px;
                    border: 1px solid #ddd;
                }
                .header {
                    text-align: center;
                    color: #4CAF50;
                    margin-bottom: 20px;
                }
                .success {
                    background-color: #d4edda;
                    border: 1px solid #c3e6cb;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 15px 0;
                    text-align: center;
                }
                .footer {
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    font-size: 12px;
                    color: #666;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="header">Password Successfully Reset</h1>
                <div class="success">
                    <p><strong>Your password has been successfully changed.</strong></p>
                </div>
                <p>This email confirms that your Study Buddy account password was recently reset.</p>
                <p>If you made this change, no further action is needed.</p>
                <p>If you did NOT request this password reset, please contact our support team immediately as your account may have been compromised.</p>
                <div class="footer">
                    <p>This is an automated email. Please do not reply to this message.</p>
                    <p>&copy; 2025 Study Buddy. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        plain_content = """
        Password Successfully Reset

        Your Study Buddy account password has been successfully changed.

        If you made this change, no further action is needed.

        If you did NOT request this password reset, please contact our support team immediately.

        - Study Buddy Team
        """

        try:
            message = Mail(
                from_email=Email(self._from_email),
                to_emails=To(to_email),
                subject='Study Buddy - Password Reset Confirmation',
                plain_text_content=Content("text/plain", plain_content),
                html_content=Content("text/html", html_content)
            )

            response = self._client.send(message)
            return response.status_code in [200, 201, 202]
        except Exception as e:
            print(f"Error sending confirmation email: {str(e)}")
            # Don't raise error for confirmation email failure
            return False
