# AI使用日志

## 项目: RAG智能问答系统

### 概述
本项目使用AI编程辅助工具(Trae)帮助生成代码骨架、调试错误、优化提示词。

### AI使用记录

#### 1. 项目结构设计
- **询问**: 如何组织RAG项目的代码结构？
- **AI建议**: 按照任务划分模块，config.py统一配置，knowledge_base.py处理文档，rag_chain.py处理问答链，app.py处理Web界面
- **修改记录**: 采用建议，添加了配置文件分离关注点

#### 2. LangChain ConversationalRetrievalChain使用
- **询问**: 如何正确使用LangChain的ConversationalRetrievalChain？
- **AI建议**: 需要配置memory、retriever和combine_docs_chain的prompt
- **代码修改**: 按照AI建议实现了SYSTEM_PROMPT和自定义prompt模板

#### 3. ChromaDB持久化问题
- **问题**: ChromaDB持久化目录加载失败
- **询问**: 如何正确加载已持久化的ChromaDB？
- **AI建议**: 使用persist_directory和embedding_function参数
- **修改记录**: 修改了_init_vector_store方法

#### 4. Streamlit会话状态管理
- **询问**: 如何在Streamlit中管理RAG系统的会话状态？
- **AI建议**: 使用st.session_state存储knowledge_base和rag_chain实例
- **修改记录**: 在app.py中添加了init_session_state函数

#### 5. 文档加载器选择
- **询问**: LangChain支持哪些文档格式？
- **AI回复**: PyPDFLoader支持PDF，Docx2txtLoader支持DOCX
- **修改记录**: 选择了这两个加载器

### 问题解决记录

1. **问题**: ChromaDB向量化速度慢
   - **解决**: 使用Ollama内置的nomic-embed-text嵌入模型，本地执行

2. **问题**: 模型推理超时
   - **解决**: 设置合理的timeout参数，增加错误处理

3. **问题**: Streamlit文件上传大小限制
   - **解决**: 使用file_uploader的accept_multiple_files参数支持批量上传

### 备注
- 所有AI生成的代码都经过理解和修改，确保符合项目需求
- 关键业务逻辑和配置参数由人工确认和调整
- 遵循课程要求的代码注释规范