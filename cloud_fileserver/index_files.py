
from tqdm import tqdm 
from pathlib import Path
import os, json, traceback
from dotenv import load_dotenv
# NEW ✅
from langchain_community.document_loaders import TextLoader, PythonLoader

from langchain_text_splitters              import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
load_dotenv()
DB_PATH = Path("faiss_index")          # ← ⬅ keep index + watcher in sync
INDEX_DIR = DB_PATH 
# 1️⃣ — EDIT THESE PATHS ONLY ↓ (use Windows Explorer address-bar, Ctrl +C, paste) ─
DIRECTORIES = [
    Path(r"C:\Users\ensid\OneDrive\Documents\myuploads"),
]
print("\n📂 roots to scan:")
for d in DIRECTORIES: print("   ", d, "→", "EXISTS" if d.exists() else "MISSING")
print()
TEXT_EXT = None 


MAX_SIZE = 2_000_000_000          # bytes  (≈ 2 MB)
CHUNK_CHARS    = 3_500              # ≈ 1 000 tokens
CHUNK_OVERLAP  = 200
BATCH_DOCS   = 50 
docs  = []
pbar  = tqdm(desc="🔍 scanning files", unit="file")

skipped   = []

from langchain_text_splitters import RecursiveCharacterTextSplitter   # ← add near top

       # keeps context between chunks

def safe_load(p: Path):
    try:
        if p.suffix.lower() == ".py":
            docs = PythonLoader(str(p)).load()
        else:
            docs = TextLoader(str(p), autodetect_encoding=True,
                              errors="ignore").load()
    except Exception:
        docs = []
    if not docs:                       # fallback for binary / unreadable
        docs = [Document(page_content=p.name,
                         metadata={"source": str(p)})]
    return docs                        # ← single exit point



for root in DIRECTORIES:
    for p in root.rglob("*"):
        if (p.is_file() and p.stat().st_size < MAX_SIZE):
                loaded = safe_load(p)
                docs.extend(loaded)
                pbar.update(len(loaded))
                print(p) 


pbar.close()                      # stop first bar

if not docs:                      # ⬅ guard BEFORE creating embeddings
    print("⚠️  0 indexable docs — check the printed paths and TEXT_EXT list")
    exit()
emb = OpenAIEmbeddings(model="text-embedding-3-small",
                       disallowed_special=(),
                       # ↓ gives binary-safe hashes for all files
                       allowed_special="all")
db  = None
with tqdm(total=len(docs), desc="⬆ embedding", unit="doc") as bar:
    for i in range(0, len(docs), BATCH_DOCS):
        chunk = docs[i : i + BATCH_DOCS]
        if db is None:
            db = FAISS.from_documents(chunk, emb)
        else:
            db.add_documents(chunk)
        bar.update(len(chunk))


db.save_local(DB_PATH)
print(f"✅  Indexed {len(docs):,} docs  →  {DB_PATH}")

