from pydantic import BaseModel, EmailStr, Field
from datetime import date

class Recipient(BaseModel):
    recipient_name :  str = Field(...,min_length=3,max_length=20,description="Name of the recipient",example="Parameshwaran G")
    recipient_email : str = Field(...,description="Email of the recipient",example="parameshwarangdev@gmail.com")

class GeneratorModel(BaseModel):
    course_name : str = Field(...,description="Name of the course",example="Backend with FastAPI")
    issue_date :  date | None = None
    recipient_details : list[Recipient]