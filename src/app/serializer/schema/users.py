from pydantic import BaseModel, Field, EmailStr


class UserLogin(BaseModel):
    login: str = Field(min_length=3)
    password: str = Field(min_length=6)


class UserCreate(BaseModel):
    login: str = Field(min_length=3)
    password: str = Field(min_length=6)
    email: str = EmailStr()
    name: str = Field(min_length=2)


class UserReplace(BaseModel):
    login: str = Field(min_length=3)
    password: str = Field(min_length=6)
    email: str = EmailStr()
    name: str = Field(min_length=2)


class UserUpdate(BaseModel):
    login: str | None = Field(min_length=3)
    password: str | None = Field(min_length=6)
    email: str | None = EmailStr()
    name: str | None = Field(min_length=2)
