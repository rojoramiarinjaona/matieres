from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

def get_db_connection():
    db_params = {
        "host": "enseignant.cshheptmedeq.us-east-1.rds.amazonaws.com",
        "user": "",
        "password": "",
        "database": "",
    }
    return mysql.connector.connect(**db_params)

class Matiere(BaseModel):
    libelle:str

@app.post("/add")
async def addMatiere(matiere:Matiere,db: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor()
        sql = "INSERT INTO matiere (libelle) values(%s)"
        libelle = matiere.libelle

        param_values = (libelle)
        cursor.execute(sql,(param_values,))
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur de base de données")
    finally:
        cursor.close()
        db.close()
        
    
@app.delete("/delete/{id}")
async def deleteMatiere(id,db: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor()
        sql = "DELETE FROM matiere WHERE id = "+id
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur de base de données")
    finally:
        cursor.close()
        db.close()
  
@app.put("/edit/{id}")
async def editMatiere(id, matiere:Matiere, db: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor()
        sql = "UPDATE matiere SET libelle = %s WHERE id = "+id
        libelle = matiere.libelle

        param_values = (libelle)
        cursor.execute(sql,(param_values,))
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur de base de données")
    finally:
        cursor.close()
        db.close()

@app.get("/liste")
async def listMatiere(db: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor()
        sql = "SELECT * FROM matiere"
        param_values = ()
        cursor.execute(sql,param_values)
        results = cursor.fetchall()
        matiere = []
        content = {}
        for result in results:
            content = {'id': result[0], 'libelle': result[1]}
            matiere.append(content)
        return matiere
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur de base de données")
    finally:
        cursor.close()
        db.close()


@app.get("/about/{id}")
def getInformation(id, db: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor()
        sql = "SELECT * FROM matiere WHERE id ="+id
        cursor.execute(sql,())
        results = cursor.fetchall()
        content = {}
        for result in results:
            content = {'id': result[0], 'libelle': result[1]}
        return content
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur de base de données")
    finally:
        cursor.close()
        db.close()
