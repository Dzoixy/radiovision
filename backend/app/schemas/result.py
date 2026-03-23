from pydantic import BaseModel

class ResultResponse(BaseModel):
    id: str
    finding: str
    confidence: float
    purpose: str    
    preset: str        
    image_url: str
    suggestion: str