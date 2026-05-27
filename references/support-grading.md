# 支撑度评估指南

## 目录

- [1. 支撑度浮点评分标准](#1-支撑度浮点评分标准)
- [2. 各分数段判断标准与示例](#2-各分数段判断标准与示例)
- [3. 摘要与声明的比对方法](#3-摘要与声明的比对方法)
- [4. unverified 论文的处理规则](#4-unverified-论文的处理规则)

---

## 1. 支撑度浮点评分标准

支撑度由 LLM 输出 0~1 连续浮点数，不使用离散标签。

| 分数段 | 含义 | 对应旧标签（仅供参考） |
|--------|------|----------------------|
| 0.9–1.0 | 摘要直接描述了声明中的关系/方法/结果 | strong |
| 0.6–0.8 | 相关但未直接验证声明的具体论断 | partial |
| 0.3–0.5 | 提供领域背景，不直接支撑声明 | background |
| 0.0–0.2 | 矛盾或无法判断（如缺摘要） | contradictory / unverified |

评分由 `support_llm.py` 调用 LLM 自动完成，agent 不手动打分。

---

## 2. 各分数段判断标准与示例

### 2.1 0.9–1.0（直接验证）

**判断标准**：
- 摘要明确描述了声明中提到的关系
- 摘要直接验证了声明中的方法或结果
- 论文的核心贡献就是声明所表述的内容

**示例**：

声明："Deep learning has achieved remarkable success in protein structure prediction."

| 论文 | 摘要关键内容 | 评分 |
|------|------------|------|
| AlphaFold (Jumper et al., 2021) | "we present AlphaFold, a system that achieves atomic-level accuracy in protein structure prediction" | 0.95 |
| RoseTTAFold (Baek et al., 2021) | "we describe RoseTTAFold, a three-track neural network that achieves accuracy approaching that of AlphaFold" | 0.90 |

声明："Transformer architecture outperforms RNNs in machine translation."

| 论文 | 摘要关键内容 | 评分 |
|------|------------|------|
| Attention Is All You Need (Vaswani et al., 2017) | "we propose a new simple network architecture, the Transformer, based solely on attention mechanisms...on two machine translation tasks...outperforming the best existing models" | 0.95 |

### 2.2 0.6–0.8（相关但未直接验证）

**判断标准**：
- 摘要与声明主题相关，但未直接验证声明的具体论断
- 论文涉及相同领域/方法，但关注点不同
- 声明中的部分内容可从摘要推断，但未明确陈述

**示例**：

声明："Graph neural networks are effective for molecular property prediction."

| 论文 | 摘要关键内容 | 评分 |
|------|------------|------|
| GNN综述 (Zhou et al., 2020) | "we provide a comprehensive review of graph neural networks...covering various applications" | 0.65（综述提及应用，但未专门验证分子性质预测的效果） |
| 某GNN变体论文 | "we propose a new message passing scheme that improves node classification on citation networks" | 0.60（GNN方法相关，但应用领域不同） |

### 2.3 0.3–0.5（背景知识）

**判断标准**：
- 论文提供领域背景知识，但不直接支撑声明
- 论文是该领域的早期/奠基工作，但声明涉及的是后续发展
- 论文定义了声明中使用的概念或术语

**示例**：

声明："Pre-trained language models have revolutionized NLP."

| 论文 | 摘要关键内容 | 评分 |
|------|------------|------|
| Word2Vec (Mikolov et al., 2013) | "we propose two novel model architectures for learning continuous representations of words" | 0.35（词嵌入是基础，但不是预训练语言模型） |
| Neural NLM (Bengio et al., 2003) | "we propose a neural network language model" | 0.30（早期工作，提供背景但不直接支撑"revolutionized"的论断） |

### 2.4 0.0–0.2（矛盾或无法判断）

**判断标准**：
- 摘要内容与声明直接矛盾 → 0.0–0.1
- 未能获取摘要文本，仅基于标题/元数据判断 → 0.2
- API 返回的摘要为空或不可用 → 0.2

**示例**：

声明："Increasing model size consistently improves performance."

| 论文 | 摘要关键内容 | 评分 |
|------|------------|------|
| 某缩放定律论文 | "we find that performance plateaus or degrades beyond a certain model size due to data limitations" | 0.05（矛盾） |
| 标题相关但无摘要 | — | 0.2（unverified） |

---

## 3. 摘要与声明的比对方法

### 3.1 比对维度

| 维度 | 说明 | 权重 |
|------|------|------|
| 主题匹配 | 摘要主题是否与声明一致 | 高 |
| 关系验证 | 摘要是否验证了声明中的因果关系/比较关系 | 高 |
| 方法匹配 | 摘要中的方法是否与声明提及的方法一致 | 中 |
| 结果匹配 | 摘要中的结果是否支持声明的论断 | 高 |
| 领域匹配 | 论文领域是否与声明领域一致 | 中 |

### 3.2 比对流程

```
输入：声明文本 + 论文摘要
处理：
  1. 提取声明的核心要素：
     - 主体（什么方法/对象）
     - 关系（做了什么/效果如何）
     - 条件（在什么场景下）

  2. 提取摘要的核心要素：
     - 研究问题
     - 提出方法
     - 主要结果
     - 结论

  3. 逐要素比对：
     - 主体匹配？→ 主题匹配度
     - 关系验证？→ 关系验证度
     - 条件一致？→ 条件一致性

  4. 综合判定：
     - 主体+关系+条件全部匹配 → 0.9–1.0
     - 主体匹配，关系部分匹配 → 0.6–0.8
     - 仅主体匹配 → 0.3–0.5
     - 关系矛盾 → 0.0–0.1
     - 无法判断（无摘要）→ 0.2
输出：support_score 浮点数
```

---

## 4. unverified 论文的处理规则

unverified 论文指 support_score < 0.3 的论文，通常因为缺摘要导致 LLM 无法验证。

### 4.1 标记规则

- 输出表格中标注 ⚠️ 或 "未验证"
- 风险提示中列出所有 unverified 论文

### 4.2 排序影响

- unverified 论文的 support_score 远低于直接验证的论文（0.2 vs 0.9+）
- 即使搜索相关性很高，unverified 论文也不得排在强支撑论文之前
- 同为 unverified 的论文，按 composite_score 排序

### 4.3 推荐限制

- 每个声明最多推荐 **3 篇** unverified 论文
- 仅在 support_score ≥ 0.6（strong+partial）的论文不足 **5 篇**时才推荐 unverified 论文
- 推荐时必须附带风险提示

### 4.4 风险提示模板

```
⚠️ 以下论文仅基于标题/元数据判断相关性，未验证摘要内容：
- [论文标题] (年份) - 可能与声明相关，但支撑度未确认
```

### 4.5 unverified → 已验证的升级

如果后续获取到摘要，应重新评估支撑度：

```
1. 获取摘要（通过 Unpaywall、Crossref、OpenAlex 补全）
2. 按 3.2 的比对流程重新评估
3. 重新运行 support_llm.py
4. 重新排序
```
