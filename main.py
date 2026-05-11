from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import models
from schemas import ProdiCreate, ProdiUpdate
from database import SessionLocal, engine
from schemas import ProdiCreate, ProdiUpdate, FakultasCreate, FakultasUpdate

app = FastAPI(title="Praktikum Web API", version="1.0.0")

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.get("/")
def root():
    return {"message": "Selamat datang di API Sistem Akademik!"}

@app.get("/prodi/", status_code=200, description="Menampilkan data prodi")
def list_prodi(db: Session = Depends(get_db)):
    query = text("SELECT * FROM prodi")
    data_prodi = db.execute(query).mappings().fetchall()
    return {"total": len(data_prodi), "data": data_prodi}

@app.post("/prodi/", status_code=201, description="Menambahkan data prodi baru")
def create_prodi(pro: ProdiCreate, db: Session = Depends(get_db)):
    try:
        query = text("INSERT INTO prodi (id, nama, fakultas) VALUES (:pid, :pnama, :pfakultas)")
        db.execute(query, {"pid": pro.id, "pnama": pro.nama, "pfakultas": pro.fakultas})
        db.commit()
        return {
            "message": "Data berhasil disimpan",
            "data": {"id": pro.id, "nama": pro.nama, "fakultas": pro.fakultas}
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/prodi/{prodi_id}", status_code=200, description="Memperbarui data prodi")
def update_prodi(prodi_id: str, pro: ProdiUpdate, db: Session = Depends(get_db)):
    try:
        query = text("UPDATE prodi SET nama=:pnama, fakultas=:pfakultas WHERE id=:pid")
        result = db.execute(query, {"pid": prodi_id, "pnama": pro.nama, "pfakultas": pro.fakultas})
        db.commit()
        
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Prodi tidak ditemukan")
            
        return {
            "message": "Data berhasil diperbarui",
            "data": {"id": prodi_id, "nama": pro.nama, "fakultas": pro.fakultas}
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/prodi/{prodi_id}", status_code=200, description="Menghapus data prodi")
def delete_prodi(prodi_id: str, db: Session = Depends(get_db)):
    try:
        query = text("DELETE FROM prodi WHERE id=:pid")
        result = db.execute(query, {"pid": prodi_id})
        db.commit()
        
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Prodi tidak ditemukan")
            
        return {"message": f"Data dengan ID {prodi_id} berhasil dihapus"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
 
@app.get("/fakultas/", status_code=200, description="Mengambil semua daftar fakultas")
def list_fakultas(db: Session = Depends(get_db)):
    query = text("SELECT * FROM fakultas")
    data = db.execute(query).mappings().fetchall()
    return {"total": len(data), "data": data}

@app.post("/fakultas/", status_code=201, description="Menyimpan data fakultas baru")
def create_fakultas(fak: FakultasCreate, db: Session = Depends(get_db)):
    try:
        query = text("INSERT INTO fakultas (id, nama_fakultas) VALUES (:fid, :fnama)")
        db.execute(query, {"fid": fak.id, "fnama": fak.nama_fakultas})
        db.commit()
        return {"message": "Data fakultas berhasil disimpan", "data": {"id": fak.id, "nama_fakultas": fak.nama_fakultas}}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/fakultas/{id}", status_code=200, description="Mengubah data fakultas")
def update_fakultas(id: str, fak: FakultasUpdate, db: Session = Depends(get_db)):
    try:
        query = text("UPDATE fakultas SET nama_fakultas=:fnama WHERE id=:fid")
        result = db.execute(query, {"fid": id, "fnama": fak.nama_fakultas})
        db.commit()
        
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Fakultas tidak ditemukan")
            
        return {"message": "Data fakultas berhasil diperbarui", "data": {"id": id, "nama_fakultas": fak.nama_fakultas}}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/fakultas/{id}", status_code=200, description="Menghapus data fakultas")
def delete_fakultas(id: str, db: Session = Depends(get_db)):
    try:
        query = text("DELETE FROM fakultas WHERE id=:fid")
        result = db.execute(query, {"fid": id})
        db.commit()
        
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Fakultas tidak ditemukan")
            
        return {"message": f"Data fakultas dengan ID {id} berhasil dihapus"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/fakultas/{id}", status_code=200, description="Mengambil detail fakultas berdasarkan ID")
def get_fakultas_by_id(id: str, db: Session = Depends(get_db)):
    query = text("SELECT * FROM fakultas WHERE id=:fid")
    data = db.execute(query, {"fid": id}).mappings().fetchone() 
    
    if not data:
        raise HTTPException(status_code=404, detail="Fakultas tidak ditemukan")
        
    return {"data": data}