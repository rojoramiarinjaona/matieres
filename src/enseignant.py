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

class Enseignant(BaseModel):
    nom:str

@app.post("/add")
async def addEnseignant(enseignant:Enseignant,db: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor()
        sql = "INSERT INTO enseignant (nom) values(%s)"
        nom = enseignant.nom

        param_values = (nom)
        cursor.execute(sql,(param_values,))
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur de base de données")
    finally:
        cursor.close()
        db.close()
        
    
@app.delete("/delete/{id}")
async def deleteEnseignant(id,db: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor()
        sql = "DELETE FROM enseignant WHERE id = "+id
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur de base de données")
    finally:
        cursor.close()
        db.close()
  
@app.put("/edit/{id}")
async def editEnseignant(id, enseignant:Enseignant, db: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor()
        sql = "UPDATE enseignant SET nom = %s WHERE id = "+id
        nom = enseignant.nom

        param_values = (nom)
        cursor.execute(sql,(param_values,))
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur de base de données")
    finally:
        cursor.close()
        db.close()

@app.get("/liste")
async def listEnseignant(db: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor()
        sql = "SELECT * FROM enseignant order by nom"
        param_values = ()
        cursor.execute(sql,param_values)
        results = cursor.fetchall()
        enseignant = []
        content = {}
        for result in results:
            content = {'id': result[0], 'nom': result[1]}
            enseignant.append(content)
        return enseignant
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur de base de données")
    finally:
        cursor.close()
        db.close()


@app.get("/about/{id}")
def getInformation(id, db: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor()
        sql = "SELECT * FROM enseignant WHERE id ="+id
        cursor.execute(sql,())
        results = cursor.fetchall()
        content = {}
        for result in results:
            content = {'id': result[0], 'nom': result[1]}
        return content
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur de base de données")
    finally:
        cursor.close()
        db.close()
