from typing import List, Optional
from langchain.chains import ConversationalRetrievalChain
from langchain_ollama import ChatOllama
from langchain.memory import ConversationBufferMemory
from langchain.schema import Document

from config import OLLAMA_BASE_URL, OLLAMA_MODEL, TOP_K
from knowledge_base import KnowledgeBase

SYSTEM_PROMPT = """你是一个专业的问答助手，基于提供的参考文档回答用户问题。

回答规则：
1. 如果文档中有相关信息，基于文档内容给出准确答案
2. 如果文档中没有相关信息，明确回复"文档中未找到相关答案"
3. 在回答时，可以引用文档中的具体内容来支持你的答案
4. 保持回答清晰、简洁、有条理

请始终遵循以上规则。"""

class RAGChain:
    def __init__(self, knowledge_base: KnowledgeBase):
        self.knowledge_base = knowledge_base
        self.llm = ChatOllama(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=0.7,
            verbose=True
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            output_key="answer",
            return_messages=True
        )
        self.chain = None
        self._build_chain()

    def _build_chain(self):
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.knowledge_base.vector_store.as_retriever(
                search_kwargs={"k": TOP_K}
            ),
            memory=self.memory,
            combine_docs_chain_kwargs={"prompt": self._get_prompt()},
            return_source_documents=True,
            verbose=True
        )

    def _get_prompt(self):
        from langchain.prompts import Prompt
        from langchain.prompts.chat import HumanMessagePromptTemplate, SystemMessagePromptTemplate

        system_template = SYSTEM_PROMPT + """

参考文档:
{context}
"""
        human_template = "{question}"

        return Prompt(
            input_variables=["context", "question"],
            template=system_template + "\n\n" + human_template
        )

    def ask(self, question: str) -> dict:
        if not self.chain:
            return {
                "answer": "知识库未初始化，请先构建知识库",
                "source_documents": [],
                "has_context": False
            }

        try:
            result = self.chain({"question": question})
            answer = result.get("answer", "")
            source_docs = result.get("source_documents", [])

            has_context = len(source_docs) > 0 and any(
                len(doc.page_content.strip()) > 0 for doc in source_docs
            )

            return {
                "answer": answer,
                "source_documents": source_docs,
                "has_context": has_context
            }
        except Exception as e:
            return {
                "answer": f"查询出错: {str(e)}",
                "source_documents": [],
                "has_context": False
            }

    def chat(self, question: str) -> str:
        result = self.ask(question)
        return result["answer"]

    def get_source_content(self, source_docs: List[Document]) -> List[str]:
        contents = []
        for doc in source_docs:
            content = doc.page_content.strip()
            if content:
                contents.append(content)
        return contents

    def clear_memory(self):
        self.memory.clear()
        print("对话历史已清空")

def test_rag_chain():
    print("=" * 50)
    print("RAG问答链测试")
    print("=" * 50)

    print("\n初始化知识库...")
    kb = KnowledgeBase()
    stats = kb.get_stats()
    print(f"知识库状态: {stats}")

    print("\n初始化RAG问答链...")
    rag = RAGChain(kb)

    test_questions = [
        "什么是自然语言处理？",
        "深度学习在NLP中有哪些应用？",
        "Transformer模型的工作原理是什么？",
        "Python和Java有什么区别？",
        "如何学习机器学习？"
    ]

    print("\n" + "=" * 50)
    print("问答测试")
    print("=" * 50)

    for i, question in enumerate(test_questions, 1):
        print(f"\n问题 {i}: {question}")
        print("-" * 40)
        result = rag.ask(question)
        print(f"回答: {result['answer'][:300]}...")
        if result['source_documents']:
            print(f"参考文档数: {len(result['source_documents'])}")
        print(f"有上下文支撑: {'是' if result['has_context'] else '否'}")

if __name__ == "__main__":
    test_rag_chain()