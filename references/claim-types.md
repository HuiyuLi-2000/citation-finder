# 声明类型分类与引用规则

## 目录

- [1. 核心判断原则](#1-核心判断原则)
- [2. 三层融合判断框架](#2-三层融合判断框架)
- [3. 话语角色分类（第一层：主判断）](#3-话语角色分类第一层主判断)
- [4. 知识溯源（第二层：验证）](#4-知识溯源第二层验证)
- [5. 可质疑性测试（第三层：兜底）](#5-可质疑性测试第三层兜底)
- [6. 不需要引用的情况](#6-不需要引用的情况)
- [7. 灰色地带处理](#7-灰色地带处理)
- [8. 声明提取流程](#8-声明提取流程)
- [9. 搜索查询生成策略](#9-搜索查询生成策略)

---

## 1. 核心判断原则

**一个句子需不需要引用，取决于这个句子在论证中扮演的角色，而不是它用了什么词。**

默认倾向：**不确定就引**。漏引比多引更危险。

核心判断标准：**这个声明是否可以被合理地质疑？如果可以，就需要引用来支撑。**

---

## 2. 三层融合判断框架

```
句子到达
  │
  ├─ 第一层：话语角色分类（主判断）
  │   理解句子在学术论证中的角色
  │   → 需要引用的角色 → 标记为"需要引用"
  │   → 不需要引用的角色 → 进入第二层验证
  │
  ├─ 第二层：知识溯源（验证）
  │   追问"这个信息的源头在哪里？"
  │   → 源头是外部文献 → 确认需要引用
  │   → 源头是本文作者 → 纠正为不需要
  │   → 源头不确定 → 倾向于引用
  │
  └─ 第三层：可质疑性测试（兜底）
      对判断为"不需要引用"的句子做最终检查
      → 可以合理质疑？ → 升级为"推荐引用"
      → 不可质疑？ → 确认不需要
```

**信号词的角色**：仅作为辅助确认信号，不作为主要判断依据。检测到信号词可增加分类置信度，但不可单独决定分类。

---

## 3. 话语角色分类（第一层：主判断）

每个句子在学术论证中扮演一个角色，角色决定引用需求。

### 3.1 需要引用的话语角色

#### 引言部分

| 话语角色 | 定义 | 典型示例 | 引用必要性 |
|---------|------|---------|-----------|
| 背景铺陈 | 介绍领域现状、问题重要性 | "X plays a crucial role in Y", "X is a fundamental problem in Y" | 必须 |
| 前人归因 | 提及他人的工作、方法、发现 | "Recent studies have explored GNNs for drug discovery" | 必须 |
| 领域共识 | 陈述领域内公认但非公理的观点 | "Pre-training generally improves downstream performance" | 必须 |
| 事实声明 | 陈述具体数据、统计、观察 | "The global NLP market reached $26.4 billion in 2023" | 必须 |
| 方法引用 | 提及具体方法名、模型名、数据集名 | "We use BERT for text encoding" | 必须 |
| 历史脉络 | 描述领域发展历程 | "Since the introduction of X in the 1990s" | 必须 |
| 经验性观察 | 陈述已被观察到的现象 | "Studies have shown that X affects Y" | 必须 |
| 跨领域借鉴 | 从其他领域引入方法/概念 | "Approaches from NLP have been applied to genomics" | 必须 |
| 动机衔接 | "Motivated by X" 中的 X | "Motivated by the success of transformers in NLP" | 必须 |
| 领域进展 | 概述领域近期发展 | "Significant progress has been made in X" | 必须 |
| 技术原理 | 解释方法背后的原理 | "Method X relies on the principle of Y" | 必须 |
| 收敛/综合 | 综合多个方向的发展 | "Recent advances in A and B have enabled C" | 必须 |
| 局限性识别 | 指出现有方法的不足 | "Existing methods suffer from high computational cost" | 推荐 |
| 研究空白 | 指出尚未解决的问题 | "Few studies have addressed the scalability issue" | 推荐 |
| 对比评价 | 比较不同方法的优劣 | "Method A outperforms Method B in low-resource settings" | 推荐 |
| 概念框架 | 引入概念或理论框架 | "The concept of X was first introduced in Y" | 推荐 |
| 假设前提 | 陈述方法基于的假设 | "Based on the assumption that X follows Y distribution" | 推荐 |

#### 讨论部分

| 话语角色 | 定义 | 典型示例 | 引用必要性 |
|---------|------|---------|-----------|
| 与先前工作一致 | 将结果与已有发现对齐 | "Our findings are consistent with X et al." | 必须 |
| 与先前工作矛盾 | 指出与已有发现的不一致 | "In contrast to X et al., we found that..." | 必须 |
| 对先前工作的扩展 | 在已有工作上进一步发展 | "Building on the work of X et al...." | 必须 |
| 机制解释 | 用先前理论解释自己的发现 | "This may be explained by the mechanism proposed in X" | 必须 |
| 替代解释 | 提出其他可能的解释 | "An alternative explanation, suggested by X et al., is..." | 推荐 |
| 意外结果 | 报告与预期不符的发现 | "Surprisingly, we observed X, which contrasts with Y" | 推荐 |
| 阴性结果对照 | 与已有阴性结果对比 | "Our null finding aligns with X et al.'s observation" | 推荐 |
| 实践意义 | 讨论结果的应用价值 | "This has implications for X, as suggested by Y" | 推荐 |
| 泛化性讨论 | 讨论结果的可推广性 | "Whether this extends to X remains to be seen (Y et al.)" | 推荐 |
| 局限性承认 | 承认研究的局限 | "A limitation, as noted in X, is..." | 推荐 |

### 3.2 不需要引用的话语角色

| 话语角色 | 定义 | 典型示例 |
|---------|------|---------|
| 本文贡献 | 作者自己提出的内容 | "We propose a novel method...", "Our framework achieves..." |
| 结构过渡 | 纯组织性句子 | "In the following section, we...", "The remainder of this paper is organized as follows" |
| 公共知识 | 真正的公理，不可质疑 | "Water is H₂O", "2+2=4" |

---

## 4. 知识溯源（第二层：验证）

对第一层判断为"需要引用"的句子，追问：

> **这个信息的源头在哪里？**

| 源头 | 判断 | 示例 |
|------|------|------|
| 外部文献 | 确认需要引用 | "GNNs have achieved SOTA in molecular prediction" → 谁证明的？外部文献 |
| 本文作者 | 纠正为不需要 | "We recently proposed a GNN framework" → 这是自己说的 |
| 公共知识 | 纠正为不需要 | "Neural networks are composed of layers" → 教科书知识 |
| 不确定 | 倾向于引用 | "X is important for Y" → 谁说的？不确定，先引 |

**关键纠偏场景**：

| 句子 | 第一层可能误判 | 知识溯源纠正 |
|------|--------------|-------------|
| "We recently proposed X (Smith et al., 2023)" | 前人归因 → 需要引用 | 源头是本文作者 → 不需要（但已有引用标记，保留） |
| "Our previous work demonstrated X" | 前人归因 → 需要引用 | 源头是本文作者 → 不需要新引用（已有自引） |
| "The method we introduced last year" | 方法引用 → 需要引用 | 源头是本文作者 → 自引即可 |

---

## 5. 可质疑性测试（第三层：兜底）

对判断为"不需要引用"的句子，做最终检查：

> **这个声明是否可以被合理地质疑？**

| 句子 | 可以质疑？ | 最终判断 |
|------|-----------|---------|
| "Deep learning has transformed NLP" | 可以（真的transform了吗？所有方面？） | 升级为推荐引用 |
| "X is a fundamental problem" | 可以（谁说的？凭什么fundamental？） | 升级为推荐引用 |
| "X has attracted considerable attention" | 可以（真的吗？有多少关注？） | 升级为推荐引用 |
| "X offers a promising approach" | 可以（真的promising吗？） | 升级为推荐引用 |
| "Pre-training improves performance" | 可以（一定吗？什么条件下不？） | 升级为推荐引用 |
| "We propose a new method" | 不可以（这是你说的） | 确认不需要 |
| "The sky is blue" | 不可以（公理） | 确认不需要 |
| "In the next section, we..." | 不可以（纯过渡） | 确认不需要 |

**判断标准**：如果一个声明涉及价值判断（"important", "fundamental", "promising", "significant", "considerable"等），即使看起来很general，也应该引用，因为这些判断本身需要证据支撑。

---

## 6. 不需要引用的情况

仅以下三种情况明确不需要引用：

| 情况 | 判定标准 | 示例 |
|------|---------|------|
| 公共知识 | 任何该领域研究者都不会质疑的事实 | "Water boils at 100°C at sea level", "Python is a programming language" |
| 本文贡献 | 信息源头是本文作者自身 | "We propose...", "Our method achieves...", "In this work, we..." |
| 纯过渡句 | 无实质信息，仅起组织结构作用 | "The remainder of this paper is organized as follows", "Next, we describe..." |

**注意**：定义/术语解释需要区分——如果是术语的原始定义（如"Generative Adversarial Network"首次出现），需要引用原始论文；如果是领域内广泛使用的术语简述，不需要。

---

## 7. 灰色地带处理

"General但不是公理"的句子，在顶刊中几乎都会引用。处理原则：

| 句子特征 | 处理方式 | 示例 |
|---------|---------|------|
| 包含价值判断词 | 必须引用 | "crucial", "fundamental", "important", "significant", "promising", "considerable", "remarkable", "essential", "critical", "notable" |
| 包含程度/范围修饰 | 推荐引用 | "widely", "generally", "increasingly", "extensively", "commonly", "frequently" |
| 包含因果/机制声明 | 必须引用 | "X enables Y", "X leads to Y", "X is responsible for Y" |
| 包含趋势/变化声明 | 推荐引用 | "X has grown rapidly", "X has become increasingly popular" |
| 包含比较/排序 | 必须引用 | "X is one of the most...", "X is the leading approach" |
| 包含历史判断 | 推荐引用 | "X has transformed Y", "X revolutionized Y" |

**核心原则**：宁可多引不可漏引。如果拿不准，就引用。

---

## 8. 声明提取流程

### 8.1 句子切分

```
输入：一段文本
处理：
  1. 按句号、问号、感叹号切分
  2. 保留句子在原文中的位置信息（用于后续标注）
  3. 处理特殊情况：
     - 缩写中的句号（e.g., i.e., et al.）不切分
     - 引号内的句号不切分
     - LaTeX 中的 \cite{} 不切分
输出：句子列表 + 位置信息
```

### 8.1.1 语言检测

在句子切分完成后、分类之前，检测文本主要语言：

```
判断规则：
  - 包含中文字符（Unicode CJK 范围）占比 > 30% → 中文文本
  - 否则 → 英文文本（默认）

标记：记录 text_language = "zh" 或 "en"
```

**中文文本的特殊处理**：中文文本在 Step 1 的声明识别阶段正常执行三层判断（中文的学术论证逻辑与英文一致）。但在**生成搜索查询时**，必须将核心术语翻译为英文，因为学术数据库对中文关键词的覆盖极差。

翻译方式：
1. 提取中文核心术语
2. 使用 agent 自身能力翻译为对应英文术语（多数 CS/理工科术语有固定英文对应）
3. 用英文术语生成搜索查询

示例：

| 中文声明 | 核心术语（中文） | 翻译后（英文） | 搜索查询 |
|---------|----------------|--------------|---------|
| "图神经网络在分子性质预测中取得了显著成效" | 图神经网络, 分子性质预测 | graph neural network, molecular property prediction | graph neural network molecular property prediction |
| "Transformer 架构已成为 NLP 领域的主流范式" | Transformer 架构, NLP | Transformer architecture, NLP | Transformer architecture natural language processing |
| "预训练语言模型显著提升了下游任务性能" | 预训练语言模型, 下游任务 | pre-trained language model, downstream task | pre-trained language model downstream task performance |

**注意**：如果中文声明中已包含英文术语（如 "GNN"、"BERT"、"Transformer"），直接使用英文原文，不翻译。

### 8.2 三层融合分类

对每个句子，依次执行三层判断：

**第一层：话语角色分类**
- 理解句子在论证中的功能角色（见第3节）
- 匹配到需要引用的角色 → 标记为"需要引用"
- 匹配到不需要引用的角色 → 进入第二层

**第二层：知识溯源**
- 追问信息源头：外部文献 / 本文作者 / 公共知识 / 不确定
- 源头是外部文献 → 确认需要引用
- 源头是本文作者 → 纠正为不需要
- 源头不确定 → 倾向于引用

**第三层：可质疑性测试**
- 对判断为"不需要引用"的句子，检查是否可被合理质疑
- 可以质疑 → 升级为"推荐引用"
- 不可质疑 → 确认不需要

**辅助信号词**（仅增加置信度，不单独决定分类）：

| 类别 | 信号词/模式 |
|------|-----------|
| 前人归因 | "recently", "previous", "existing", "prior", "earlier", "has been", "have been", "was proposed", "was introduced", "pioneered by", "first demonstrated in" |
| 领域共识 | "widely accepted", "well-known", "it is known", "generally agreed", "consensus", "well-established", "commonly understood" |
| 事实声明 | 具体数字 + 单位/百分比, "reached", "grew to", "accounted for", "estimated at" |
| 背景铺陈 | "crucial", "fundamental", "important", "essential", "critical", "plays a key role", "is central to" |
| 领域进展 | "significant progress", "considerable attention", "rapidly growing", "increasingly popular", "has advanced" |
| 研究空白 | "however", "few studies", "remains unexplored", "little attention", "gap", "challenge", "limited", "underexplored" |
| 对比评价 | "outperforms", "superior to", "better than", "more effective", "significantly improved", "advantages over" |
| 动机衔接 | "motivated by", "inspired by", "building on", "following the success of" |
| 局限性识别 | "suffer from", "limited by", "a key limitation", "the main drawback", "fails to" |
| 历史脉络 | "since the discovery of", "over the past decade", "dating back to", "first introduced in" |
| 技术原理 | "relies on", "based on the principle of", "the key idea behind", "operates by" |
| 本文贡献 | "we propose", "we introduce", "our method", "in this work", "our contribution", "we present" |
| 结构过渡 | "in the following", "the rest of", "is organized as", "next, we", "the remainder of" |

### 8.3 核心声明提取

对需要引用的句子，提取核心声明：

```
输入："Significant progress has been made in graph neural networks for molecular property prediction."
处理：
  1. 识别话语角色：领域进展
  2. 去除角色标记和修饰语："Significant progress has been made in" → 进展信号
  3. 提取核心概念：graph neural networks, molecular property prediction
  4. 提取关系：GNN → molecular property prediction
输出：核心声明 = "graph neural networks for molecular property prediction"
```

### 8.4 已有引用处理

如果原文中已有引用标记，处理规则：

| 格式 | 处理方式 |
|------|---------|
| `\cite{key}` | 保留不动，该句子标记为"已引用" |
| `[数字]` | 保留不动，该句子标记为"已引用" |
| `(Author, Year)` | 保留不动，该句子标记为"已引用" |
| `et al.` | 视为已有引用的信号，检查后面是否有年份 |

已引用的句子不再搜索新文献，除非用户明确要求补充。

---

## 9. 搜索查询生成策略

搜索查询直接使用原始声明或截断后的核心断言，不提取关键词、不做同义替换。

**理由**：现代搜索引擎（Exa neural search、OpenAlex relevance、Google Scholar）能处理完整句子做语义匹配，人工拆解关键词反而损失语义完整性。

**语言前置规则**：如果声明语言为中文（text_language="zh"），先将核心术语翻译为英文，再作为搜索查询。所有搜索查询必须是英文。

**查询长度控制**：
- 短句（≤30词）：直接使用原始声明
- 长句（>30词）：截断到核心断言（保留主语+谓语+宾语，砍掉从句和修饰）

| 原始声明 | 处理 |
|---------|------|
| Yager reassigns conflict mass to the frame of discernment | 短句，直接搜 |
| Murphy averages BPAs uniformly | 短句，直接搜 |
| Methods that assign static weights or that evaluate evidence exclusively through current pairwise comparisons cannot capture such context-dependent reliability | 长句，截断为：Methods that assign static weights cannot capture context-dependent reliability |
