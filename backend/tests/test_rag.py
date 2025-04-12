# test_rag.py
from app.services.rag_service import RAGService

def test_rag_queries():
    # Initialize the RAG service
    rag = RAGService()
    
    # Test queries
    test_queries = [
        "What are the health insurance benefits?",
        "Tell me about pension plans",
        "What is the premium payment process?",
        "How do I file a claim?",
        "What are the maturity benefits?"
    ]
    
    # Test each query
    for query in test_queries:
        print("\n" + "="*50)
        print(f"Query: {query}")
        print("="*50)
        
        try:
            context = rag.get_relevant_context(query, top_k=5)
            print("\nRelevant Context:")
            print("-"*30)
            print(context)
            
        except Exception as e:
            print(f"\nError processing query: {str(e)}")

if __name__ == "__main__":
    test_rag_queries()