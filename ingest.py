#!/usr/bin/env python3
import os
import glob
import argparse
from typing import List
from dotenv import load_dotenv
from multiprocessing import Pool
from tqdm import tqdm

from langchain.document_loaders import (
    CSVLoader,
    EverNoteLoader,
    PyMuPDFLoader,
    TextLoader,
    UnstructuredEmailLoader,
    UnstructuredEPubLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredODTLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
)

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document

from chromadb.config import Settings
import chromadb


# Custom document loaders
class MyElmLoader(UnstructuredEmailLoader):
    """Wrapper to fallback to text/plain when default does not work"""

    def load(self) -> List[Document]:
        """Wrapper adding fallback for elm without html"""
        try:
            try:
                doc = UnstructuredEmailLoader.load(self)
            except ValueError as e:
                if 'text/html content not found in email' in str(e):
                    # Try plain text
                    self.unstructured_kwargs["content_source"] = "text/plain"
                    doc = UnstructuredEmailLoader.load(self)
                else:
                    raise
        except Exception as e:
            # Add file_path to exception message
            raise type(e)(f"{self.file_path}: {e}") from e

        return doc


# Map file extensions to document loaders and their arguments
LOADER_MAPPING = {
    ".csv": (CSVLoader, {}),
    # ".docx": (Docx2txtLoader, {}),
    ".doc": (UnstructuredWordDocumentLoader, {}),
    ".docx": (UnstructuredWordDocumentLoader, {}),
    ".enex": (EverNoteLoader, {}),
    ".eml": (MyElmLoader, {}),
    ".epub": (UnstructuredEPubLoader, {}),
    ".html": (UnstructuredHTMLLoader, {}),
    ".md": (UnstructuredMarkdownLoader, {}),
    ".odt": (UnstructuredODTLoader, {}),
    ".pdf": (PyMuPDFLoader, {}),
    ".ppt": (UnstructuredPowerPointLoader, {}),
    ".pptx": (UnstructuredPowerPointLoader, {}),
    ".txt": (TextLoader, {"encoding": "utf8"}),
    # Add more mappings for other file extensions and loaders as needed
}


def load_single_document(file_path: str) -> List[Document]:
    ext = "." + file_path.rsplit(".", 1)[-1].lower()
    if ext in LOADER_MAPPING:
        loader_class, loader_args = LOADER_MAPPING[ext]
        loader = loader_class(file_path, **loader_args)
        return loader.load()

    raise ValueError(f"Unsupported file extension '{ext}'")


def load_documents(source_dir: str, ignored_files: List[str] = []) -> List[Document]:
    """
    Loads all documents from the source documents directory, ignoring specified files
    """
    all_files = []
    for ext in LOADER_MAPPING:
        all_files.extend(
            glob.glob(os.path.join(
                source_dir, f"**/*{ext.lower()}"), recursive=True)
        )
        all_files.extend(
            glob.glob(os.path.join(
                source_dir, f"**/*{ext.upper()}"), recursive=True)
        )
    filtered_files = [
        file_path for file_path in all_files if file_path not in ignored_files]

    with Pool(processes=os.cpu_count()) as pool:
        results = []
        with tqdm(total=len(filtered_files), desc='Loading new documents', ncols=80) as pbar:
            for i, docs in enumerate(pool.imap_unordered(load_single_document, filtered_files)):
                results.extend(docs)
                pbar.update()

    return results


def process_documents(
    source_directory: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    ignored_files: List[str] = []
) -> List[Document]:
    """
    Load documents and split in chunks
    """
    print(f"Loading documents from {source_directory}")
    documents = load_documents(source_directory, ignored_files)
    if not documents:
        print("No new documents to load")
        exit(0)
    print(f"Loaded {len(documents)} new documents from {source_directory}")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    texts = text_splitter.split_documents(documents)
    print(
        f"Split into {len(texts)} chunks of text (max. {chunk_size} tokens each)")
    return texts


def does_vectorstore_exist(persist_directory: str, embeddings: HuggingFaceEmbeddings) -> bool:
    """
    Checks if vectorstore exists
    """
    db = Chroma(persist_directory=persist_directory,
                embedding_function=embeddings)
    if not db.get()['documents']:
        return False
    return True


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Ingest documents to vectorstore.")

    parser.add_argument("-cs", "--chunk-size",
                        type=int,
                        help="Chunk size when splitting documents.")

    parser.add_argument("-co", "--chunk-overlap",
                        type=int,
                        help="Chunk overlap size when splitting documents with multiple chunks.")

    parser.add_argument("-n", "--model-name",
                        type=str,
                        help="Use this flag to disable the streaming StdOut callback for LLMs.")

    parser.add_argument("-p", "--persist-directory",
                        type=str,
                        help="Directory to store embedding vector store.")

    parser.add_argument("-s", "--source-directory",
                        type=str,
                        help='Directory to recursively read documents from.')

    return parser.parse_args()


def main():
    if not load_dotenv():
        print("Could not load .env file or it is empty. Please check if it exists and is readable.")
        exit(1)

    args = parse_arguments()

    embeddings_model_name = args.model_name or os.environ.get(
        'EMBEDDINGS_MODEL_NAME',
        "all-MiniLM-L6-v2"
    )
    persist_directory = args.persist_directory or os.environ.get(
        'PERSIST_DIRECTORY',
        'vectorstore/'
    )
    source_directory = args.source_directory or os.environ.get(
        'SOURCE_DIRECTORY',
        'source_documents/'
    )
    chunk_size = args.chunk_size or os.environ.get(
        'CHUNK_SIZE',
        500
    )
    chunk_overlap = args.chunk_overlap or os.environ.get(
        'CHUNK_OVERLAP',
        50
    )
    # REMINDER: can add ignored files

    CHROMA_SETTINGS = Settings(
        persist_directory=persist_directory,
        anonymized_telemetry=False
    )

    # Create embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name=embeddings_model_name
    )
    # Chroma client
    chroma_client = chromadb.PersistentClient(
        settings=CHROMA_SETTINGS,
        path=persist_directory
    )

    if does_vectorstore_exist(persist_directory, embeddings):
        # Update and store locally vectorstore
        print(f"Appending to existing vectorstore at {persist_directory}")
        db = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings,
            client_settings=CHROMA_SETTINGS,
            client=chroma_client
        )
        collection = db.get()
        texts = process_documents(
            source_directory=source_directory,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            ignored_files=[metadata['source']
                           for metadata in collection['metadatas']]
        )
        print(f"Creating embeddings. May take some minutes...")
        db.add_documents(texts)

    else:
        # Create and store locally vectorstore
        print("Creating new vectorstore")
        texts = process_documents(
            source_directory=source_directory,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            ignored_files=[]
        )
        print(f"Creating embeddings. May take some minutes...")
        db = Chroma.from_documents(
            texts, embeddings,
            persist_directory=persist_directory,
            client_settings=CHROMA_SETTINGS,
            client=chroma_client
        )

    db.persist()
    db = None

    print(f"Ingestion complete! You can now run privateGPT.py to query your documents")


if __name__ == "__main__":
    main()
