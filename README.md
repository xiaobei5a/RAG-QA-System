# RAG智能问答系统

基于本地文档的智能问答系统，使用Ollama本地大模型、LangChain框架和Streamlit构建。

## 项目简介

本项目实现了一个RAG(检索增强生成)问答系统，能够"学习"用户上传的PDF/DOCX文档，并基于这些文档回答用户提问。系统使用Ollama部署的DeepSeek-R1模型进行推理，ChromaDB存储文档向量，支持多轮对话。

## 环境要求

### 软件要求
- Python 3.9+
- Ollama (已安装并运行)
- Windows 10/11

### 依赖安装

1. 安装Python依赖包:
```bash
pip install -r requirements.txt
```

2. 安装并配置Ollama:
```bash
# 下载安装Ollama (Windows版)
# https://ollama.com/download

# 启动Ollama服务
ollama serve

# 下载大模型
ollama pull deepseek-r1:7b

# 下载嵌入模型
ollama pull nomic-embed-text
```

## 使用说明

### 1. 启动Web应用

```bash
streamlit run app.py
```

应用将在浏览器中打开(默认地址: http://localhost:8501)

### 2. 上传文档

- 点击"选择文件"按钮
- 选择PDF或DOCX格式的文档
- 支持批量上传多个文件
- 系统自动解析文档并构建知识库

### 3. 提问

- 在文本框中输入问题
- 点击"提问"按钮获取答案
- 系统会显示参考文档片段
- 支持多轮对话，上下文会被记住

### 4. 命令行版本

如果只想使用命令行版本:

```bash
# 测试Ollama连接
python test_ollama.py

# 构建知识库(需要将文档放入sample_documents文件夹)
python knowledge_base.py

# 运行RAG问答
python rag_chain.py
```

## 关键技术点

### RAG流程
1. **文档加载**: 使用PyPDFLoader和Docx2txtLoader读取文档
2. **文本分割**: 使用RecursiveCharacterTextSplitter分块(chunk_size=1000, overlap=200)
3. **向量化**: 使用Ollama的nomic-embed-text模型生成嵌入向量
4. **存储检索**: 使用ChromaDB向量数据库存储和检索相似文档
5. **生成回答**: 使用ConversationalRetrievalChain结合检索结果和LLM生成答案

### 所用模型
- **大语言模型**: DeepSeek-R1:7B (通过Ollama部署)
- **嵌入模型**: nomic-embed-text (Ollama内置)

### 技术栈
- LangChain & LangChain-Community
- ChromaDB (向量数据库)
- Streamlit (Web界面)
- Ollama (本地模型服务)

## 项目结构

```
.
├── app.py              # Streamlit Web应用
├── config.py           # 配置文件
├── test_ollama.py      # Ollama连接测试
├── knowledge_base.py   # 知识库构建模块
├── rag_chain.py        # RAG问答链模块
├── build_exe.py        # PyInstaller打包脚本
├── requirements.txt    # Python依赖
├── README.md           # 本文件
├── AI_usage_log.md     # AI使用日志
└── sample_documents/   # 示例文档文件夹(需创建)
```

## 已知问题与改进方向

### 已知问题
1. 首次加载文档时，向量化过程可能较慢
2. 需要Ollama服务持续运行
3. 暂不支持中文文档的精确分句

### 改进方向
1. 添加更多文档格式支持(如TXT、MD)
2. 增加夜间模式
3. 支持批量上传和导出问答记录
4. 优化嵌入模型选择(如使用OpenAI的text-embedding-ada-002)
5. 添加文档管理功能(删除、重命名等)

## 许可证

本项目仅供学习交流使用。