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

class Enseignement(BaseModel):
    id_p: int = 0
    id_m: int = 0
    id_c: int = 0
    nb_heure: int

@app.post("/add")
async def addEnseignement(enseignement:Enseignement,db: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor()
        sql = "INSERT INTO enseignement (id_prof,id_matiere,id_classe,nb_heure) values(%s,%s,%s,%s)"
        prof = enseignement.id_p
        matiere = enseignement.id_m
        classe = enseignement.id_c
        nb_heure = enseignement.nb_heure

        param_values = (prof, matiere, classe, nb_heure)
        cursor.execute(sql,param_values)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur de base de données")
    finally:
        cursor.close()
        db.close()


@app.delete("/delete/{id}")
async def deleteEnseignement(id,db: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor()
        sql = "DELETE FROM enseignement WHERE id = "+id
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur de base de données")
    finally:
        cursor.close()
        db.close()

@app.put("/edit/{id}")
async def editEnseignement(id, enseignement:Enseignement, db: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor()
        sql = "UPDATE enseignement SET nb_heure = %s WHERE id =%s"
        nb_heure = enseignement.nb_heure

        cursor.execute(sql,(nb_heure,id))
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur de base de données")
    finally:
        cursor.close()
        db.close()


@app.get("/liste")
async def listEnseignement(db: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor()
        sql = "SELECT *, libelle, design, nom, parcours FROM enseignement, matiere, classe, enseignant WHERE enseignement.id_prof = enseignant.id AND enseignement.id_matiere = matiere.id AND enseignement.id_classe = classe.id"
        param_values = ()
        cursor.execute(sql,param_values)
        results = cursor.fetchall()
        enseignement = []
        content = {}
        for result in results:
            content = {'id': result[0], 'libelle': result[6], 'design': result[8], 'parcours': result[9], 'nom': result[11], 'nb_heure': result[4]}
            enseignement.append(content)
        return enseignement
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur de base de données")
    finally:
        cursor.close()
        db.close()

@app.get("/about/{id}")
def getInformation(id, db: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor()
        sql = "SELECT * FROM enseignement WHERE id ="+id
        cursor.execute(sql,())
        results = cursor.fetchall()
        content = {}
        for result in results:
            content = {'id': result[0], 'nb_heure': result[4]}
        return content
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur de base de données")
    finally:
        cursor.close()
        db.close()

@app.get("/heure/{id}")
def getInformation(id, db: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor()
        sql = "SELECT nom, libelle, nb_heure FROM enseignement, matiere, classe, enseignant WHERE enseignement.id_prof = enseignant.id AND enseignement.id_matiere = matiere.id AND enseignement.id_classe = classe.id AND enseignant.id = %s"
        cursor.execute(sql,(id,))
        results = cursor.fetchall()
        enseignement = []
        content = {}
        for result in results:
           content = {'nom': result[0], 'libelle': result[1], 'nb_heure': result[2]}
           enseignement.append(content)
        return enseignement
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur de base de données")
    finally:
        cursor.close()
        db.close()

@app.get("/nom/{id}")
def getInformationf(id, db: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor()
        sql = "SELECT nom FROM enseignement, matiere, classe, enseignant WHERE enseignement.id_prof = enseignant.id AND enseignement.id_matiere = matiere.id AND enseignement.id_classe = classe.id AND enseignant.id = %s group by nom"
        cursor.execute(sql,(id,))
        results = cursor.fetchall()
        enseignement = []
        content = {}
        for result in results:
           content = {'nom': result[0]}
           enseignement.append(content)
        return enseignement
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur de base de données")
    finally:
        cursor.close()
        db.close()

@app.get("/total/{id}")
def getInformation2(id, db: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    try:
        cursor = db.cursor()
        sql = "SELECT sum(nb_heure) as tot FROM enseignement, matiere, classe, enseignant WHERE enseignement.id_prof = enseignant.id AND enseignement.id_matiere = matiere.id AND enseignement.id_classe = classe.id AND enseignant.id = %s"
        cursor.execute(sql,(id,))
        results = cursor.fetchall()
        enseignement = []
        content = {}
        for result in results:
           content = {'tot': result[0]}
           enseignement.append(content)
        return enseignement
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur de base de données")
    finally:
        cursor.close()
        db.close()
