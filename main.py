from fastapi import FastAPI
import uvicorn
from src.enseignement import app as app0
from src.enseignant import app as app1
from src.matiere import app as app2
from src.classe import app as app3

app = FastAPI()

app.mount("/enseignement", app0)
app.mount("/enseignant", app1)
app.mount("/matiere", app2)
app.mount("/classe", app3)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)