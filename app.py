import streamlit as st
import os
from knowledge_base import KnowledgeBase
from rag_chain import RAGChain
from config import UPLOAD_DIRECTORY

st.set_page_config(
    page_title="RAG智能问答系统",
    page_icon="📚",
    layout="wide"
)

def init_session_state():
    if 'kb' not in st.session_state:
        st.session_state.kb = KnowledgeBase()
    if 'rag' not in st.session_state:
        st.session_state.rag = RAGChain(st.session_state.kb)
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_files' not in st.session_state:
        st.session_state.current_files = set()

def save_uploaded_file(uploaded_file):
    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIRECTORY, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def display_chat_history():
    for i, (q, a) in enumerate(st.session_state.chat_history):
        with st.container():
            st.markdown(f"**你:** {q}")
            st.markdown(f"**助手:** {a}")
            st.markdown("---")

def main():
    init_session_state()

    st.title("📚 RAG智能问答系统")
    st.markdown("基于本地文档的智能问答助手 - 使用Ollama + LangChain + Streamlit构建")

    with st.sidebar:
        st.header("📊 知识库状态")
        stats = st.session_state.kb.get_stats()
        st.metric("文档块数量", stats.get("document_count", 0))

        st.header("⚙️ 功能")
        if st.button("🔄 重新初始化知识库"):
            st.session_state.kb = KnowledgeBase()
            st.session_state.rag = RAGChain(st.session_state.kb)
            st.session_state.chat_history = []
            st.session_state.current_files = set()
            st.rerun()

        if st.button("🗑️ 清空知识库"):
            st.session_state.kb.clear()
            st.session_state.rag = RAGChain(st.session_state.kb)
            st.session_state.chat_history = []
            st.session_state.current_files = set()
            st.rerun()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("💬 问答交互")

        with st.container(border=True):
            st.subheader("📄 上传文档")
            uploaded_files = st.file_uploader(
                "选择PDF或DOCX文件",
                type=["pdf", "docx"],
                accept_multiple_files=True,
                help="支持批量上传多个文件"
            )

            if uploaded_files:
                new_files = [f for f in uploaded_files if f.name not in st.session_state.current_files]
                if new_files:
                    for uploaded_file in new_files:
                        with st.spinner(f"正在处理 {uploaded_file.name}..."):
                            try:
                                file_path = save_uploaded_file(uploaded_file)
                                st.session_state.kb.add_single_document(file_path)
                                st.session_state.current_files.add(uploaded_file.name)
                                st.success(f"✓ {uploaded_file.name} 已添加")
                            except Exception as e:
                                st.error(f"✗ 处理 {uploaded_file.name} 失败: {e}")

        st.subheader("💭 提问")
        question = st.text_input("请输入您的问题:", placeholder="例如：文档中关于什么内容？", key="question_input")

        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            ask_button = st.button("🚀 提问", type="primary", use_container_width=True)
        with col_btn2:
            clear_button = st.button("🗑️ 清空历史", use_container_width=True)

        if clear_button:
            st.session_state.chat_history = []
            st.session_state.rag.clear_memory()
            st.rerun()

        if ask_button and question:
            with st.spinner("正在思考..."):
                result = st.session_state.rag.ask(question)
                answer = result["answer"]

                if not result["has_context"]:
                    answer = "文档中未找到相关答案。"

                st.session_state.chat_history.append((question, answer))

                if result["source_documents"]:
                    with st.expander("📑 参考文档片段"):
                        for i, doc in enumerate(result["source_documents"], 1):
                            st.markdown(f"**片段 {i}:**")
                            st.text(doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content)

        if st.session_state.chat_history:
            st.subheader("📝 对话历史")
            display_chat_history()

    with col2:
        st.header("📋 使用说明")
        st.markdown("""
        1. **上传文档**: 通过左侧上传PDF或DOCX文件
        2. **构建知识库**: 文件会自动解析并添加到向量数据库
        3. **提问**: 输入问题，系统会基于已上传文档回答
        4. **查看参考**: 可展开查看答案的参考文档片段

        **注意**:
        - 支持多轮对话，会记住上下文
        - 如果文档中没有相关信息，系统会明确告知
        """)

        st.header("🔧 系统信息")
        st.info(f"""
        **配置信息**:
        - 模型: deepseek-r1:7b
        - 嵌入模型: nomic-embed-text
        - 向量数据库: ChromaDB
        - Chunk大小: 1000
        - Top-K: 3
        """)

if __name__ == "__main__":
    main()