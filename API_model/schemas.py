from pydantic import BaseModel


class PredictRequest(BaseModel):
    data: list

class LoginRequest(BaseModel):
    username: str
    password: str