# ─ imports ───────────────────────────────────────────────
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import secrets, os
# ─────────────────────────────────────────────────────────

load_dotenv()
USER = os.getenv("FS_USER")
PASS = os.getenv("FS_PASS")
INDEX_DIR = Path("faiss_index")

security = HTTPBasic()

def check(creds: HTTPBasicCredentials = Depends(security)):
    ok = creds.username == USER and secrets.compare_digest(creds.password, PASS)
    if not ok:
        raise HTTPException(status_code=401, detail="🔐 Wrong credentials")
    return True

emb = OpenAIEmbeddings(model="text-embedding-3-small", disallowed_special=())
db  = FAISS.load_local(str(INDEX_DIR), emb, allow_dangerous_deserialization=True)

app = FastAPI(title="Cloud-GPT-FileSearch")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

# expose plugin manifest
app.mount("/.well-known", StaticFiles(directory=".well-known"), name="wellknown")

def custom_openapi():
    if app.openapi_schema: return app.openapi_schema
    s = get_openapi(
        title=app.title, version="0.1.0",
        description="Secure cloud file search", routes=app.routes
    )
    s["servers"] = [{"url": "https://YOUR-DOMAIN"}]   # ← edit when deployed
    app.openapi_schema = s
    return s
app.openapi = custom_openapi

class Ask(BaseModel):
    query: str
    k: int = 5

@app.post("/ask")
def ask(body: Ask, _: bool = Depends(check)):
    docs = db.similarity_search(body.query, body.k)
    return [
        {"path": d.metadata["source"], "snippet": d.page_content[:160]}
        for d in docs
    ]

@app.get("/")
def root():
    return {"msg": "🟢 online"}
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
