# B层语义聚合系统

B层是主动辅助系统的语义聚合层，将A层的原始感知事件聚合成语义事件。

## 快速开始

### 1. 安装依赖

```bash
cd b_layer
pip install -r requirements.txt
```

### 2. 配置LLM API

编辑 `config.json`，填入你的LLM API信息：

```json
{
  "llm_api_url": "https://api.openai.com/v1/chat/completions",
  "llm_api_key": "your-api-key-here",
  "model": "gpt-4"
}
```

### 3. 运行

```bash
python b_layer.py
```

程序会读取 `../events/A.jsonl`，输出到 `../events/B.jsonl`。

## 功能特性

- **增量式人物识别**：基于face embedding自动识别和追踪人物
- **动态窗口聚合**：根据事件变化智能切分语义事件
- **上下文感知**：维护场景和活动状态，生成完整语义摘要
- **LLM集成**：调用大模型生成自然语言摘要和对话行为分类

## 配置说明

- `face_similarity_threshold`: 人脸匹配阈值（默认0.75）
- `min_window_seconds`: 最小窗口时长（默认2秒）
- `max_window_seconds`: 最大窗口时长（默认30秒）
- `person_change_delay`: 人物变化延迟（默认3秒）
