from fastapi import APIRouter, Response
from app.model.generator_model import GeneratorModel
from app.service.generator_service import generate_certificates_service,generation_status

router = APIRouter()

@router.post("/generate") 
def generate_certificates_route(generator : GeneratorModel):
    certificates_zip = generate_certificates_service(generator)
    failed_generations = len(generator.recipient_details) - generation_status()
    return Response(
        content = certificates_zip,
        media_type = "application/zip",
        headers={"Content-Disposition": 'attachment; filename="certificates.zip"',
            "X-Total": str(len(generator.recipient_details)),
            "X-Succeeded": str(generation_status()),
            "X-Failed": str(failed_generations),}
    )