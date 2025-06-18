# main.py

import os
from dotenv import load_dotenv
from agent.embed_manager import load_embeddings
from agent.sop_loader import load_all_sops, load_cardinal, load_etiq
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env")

# Load knowledge
print("🔹 Loading embeddings...")
db = load_embeddings()
retriever = db.as_retriever()
qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(openai_api_key=api_key), retriever=retriever)

# Load routing & SOPs
cardinal = load_cardinal()
etiquette = load_etiq()
sops = load_all_sops()

print("💬 Ask your support question (type 'exit' to quit):")

while True:
    query = input("🧾 You: ")
    if query.strip().lower() in ["exit", "quit"]:
        break

    print("🔍 Matching scenario via cardinal.md...")
    routing_result = qa.invoke({"query": query + "\nBased on this query, tell me which SOP filename from the list below should be used:\n" +
                                ", ".join(f"{k}.md" for k in sops.keys()) +
                                "\nIf none match, reply only: NONE.\n\n" + cardinal})

    sop_key = routing_result.get("result", "").strip().replace(".md", "")

    if sop_key not in sops:
        print("🚫 Human Intervention required as the query is out of defined bounds.")
        continue

    sop_text = sops[sop_key]

    # Final SOP + etiquette-based response
    final_query = (
        f"User query: {query}\n\n"
        f"Use this SOP to guide the response:\n{sop_text}\n\n"
        f"Ensure tone matches the following etiquette:\n{etiquette}\n\n"
        f"Now write a complete support response."
    )

    print("🤖 Generating response...")
    result = qa.invoke({"query": final_query})
    print("\n📢 Agent Response:\n", result.get("result", result))
