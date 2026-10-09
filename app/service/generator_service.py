import zipfile
from io import BytesIO
from datetime import date
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4 , landscape
from app.model.generator_model import GeneratorModel

W , H = landscape(A4)

unique_list = []

def generation_status():
    valid_generations = len(unique_list)
    return valid_generations

def get_grade(score: int) -> str:
    if score >= 90:
        return "with Distinction"
    if score >= 75:
        return "with Merit"
    return "with Pass"

def draw_template(c):
    # borders
    c.setStrokeColorRGB(0.1, 0.2, 0.5); c.setLineWidth(6)
    c.rect(30, 30, W - 60, H - 60)
    c.setStrokeColorRGB(0.72, 0.57, 0.23); c.setLineWidth(1.5)
    c.rect(42, 42, W - 84, H - 84)

    # fixed text
    c.setFillColorRGB(0.1, 0.2, 0.5)
    c.setFont("Helvetica-Bold", 38)
    c.drawCentredString(W / 2, H * 0.76, "CERTIFICATE OF COMPLETION")
    c.setFillColorRGB(0.33, 0.33, 0.33)
    c.setFont("Helvetica", 16)
    c.drawCentredString(W / 2, H * 0.63, "This is to certify that")
    c.drawCentredString(W / 2, H * 0.41, "has successfully completed the course")
    c.setFillColorRGB(0.1, 0.2, 0.5)
    c.setFont("Helvetica", 13)
    c.drawString(W * 0.75, H * 0.14, "Authority Sign")

def generate_certificate(name: str, course: str, issue_date: date, score: int) -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(W, H))
    draw_template(c)

    # recipient name
    c.setFillColorRGB(0.1, 0.2, 0.5)
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(W / 2, H * 0.52, name)

    # course name
    c.setFont("Helvetica", 24)
    c.drawCentredString(W / 2, H * 0.34, course)

    # score + grade
    c.setFillColorRGB(0.72, 0.57, 0.23)          # gold accent
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(W / 2, H * 0.26, f"{get_grade(score)}  |  Score: {score}%")

    # date
    c.setFillColorRGB(0.1, 0.2, 0.5)
    c.setFont("Helvetica", 13)
    c.drawString(W * 0.12, H * 0.14, f"Date: {issue_date}")

    c.save()
    return buffer.getvalue()    # return the PDF bytes

def generate_zip(certificate_list : list[tuple[str,bytes]]) -> bytes:
    buffer = BytesIO()
    with zipfile.ZipFile(buffer,"w",zipfile.ZIP_DEFLATED) as zf:
        for file_name,pdf in certificate_list :
            zf.writestr(file_name,pdf)
    return buffer.getvalue()

def generate_certificates_service(generator : GeneratorModel):
    valid_generations = 0
    course_name = generator.course_name
    issue_date = generator.issue_date
    recipients = generator.recipient_details
    seen_emails = set()
    certificates = []
    
    for recipient_obj in recipients:
        if recipient_obj.recipient_email not in seen_emails and recipient_obj.recipient_score >= 75:
            seen_emails.add(recipient_obj.recipient_email)
            unique_list.append(recipient_obj)

    for index, recipient in enumerate(unique_list,start=1):
        pdf = generate_certificate(recipient.recipient_name,course_name,issue_date,recipient.recipient_score)
        certificates.append((f"{index} {recipient.recipient_name} Certificate.pdf",pdf))
    certificates_zip = generate_zip(certificates)

    return certificates_zip