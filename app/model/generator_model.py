from pydantic import BaseModel

class GeneratorModel(BaseModel):
    course_name : str
    issue_date : str
    recipient_details : list[dict]