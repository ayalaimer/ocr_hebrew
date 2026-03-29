"""
Protocol Genesis — Pipeline Orchestrator
Usage: python main.py
Runs from within the ocr/ directory (where this file lives).
"""
import os
import sys

# Pin the working directory to this file's location so all relative
# paths (test_pdf/, test_files_json/, chunks.json) resolve correctly
# regardless of where the caller invoked Python from.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

from dotenv import load_dotenv
load_dotenv(os.path.join(BASE_DIR, ".env"))


# ==========================================
#  Pipeline steps (thin wrappers)
# ==========================================

def run_step1_ocr():
    print("\n" + "=" * 50)
    print("  Step 1: OCR  (PDF/images → JSON)")
    print("=" * 50)
    from run_ocr import main as ocr_main
    ocr_main()


def run_step2_chunking():
    print("\n" + "=" * 50)
    print("  Step 2: Chunking  (JSON → chunks.json)")
    print("=" * 50)
    from chunker import process_directory
    input_dir = os.path.join(BASE_DIR, "test_files_json")
    output_file = os.path.join(BASE_DIR, "chunks.json")
    process_directory(input_dir, output_file)


def run_step3_rag():
    print("\n" + "=" * 50)
    print("  Step 3: RAG — Interactive Q&A")
    print("=" * 50)
    if not os.getenv("GROQ_API_KEY"):
        print("Error: GROQ_API_KEY is not set.")
        print("Create a .env file in this directory with:  GROQ_API_KEY=your_key_here")
        return
    from rag_pipeline import run_interactive
    run_interactive()


# ==========================================
#  CLI menu
# ==========================================

def print_menu():
    print("\n" + "=" * 50)
    print("  Protocol Genesis — Pipeline Menu")
    print("=" * 50)
    print("  1.  OCR           (PDF/images → JSON)")
    print("  2.  Chunk         (JSON → chunks.json)")
    print("  3.  RAG Q&A       (Interactive mode)")
    print("  4.  Full pipeline (1 → 2 → 3)")
    print("  0.  Exit")
    print("=" * 50)


if __name__ == "__main__":
    while True:
        print_menu()
        choice = input("Select an option [0-4]: ").strip()
        if choice == "1":
            run_step1_ocr()
        elif choice == "2":
            run_step2_chunking()
        elif choice == "3":
            run_step3_rag()
        elif choice == "4":
            run_step1_ocr()
            run_step2_chunking()
            run_step3_rag()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid choice, please enter 0–4.")
