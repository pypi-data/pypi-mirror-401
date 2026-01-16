#!/usr/bin/env python3
"""
Test to compare RAG vs No RAG

This script shows the difference between:
1. RAG: Using your financial documents (vector database + Gemini)
2. No RAG: Just asking Gemini directly (no document context)
"""

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Test query
test_query = "What are Apple's main revenue sources in 2024?"

print("=" * 70)
print("COMPARISON: RAG vs NO RAG")
print("=" * 70)

# ============================================================================
# METHOD 1: WITHOUT RAG (Just Gemini, no documents)
# ============================================================================
print("\n\n### METHOD 1: WITHOUT RAG (No Document Context) ###")
print("-" * 70)
print("What happens: Gemini answers based ONLY on its training data")
print("Expected: General answer, no specific numbers from YOUR documents")
print("-" * 70)

try:
    # Initialize Gemini client (no vector database!)
    project_id = os.getenv('GCP_PROJECT_ID')
    location = os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1')

    client = genai.Client(
        vertexai=True,
        project=project_id,
        location=location
    )

    # Ask Gemini directly (NO CONTEXT from your documents)
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp',
        contents=[test_query],
        config={'temperature': 0.1, 'max_output_tokens': 500}
    )

    print(f"\nQuery: {test_query}")
    print(f"\nGemini's Answer (WITHOUT your documents):")
    print(response.text)
    print("\n❌ Notice: No citations, no specific data from YOUR 10-K filings")

except Exception as e:
    print(f"Error: {e}")

# ============================================================================
# METHOD 2: WITH RAG (Vector Database + Gemini)
# ============================================================================
print("\n\n" + "=" * 70)
print("### METHOD 2: WITH RAG (Using Your Document Context) ###")
print("-" * 70)
print("What happens: ")
print("  1. Search your vector database for relevant chunks")
print("  2. Send those chunks to Gemini as context")
print("  3. Gemini answers based on YOUR actual documents")
print("Expected: Specific answer with citations from YOUR 10-K filings")
print("-" * 70)

try:
    # Import your RAG system
    exec(open('07_generation_system.py').read())

    # Initialize RAG system (vector database + Gemini)
    rag = FinancialRAGSystem('vector_db/')

    # Query with RAG
    print(f"\nQuery: {test_query}")
    result = rag.query(test_query)

    print(f"\nRAG Answer (WITH your documents):")
    print(result['answer'])

    print(f"\n✅ Citations from YOUR documents:")
    for i, citation in enumerate(result['citations'][:3], 1):
        print(f"  [{i}] {citation['user_friendly_format']}")
        print(f"      Similarity: {citation['similarity_score']:.3f}")

    print(f"\n✅ Retrieved {result['retrieved_chunks']} chunks from vector database")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# SUMMARY
# ============================================================================
print("\n\n" + "=" * 70)
print("SUMMARY - KEY DIFFERENCES")
print("=" * 70)
print("""
WITHOUT RAG (Method 1):
  ❌ No access to your specific documents
  ❌ No citations
  ❌ Answers based on Gemini's general training data
  ❌ Can't answer company-specific questions accurately
  ❌ No retrieval step

WITH RAG (Method 2):
  ✅ Searches your 7,786 document chunks
  ✅ Provides citations from actual 10-K filings
  ✅ Answers based on YOUR specific documents
  ✅ Can answer detailed, company-specific questions
  ✅ Shows which documents were used (transparency)

RAG = More accurate, verifiable, document-grounded answers!
""")
print("=" * 70)
