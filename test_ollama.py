import requests
import sys
from config import OLLAMA_BASE_URL, OLLAMA_MODEL

def test_ollama_connection():
    print(f"Testing Ollama connection to {OLLAMA_BASE_URL}...")
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=10)
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"✓ Ollama服务连接成功!")
            print(f"可用模型数量: {len(models)}")
            if models:
                print("已安装的模型:")
                for model in models:
                    print(f"  - {model.get('name', 'unknown')}")
            return True
        else:
            print(f"✗ Ollama返回异常状态码: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"✗ 无法连接到Ollama服务，请确保Ollama已在本地运行")
        print(f"  提示: 在终端运行 'ollama serve' 启动服务")
        return False
    except Exception as e:
        print(f"✗ 连接错误: {str(e)}")
        return False

def test_model_inference():
    print(f"\n测试模型推理: {OLLAMA_MODEL}")
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": "你好，请用一句话介绍一下自己",
            "stream": False
        }
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json=payload,
            timeout=60
        )
        if response.status_code == 200:
            result = response.json()
            print(f"✓ 模型推理成功!")
            print(f"回答: {result.get('response', '')[:200]}...")
            return True
        else:
            print(f"✗ 模型推理失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ 推理错误: {str(e)}")
        return False

def test_embedding():
    print(f"\n测试嵌入模型: nomic-embed-text")
    try:
        payload = {
            "model": "nomic-embed-text",
            "prompt": "这是一个测试文本"
        }
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/embeddings",
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            result = response.json()
            embedding = result.get("embedding", [])
            print(f"✓ 嵌入模型工作正常!")
            print(f"嵌入向量维度: {len(embedding)}")
            return True
        else:
            print(f"✗ 嵌入模型测试失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ 嵌入错误: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Ollama API 测试脚本")
    print("=" * 50)

    connection_ok = test_ollama_connection()

    if connection_ok:
        test_model_inference()
        test_embedding()

    print("\n" + "=" * 50)
    if connection_ok:
        print("测试完成!")
        sys.exit(0)
    else:
        print("测试未完全通过，请检查Ollama配置")
        sys.exit(1)