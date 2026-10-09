from fastapi import APIRouter, Response
from app.model.generator_model import GeneratorModel
from app.service.generator_service import generate_certificates_service

router = APIRouter()

@router.post("/generate") 
def generate_certificates_route(generator : GeneratorModel):
    certificates_zip = generate_certificates_service(generator)
    return Response(
        content = certificates_zip,
        media_type = "application/zip",
        headers={"Content-Disposition": 'attachment; filename="certificates.zip"'}
    )