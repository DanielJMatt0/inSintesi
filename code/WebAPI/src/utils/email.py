import os
import resend

resend.api_key = os.getenv("RESEND_API_KEY")
BASE_URL = os.getenv("FRONTEND_BASE_URL")


def send_token_email(user_email: str, token_value: str, question_content: str):
    """Send an email with a direct link to answer the question."""
    answer_link = f"{BASE_URL}/answer/{token_value}"

    subject = "New Question Assigned"
    html_body = f"""
        <p>Hello,</p>
        <p>You have been assigned a new question:</p>
        <blockquote>{question_content}</blockquote>
        <p>Your personal link:</p>
        <p><a href="{answer_link}">{answer_link}</a></p>
        <p>If the link does not work, you can use this token manually:</p>
        <p><strong>{token_value}</strong></p>
    """

    params: resend.Emails.SendParams = {
        "from": "inSintesi <onboarding@resend.dev>",
        "to": [user_email],
        "subject": subject,
        "html": html_body,
    }

    try:
        response = resend.Emails.send(params)
        print("Resend response:", response)
    except Exception as e:
        print("Error sending email:", e)
