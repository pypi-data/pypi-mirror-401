#!/usr/bin/env python3
"""
Example script demonstrating LEANN backend vs FAISS backend
Compares storage size and performance
"""
import os
import sys
import time
from pathlib import Path

# Add javis to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from javis.rag.code_loader import CodeLoader
from javis.rag.vector_store_factory import VectorStoreFactory


def get_directory_size(path):
    """Calculate total size of directory in MB"""
    total = 0
    try:
        for entry in Path(path).rglob('*'):
            if entry.is_file():
                total += entry.stat().st_size
    except Exception as e:
        print(f"Error calculating size: {e}")
    return total / (1024 * 1024)  # Convert to MB


def benchmark_backend(backend_name, codebase_dir, index_name, storage_dir="/tmp/javis_rag_benchmark"):
    """Benchmark a specific backend"""
    print(f"\n{'='*60}")
    print(f"Benchmarking: {backend_name.upper()}")
    print(f"{'='*60}")
    
    try:
        # Create vector store
        print(f"\n1. Creating {backend_name} vector store...")
        vector_store = VectorStoreFactory.create_vector_store(
            backend=backend_name,
            storage_dir=storage_dir,
            mode="retrieval_only"
        )
        
        # Load and chunk documents
        print(f"\n2. Loading codebase from: {codebase_dir}")
        loader = CodeLoader()
        start_load = time.time()
        chunks = loader.load_and_chunk(codebase_dir)
        load_time = time.time() - start_load
        
        print(f"   ✓ Loaded {len(chunks)} chunks in {load_time:.2f}s")
        
        # Build index
        print(f"\n3. Building {backend_name} index...")
        start_build = time.time()
        vector_store.create_vectorstore(chunks, index_name=index_name)
        build_time = time.time() - start_build
        
        print(f"   ✓ Index built in {build_time:.2f}s")
        
        # Calculate index size
        index_path = os.path.join(storage_dir, f"{index_name}.{backend_name}")
        if backend_name == "faiss":
            index_path = os.path.join(storage_dir, f"{index_name}.faiss")
        elif backend_name == "leann":
            index_path = os.path.join(storage_dir, f"{index_name}.leann")
        
        index_size = get_directory_size(index_path)
        print(f"   ✓ Index size: {index_size:.2f} MB")
        
        # Test query
        print(f"\n4. Testing query performance...")
        test_queries = [
            "How does the system handle errors?",
            "What is the main entry point?",
            "Explain the authentication flow"
        ]
        
        # Load index
        vector_store.load_vectorstore(index_name=index_name)
        
        query_times = []
        for query in test_queries:
            start_query = time.time()
            results = vector_store.search(query, k=5)
            query_time = time.time() - start_query
            query_times.append(query_time)
            print(f"   Query: '{query[:40]}...'")
            print(f"   → Found {len(results)} results in {query_time*1000:.0f}ms")
        
        avg_query_time = sum(query_times) / len(query_times)
        
        # Return metrics
        return {
            "backend": backend_name,
            "chunks": len(chunks),
            "load_time": load_time,
            "build_time": build_time,
            "index_size_mb": index_size,
            "avg_query_time_ms": avg_query_time * 1000,
            "success": True
        }
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return {
            "backend": backend_name,
            "success": False,
            "error": str(e)
        }


def compare_backends(codebase_dir):
    """Compare FAISS and LEANN backends"""
    print("\n" + "="*60)
    print("JAVIS RAG BACKEND COMPARISON: FAISS vs LEANN")
    print("="*60)
    print(f"\nCodebase: {codebase_dir}")
    
    # Create temp storage dir
    storage_dir = "/tmp/javis_rag_benchmark"
    os.makedirs(storage_dir, exist_ok=True)
    
    results = {}
    
    # Benchmark FAISS
    try:
        results["faiss"] = benchmark_backend(
            "faiss", 
            codebase_dir, 
            "benchmark_faiss",
            storage_dir
        )
    except Exception as e:
        print(f"\nFAISS benchmark failed: {e}")
        results["faiss"] = {"success": False, "error": str(e)}
    
    # Benchmark LEANN
    try:
        results["leann"] = benchmark_backend(
            "leann",
            codebase_dir,
            "benchmark_leann", 
            storage_dir
        )
    except Exception as e:
        print(f"\nLEANN benchmark failed: {e}")
        results["leann"] = {"success": False, "error": str(e)}
    
    # Print comparison
    print(f"\n{'='*60}")
    print("COMPARISON SUMMARY")
    print(f"{'='*60}\n")
    
    if results["faiss"]["success"] and results["leann"]["success"]:
        faiss = results["faiss"]
        leann = results["leann"]
        
        print(f"{'Metric':<30} {'FAISS':<15} {'LEANN':<15} {'Savings':<15}")
        print(f"{'-'*75}")
        
        # Index size comparison
        storage_savings = (1 - leann["index_size_mb"] / faiss["index_size_mb"]) * 100
        print(f"{'Index Size':<30} {faiss['index_size_mb']:.2f} MB{'':<6} {leann['index_size_mb']:.2f} MB{'':<6} {storage_savings:.1f}%")
        
        # Build time
        print(f"{'Build Time':<30} {faiss['build_time']:.2f}s{'':<9} {leann['build_time']:.2f}s")
        
        # Query time
        print(f"{'Avg Query Time':<30} {faiss['avg_query_time_ms']:.0f}ms{'':<10} {leann['avg_query_time_ms']:.0f}ms")
        
        print(f"\n{'='*75}")
        print(f"🎉 LEANN saves {storage_savings:.1f}% storage compared to FAISS!")
        print(f"{'='*75}")
    else:
        print("⚠️  Could not complete comparison due to errors")
        for backend, result in results.items():
            if not result["success"]:
                print(f"   {backend.upper()}: {result.get('error', 'Unknown error')}")
    
    # Cleanup
    print(f"\n💡 Benchmark files saved to: {storage_dir}")
    print(f"   To clean up: rm -rf {storage_dir}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Compare FAISS vs LEANN backends")
    parser.add_argument(
        "codebase_dir",
        nargs="?",
        default=os.getenv("src_dir", "/home/worker/src/codefun/deepl/javis_agent/javis"),
        help="Path to codebase directory (default: from src_dir env or javis source)"
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.codebase_dir):
        print(f"❌ Error: Directory not found: {args.codebase_dir}")
        sys.exit(1)
    
    print("\n📦 Installing dependencies...")
    print("   Make sure you have installed:")
    print("   - For FAISS: pip install langchain langchain-community faiss-cpu")
    print("   - For LEANN: pip install leann")
    
    compare_backends(args.codebase_dir)
