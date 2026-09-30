import re

from pydantic import BaseModel, EmailStr, field_validator

# Letters, spaces, hyphens, apostrophes, and periods (covers "Mary-Jane",
# "O'Brien", "Dr. Smith") -- must start and end with a letter, so a bare
# symbol or trailing punctuation can't sneak through.
NAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z '\-.]*[A-Za-z]$")


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    interface_mode: str = "beginner"

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2:
            raise ValueError("Name must be at least 2 characters long")
        if any(ch.isdigit() for ch in v):
            raise ValueError("Name cannot contain numbers")
        if not NAME_PATTERN.match(v):
            raise ValueError("Name can only contain letters, spaces, hyphens, apostrophes, and periods")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if v.strip() != v:
            raise ValueError("Password cannot start or end with a space")
        if not re.search(r"[A-Za-z]", v):
            raise ValueError("Password must contain at least one letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    interface_mode: str
    target_track: str | None = None

    class Config:
        from_attributes = True
