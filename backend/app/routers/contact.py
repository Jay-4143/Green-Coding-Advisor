from fastapi import APIRouter, HTTPException
from ..schemas import ContactRequest
from ..logger import green_logger
from ..email_service import email_service

router = APIRouter()

@router.post("")
async def submit_contact_form(contact_data: ContactRequest):
    """Submit a contact form message"""
    # Send email to admin
    email_service.send_email(
        to_email="vasanijay3008@gmail.com",
        subject=f"New Contact Form Submission from {contact_data.name}",
        body=f"""
Name: {contact_data.name}
Email: {contact_data.email}
Message:
{contact_data.message}
""",
        html_body=f"""
<html>
<body>
    <h2>New Contact Form Submission</h2>
    <p><strong>Name:</strong> {contact_data.name}</p>
    <p><strong>Email:</strong> {contact_data.email}</p>
    <p><strong>Message:</strong></p>
    <p>{contact_data.message}</p>
</body>
</html>
"""
    )
    
    green_logger.logger.info(f"Contact form submitted by {contact_data.email}")
    
    return {"message": "Message received. We'll get back to you soon!"}
