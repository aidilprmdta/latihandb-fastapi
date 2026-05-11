from pydantic import BaseModel

class ProdiCreate(BaseModel):
    id: str
    nama: str
    fakultas: str

class ProdiUpdate(BaseModel):
    nama: str
    fakultas: str

class FakultasCreate(BaseModel):
    id: str
    nama_fakultas: str

class FakultasUpdate(BaseModel):
    nama_fakultas: str