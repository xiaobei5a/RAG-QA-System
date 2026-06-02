import PyInstaller.__main__
import os
import shutil

def build_exe():
    print("=" * 50)
    print("开始打包RAG问答系统")
    print("=" * 50)

    project_root = os.path.dirname(os.path.abspath(__file__))
    dist_dir = os.path.join(project_root, "dist")

    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)

    pyinstaller_args = [
        "app.py",
        "--name=RAG-QA-System",
        "--onefile",
        "--windowed",
        "--icon=NONE",
        f"--distpath={dist_dir}",
        "--add-data=.;.",
        "--hidden-import=streamlit",
        "--hidden-import=langchain",
        "--hidden-import=langchain_community",
        "--hidden-import=langchain_ollama",
        "--hidden-import=chromadb",
        "--hidden-import=pypdf2",
        "--hidden-import=docx2txt",
        "--hidden-import=tiktoken",
        "--hidden-import=ollama",
        "--hidden-import=requests",
        "--collect-all=chromadb",
        "--collect-all=langchain",
        "--collect-all=streamlit",
    ]

    print("运行 PyInstaller...")
    PyInstaller.__main__.run(pyinstaller_args)

    exe_path = os.path.join(dist_dir, "RAG-QA-System.exe")
    if os.path.exists(exe_path):
        print(f"\n✓ 打包成功!")
        print(f"exe文件位置: {exe_path}")
    else:
        print("\n✗ 打包失败，exe文件未生成")

if __name__ == "__main__":
    build_exe()