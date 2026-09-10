from pydantic import BaseModel, Field


class AdvertisementCreate(BaseModel):
    title: str = Field(min_length=2)


class AdvertisementReplace(BaseModel):
    title: str = Field(min_length=2)


class AdvertisementUpdate(BaseModel):
    title: str | None = Field(min_length=2)
