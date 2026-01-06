import chromadb
from sentence_transformers import SentenceTransformer
import os
try:
    from src.budget_guidelines import budget_guidelines
except ImportError:
    from budget_guidelines import budget_guidelines

class BudgetRAG:
    def __init__(self):
        # 1. Setup Embedder Pipeline
        # Using a solid open-source embedding model
        # Note: This requires downloading the model on first run (~133MB)
        print("Loading embedding model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2') # Smaller, faster, reliable fallback
        
        # 2. Setup Vector Store (ChromaDB)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, "chroma_db")
        
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name="budget_guidelines")
        
        # 3. Index Documents (Knowledge Base)
        if self.collection.count() == 0:
            print("Indexing budget guidelines...")
            self._index_documents()
        else:
            print(f"Loaded existing index with {self.collection.count()} documents.")

    def _index_documents(self):
        embeddings = self.model.encode(budget_guidelines).tolist()
        ids = [str(i) for i in range(len(budget_guidelines))]
        self.collection.add(
            documents=budget_guidelines,
            embeddings=embeddings,
            ids=ids
        )
        print("Indexing complete.")

    def retrieve(self, query, k=5):
        # 4. Retriever Module
        query_embedding = self.model.encode([query]).tolist()
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=k
        )
        # flatten results
        return results['documents'][0] if results['documents'] else []

if __name__ == "__main__":
    try:
        rag = BudgetRAG()
        test_query = "What is the 50/30/20 rule?"
        results = rag.retrieve(test_query)
        
        print(f"\nQUERY: {test_query}")
        print("RETRIEVED CONTEXT:")
        for idx, res in enumerate(results, 1):
            print(f"{idx}. {res}")
            
    except Exception as e:
        print(f"An error occurred: {e}")
