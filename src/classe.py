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

class Classe(BaseModel):
    design:str
    parcours:str

@app.post("/add")
async def addClasse(classe:Classe,db: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor()
        sql = "INSERT INTO classe (design,parcours) values(%s,%s)"
        design = classe.design
        parcours = classe.parcours

        param_values = (design, parcours)
        cursor.execute(sql,(param_values))
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur de base de données")
    finally:
        cursor.close()
        db.close()
        
    
@app.delete("/delete/{id}")
async def deleteClasse(id,db: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor()
        sql = "DELETE FROM classe WHERE id = "+id
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur de base de données")
    finally:
        cursor.close()
        db.close()
  
@app.put("/edit/{id}")
async def editClasse(id, classe:Classe, db: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor()
        sql = "UPDATE classe SET design = %s, parcours = %s WHERE id = "+id
        design = classe.design
        parcours = classe.parcours

        param_values = (design, parcours)
        cursor.execute(sql,(param_values))
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur de base de données")
    finally:
        cursor.close()
        db.close()

@app.get("/liste")
async def listClasse(db: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor()
        sql = "SELECT * FROM classe"
        param_values = ()
        cursor.execute(sql,param_values)
        results = cursor.fetchall()
        classe = []
        content = {}
        for result in results:
            content = {'id': result[0], 'design': result[1], 'parcours': result[2]}
            classe.append(content)
        return classe
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur de base de données")
    finally:
        cursor.close()
        db.close()


@app.get("/about/{id}")
def getInformation(id, db: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor()
        sql = "SELECT * FROM classe WHERE id ="+id
        cursor.execute(sql,())
        results = cursor.fetchall()
        content = {}
        for result in results:
            content = {'id': result[0], 'design': result[1], 'parcours': result[2]}
        return content
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur de base de données")
    finally:
        cursor.close()
        db.close()
