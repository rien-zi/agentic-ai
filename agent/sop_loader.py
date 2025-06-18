# sop_loader.py

from pathlib import Path
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_core.documents import Document

def load_markdown(path: Path) -> str:
    loader = UnstructuredMarkdownLoader(str(path))
    docs = loader.load()
    return docs[0].page_content if docs else ""

def load_all_sops():
    sop_dir = Path("sop_docs")
    return {
        f.stem: load_markdown(f)
        for f in sop_dir.glob("*.md")
    }

def load_cardinal():
    return load_markdown(Path("cardinal/cardinal.md"))

def load_etiq():
    return load_markdown(Path("cardinal/chat_etiq.md"))

def load_static_template(template_code: str) -> str:
    path = Path(f"static_templates/{template_code}.txt")
    return path.read_text() if path.exists() else ""
