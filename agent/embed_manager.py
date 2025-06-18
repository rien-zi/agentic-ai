# embed_manager.py

import os
import hashlib
import pickle
from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import UnstructuredMarkdownLoader

EMBED_DIR = "vectorstore"
HASH_FILE = ".embedding_hashes.pkl"

def compute_file_hash(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def get_all_markdown_files(directories: List[str]) -> List[Path]:
    files = []
    for directory in directories:
        files.extend(Path(directory).glob("*.md"))
        files.extend(Path(directory).glob("*.txt"))
    return files

def load_documents(paths: List[Path]) -> List[Document]:
    docs = []
    for path in paths:
        loader = UnstructuredMarkdownLoader(str(path))
        docs.extend(loader.load())
    return docs

def load_embeddings(force_reload=False):
    paths = get_all_markdown_files(["sop_docs", "cardinal", "static_templates"])
    current_hashes = {str(p): compute_file_hash(p) for p in paths}

    if os.path.exists(HASH_FILE) and not force_reload:
        with open(HASH_FILE, "rb") as f:
            saved_hashes = pickle.load(f)
        if saved_hashes == current_hashes and os.path.exists(EMBED_DIR):
            db = FAISS.load_local(EMBED_DIR, OpenAIEmbeddings(), allow_dangerous_deserialization=True)
            return db

    docs = load_documents(paths)
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(EMBED_DIR)

    with open(HASH_FILE, "wb") as f:
        pickle.dump(current_hashes, f)

    return db
