import os
from typing import List
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.vectorstores import Chroma
import chromadb

from config import (
    OLLAMA_BASE_URL,
    EMBEDDING_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    PERSIST_DIRECTORY
)

class KnowledgeBase:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(
            model=EMBEDDING_MODEL,
            base_url=OLLAMA_BASE_URL
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
        )
        self.vector_store = None
        self._init_vector_store()

    def _init_vector_store(self):
        if os.path.exists(PERSIST_DIRECTORY):
            try:
                self.vector_store = Chroma(
                    persist_directory=PERSIST_DIRECTORY,
                    embedding_function=self.embeddings
                )
                print(f"✓ 已加载现有知识库，当前文档数量: {self.vector_store._collection.count()}")
            except Exception as e:
                print(f"加载现有知识库失败: {e}，将创建新的知识库")
                self.vector_store = None

        if self.vector_store is None:
            os.makedirs(PERSIST_DIRECTORY, exist_ok=True)
            self.vector_store = Chroma(
                persist_directory=PERSIST_DIRECTORY,
                embedding_function=self.embeddings
            )
            print("✓ 已创建新的知识库")

    def load_document(self, file_path: str) -> List[Document]:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
        elif ext == ".docx":
            loader = Docx2txtLoader(file_path)
        else:
            raise ValueError(f"不支持的文件格式: {ext}")

        documents = loader.load()
        print(f"  成功加载文档: {os.path.basename(file_path)}, 页数: {len(documents)}")
        return documents

    def process_documents(self, documents: List[Document]) -> List[Document]:
        chunks = self.text_splitter.split_documents(documents)
        print(f"  文本分块完成，块数: {len(chunks)}")
        return chunks

    def add_documents(self, file_paths: List[str]) -> int:
        all_chunks = []
        for file_path in file_paths:
            try:
                documents = self.load_document(file_path)
                chunks = self.process_documents(documents)
                all_chunks.extend(chunks)
            except Exception as e:
                print(f"  处理文件失败 {file_path}: {e}")

        if all_chunks:
            self.vector_store.add_documents(documents=all_chunks)
            print(f"✓ 已添加 {len(all_chunks)} 个文本块到知识库")

        return len(all_chunks)

    def add_single_document(self, file_path: str) -> int:
        return self.add_documents([file_path])

    def search(self, query: str, top_k: int = 3) -> List[Document]:
        results = self.vector_store.similarity_search(query=query, k=top_k)
        return results

    def get_stats(self) -> dict:
        if self.vector_store:
            count = self.vector_store._collection.count()
            return {"document_count": count}
        return {"document_count": 0}

    def clear(self):
        if os.path.exists(PERSIST_DIRECTORY):
            import shutil
            shutil.rmtree(PERSIST_DIRECTORY)
            os.makedirs(PERSIST_DIRECTORY)
        self.vector_store = Chroma(
            persist_directory=PERSIST_DIRECTORY,
            embedding_function=self.embeddings
        )
        print("✓ 知识库已清空")

def build_knowledge_base_from_folder(folder_path: str) -> KnowledgeBase:
    kb = KnowledgeBase()
    supported_extensions = [".pdf", ".docx"]
    file_paths = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in supported_extensions):
                file_paths.append(os.path.join(root, file))

    if file_paths:
        print(f"发现 {len(file_paths)} 个文档文件")
        kb.add_documents(file_paths)
    else:
        print(f"在 {folder_path} 中未找到文档文件")

    return kb

if __name__ == "__main__":
    print("=" * 50)
    print("知识库构建测试")
    print("=" * 50)

    documents_folder = "./sample_documents"
    if os.path.exists(documents_folder):
        kb = build_knowledge_base_from_folder(documents_folder)
        stats = kb.get_stats()
        print(f"\n知识库统计: {stats}")

        print("\n检索测试:")
        results = kb.search("自然语言处理的基本概念", top_k=3)
        for i, doc in enumerate(results):
            print(f"\n结果 {i+1}:")
            print(f"  {doc.page_content[:200]}...")
    else:
        print(f"示例文档文件夹不存在: {documents_folder}")