# 🧠 Agentic AI – SOP-Guided Support Bot (LangChain Starter)

Agentic AI is a domain-bound support automation agent built using **LangChain**, **OpenAI**, and **FAISS**. It mimics how human agents refer to Standard Operating Procedures (SOPs) while handling support queries.

This bot:
- Accepts natural-language queries (e.g., support emails or chat input),
- Consults `cardinal.md` to **route the query** to the correct SOP document,
- Applies formal response etiquette from `chat_etiq.md`,
- Uses **retrieval-augmented generation (RAG)** with FAISS and OpenAI to generate responses,
- Falls back to **static templates** when necessary (e.g., missing information or ineligible cases),
- Returns `"Human Intervention required..."` for undefined scenarios.

> ⚙️ This is a **starter kit**. You can extend, replace, or fine-tune SOPs, templates, and routing logic to match your org’s real processes.

---

## 📁 Project Structure

agentic_ai/
├── main.py # Terminal-based chatbot loop
├── .env # OpenAI API key
├── vectorstore/ # Auto-generated FAISS index
├── .embedding_hashes.pkl # Used to detect SOP/template changes
├── faiss_index/ # Auto-generated FAISS index
├── agent/
│ ├── embed_manager.py # Hash-aware FAISS index manager
│ └── sop_loader.py # Routes to Necessary SOP
├── cardinal/
│ ├── cardinal.md # Scenario-to-SOP routing logic
│ └── chat_etiq.md # Etiquette guidelines for response tone
├── sop_docs/ # SOP markdowns per scenario
│ ├── respond_to_refund.md
│ ├── handle_delivery_delay.md
│ ├── resolve_missing_items.md
│ ├── subscription_info.md
│ └── account_closure.md
├── static_templates/ # Reusable static fallback responses
│ ├── ref_denial.txt
│ └── need_more_details.txt
└── .gitignore

---

## 🚀 Quickstart

### 1. Clone & set up environment

```
git clone https://github.com/rien-zi/agentic-ai.git
cd agentic-ai
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies
```
pip install -r requirements.txt
```
Or manually:
```
pip install langchain langchain-openai langchain-community faiss-cpu python-dotenv unstructured
```

### 3. Create .env
```
OPENAI_API_KEY=sk-<your-key-here>
```

---

## 🧠 How It Works
1. Load embeddings:
- SOPs, cardinal.md, chat_etiq.md, and static templates are loaded.
- FAISS index is generated and cached unless hashes change.

2. Query Input:
- The user enters a support-like query in terminal (e.g., “I want to cancel my Swiggy subscription”).

3. Cardinal Routing:
- The bot consults cardinal.md to decide which SOP to reference.

4. Etiquette Application:
- chat_etiq.md is used to tune the tone (empathetic, apologetic, helpful).

5. SOP Retrieval:
- The appropriate .md from sop_docs/ is retrieved and embedded context is passed to OpenAI.

6. Fallback Handling:
- If needed data is missing → uses need_more_details.txt.
- If refund conditions not met → uses ref_denial.txt.
- If the query doesn't match any known SOP → Human Intervention required... message is returned.

---

## ✍️ Example Queries
| User Prompt | Behavior |
| ----------- | ----------- |
| "I want a refund"	| Routes to respond_to_refund.md |
| "My order was late again." | Uses handle_delivery_delay.md |
| "Please close my Swiggy account."	| Uses account_closure.md |
| "What do you think of Batman?" | Falls back: Human Intervention required... |
| "My order was wrong." (no order ID) | Responds with need_more_details.txt |

---

## ⚠️ Guardrails
- ❌ No general knowledge answering (e.g., celebrities, facts)
- ✅ Swiggy-specific support scenarios only
- 🔄 Embeddings are rebuilt only if files change
- ✅ Static templates ensure consistent fallback messaging

---

## 🔧 Customization
You can extend this easily by:
- Adding more .md files in sop_docs/
- Updating cardinal.md to define new scenario mappings
- Editing chat_etiq.md to tune tone (e.g., add escalation steps)
- Adding templates in static_templates/ for common fallback cases

---

## 📜 Disclaimer
This project is a starter framework. The SOPs and templates included are minimal examples and not production-grade. Replace them with real documents and compliance-reviewed flows before using in live environments.

---

## 📂 Future Enhancements (Suggestions)
- Add sentiment scoring to further adjust tone
- Integrate email ingestion or webhook input
- Enable logging and admin review for fallback hits
- Replace terminal loop with a FastAPI or Flask interface

---

## 🪪 License
MIT

---

## 🙌 Acknowledgements
Built using:
- LangChain
- OpenAI API
- FAISS
- Python