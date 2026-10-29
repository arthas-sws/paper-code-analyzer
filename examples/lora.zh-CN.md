# LoRA：从论文模块拆到源码、配置与收益证据

**简体中文** | [English](lora.en.md) · [返回首页](../README.md)

**范围。** 分析 Hu 等人的 [LoRA 论文，arXiv:2106.09685v2（2021-10-16）](https://arxiv.org/html/2106.09685v2)，聚焦其线性权重适配机制及官方 GPT-2 集成。比较起点是全量微调；Adapter 是延迟实验中的比较对象，不把它写成 LoRA 的架构前作。本文于 2026-10-29 检查官方仓库 `microsoft/LoRA@c4593f060e6a368d7bb5af5273b8e42810cdef90`，属于当前代码快照的静态核验，不保证与论文实验时的代码完全一致。未安装依赖、运行模型或复现实验；不展开跨领域迁移，也不覆盖全文的子空间分析。

## 功能模块总览

| ID | 模块与职责 | 归属 | 全量微调 → LoRA | 论文定位 | 已核对代码与配置 | 收益证据 |
|---|---|---|---|---|---|---|
| A | 预训练主干：提供已有表示 | 继承；冻结策略改变训练方式 | 更新大矩阵 → 固定底座，只允许指定适配参数训练 | §2、§4.1 | [Linear 构造](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/loralib/layers.py#L90-L117)、[参数筛选](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/loralib/utils.py#L13-L30) | 与 B 联合减少可训练参数；不单独归因精度 |
| B | 低秩更新分支：表达任务变化 | 论文提出的核心参数化；不把矩阵分解本身宣称为其首创 | 自由更新 ΔW → 用 BA 表示更新 | §4.1、式 (3) | [Linear 前向](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/loralib/layers.py#L119-L152) | 参数量可作结构推导；无本次复现实测 |
| C | 注意力投影选择：决定更新放在哪里 | 论文的设计选择 + 分组投影工程实现 | 全部权重训练 → 在所查 GPT-2 路径中只适配 Q/V | §4.2、§7.1、表 5 | [Attention 构造及调用](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/examples/NLG/src/model.py#L94-L102)、[MergedLinear](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/loralib/layers.py#L155-L244) | G2：预算匹配下的配置比较；不是“Q 的独立收益” |
| D | 合并与任务状态保存：连接训练与部署 | 线性结构的部署推导 + 工程实现 | 每个任务保存完整权重 → 可单存适配参数，并可选择合并 | §4.1、§4.2 | [合并状态机](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/loralib/layers.py#L218-L244)、[状态筛选](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/loralib/utils.py#L33-L49) | G1：论文延迟记录；所查 GPT-2 配置未启用自动合并 |

这里拆成四个模块，是为了分别解释表示、更新、放置与部署责任，**不是宣称有四项创新**。

## A. 预训练主干与训练参数边界

全量微调在预训练矩阵上继续更新；LoRA 的思路是保留既有映射，让任务变化走另一组参数。输入仍是隐藏特征，输出维度仍与原投影一致，不需要为了适配而改变注意力层对外的接口。

但“冻结底座”需要检查两个层次：

1. `Linear.__init__` 在 `r > 0` 时把该层原权重设为不可训练，见 `layers.py:109–114`。这只说明该层的权重被冻结，**不能据此断言整个模型的偏置、LayerNorm 和其他参数都冻结了**。
2. `mark_only_lora_as_trainable` 遍历模型参数，默认 `bias='none'`，把名称不含 `lora_` 的参数关闭梯度，见 `utils.py:13–30`。所查 [训练入口 321–330 行](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/examples/NLG/src/gpt2_ft.py#L321-L330) 在加载底座后，仅当 `args.lora_dim > 0` 才调用它，再创建优化器。

这给出具体的启用条件：`lora_dim=0` 不能被当成已开启 LoRA。偏置策略改为 `all` 或 `lora_only` 时，可训练参数边界也会改变。

**成本与限制。** 冻结并不删除底座权重；部署仍需要它。梯度也可能需要穿过被冻结的层传给较早的适配参数，因此“底座不更新”不能直接写成“不再需要任何反向传播或激活内存”。本节没有独立精度消融，不给 A 分配一个单独的准确率提升。

## B. 低秩更新：公式、维度与实际前向

论文 §4.1 的式 (3) 将更新写为 `BAx`，并在正文说明缩放。把缩放一并展开，线性层可解释为：

$$
h=W_0x+sBAx,\qquad s=\alpha/r.
$$

其中 `W₀ ∈ R^(d×k)` 是底座，`A ∈ R^(r×k)` 把输入映到 r 维，`B ∈ R^(d×r)` 再映回输出维。这个分支不是把整个底座分解成低秩，而是约束**可学习的更新**。即使 `BA` 低秩，也不能据此说 `W₀+BA` 低秩。

代码使用批量行向量，所以 [Linear.forward 的 147–152 行](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/loralib/layers.py#L147-L152) 对应 `X Aᵀ Bᵀ`，与论文列向量写法方向不同、含义一致。`r>0` 且未合并时加上更新分支；合并后只调用线性映射。`lora_dropout` 非零时，丢弃作用在更新分支输入，而不是直接替换底座分支。

### 能拆到多细：初始化不能只看“随机”两个字

论文 §4.1 描述 A 为随机高斯、B 为零；所查 `Linear.reset_parameters` 实际对 A 使用 Kaiming uniform、对 B 置零，见 [119–125 行](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/loralib/layers.py#L119-L125)。因此应写：**零更新起点一致，A 的初始化分布不同**。不能写成“初始化与论文完全一致”。这项差异是否影响性能，本次没有实验，保持未知。

还可以从公式检查为什么不把 A、B 都初始化成零。令损失对输出的梯度为 `g`，对单个样本、忽略 dropout 的解释性推导为：

$$
\nabla_B L=s\,g(Ax)^T,\qquad
\nabla_A L=s\,B^Tg x^T.
$$

当 B 为零而 A 非零时，B 可以先收到更新；若两者都是零，两组梯度都为零。这是本文的数学解释，不是新测量，也不是论文额外的一条实验结论。

### 参数量算到哪一步

单个无偏置投影原本有 `dk` 个可更新权重；冻结后适配参数为 `r(k+d)`。这是由形状推导的参数数目，不是实测文件大小。

**教学假设，非论文实验：** 若 `d=k=4096`、`r=8`，适配参数为 65,536，原矩阵为 16,777,216；适配参数数目是其 1/256。不能把这一比值直接称为总模型压缩率、显存降幅或速度提升：底座、其他层、精度、优化器和激活都未计入。

## C. 更新放置：从开关追到 Q/K/V 消费者

“在注意力上使用 LoRA”还不够具体。所查 GPT-2 实现把 Q/K/V 合在一个 `c_attn` 投影里，需要确认哪个分块真正被更新。

已检查的路径是：

```text
gpt2_ft.py: 参数 lora_dim / lora_alpha / lora_dropout
  → GPT2Config(... lora_attn_dim=...)
  → GPT2LMModel(config)
  → Attention.__init__: c_attn = MergedLinear
       enable_lora=[True, False, True]
  → Attention.forward: self.c_attn(x)
  → split: query, key, value
  → split_heads → _attn → merge_heads → c_proj
```

配置传递见 [训练入口 298–330 行](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/examples/NLG/src/gpt2_ft.py#L298-L330)，消费者见 [model.py:140–181](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/examples/NLG/src/model.py#L140-L181)。开关与拆分顺序合起来，才支持“这条路径适配 Q、V，K 对应增量为零”。它不意味着 K 的激活在整个网络中永远不变，因为上游输入也可能随训练改变。

`MergedLinear` 的 A/B 是按启用分块打包的，不应把它们当成一个任意混合的 QKV 更新：`merge_AB` 用分组运算计算各启用分块的更新，再用 `zero_pad` 放回完整输出位置，见 [177–216 行](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/loralib/layers.py#L177-L216)。`fan_in_fan_out=True` 还处理 GPT-2 原投影的存储方向。

**不能把 B 的教学计算顺序直接套到这条实现。** `Linear.forward` 连续计算两个低秩投影；这里的 `MergedLinear.forward` 则调用 `merge_AB()` 先构造更新矩阵，再与输入相乘。可训练参数同样是低秩参数化，但临时矩阵、运算顺序与实际开销不同，因此仅从参数量不能给出这条实现的 FLOPs、显存或训练速度结论。

**收益边界。** G2 比较的是相同总适配参数预算下的投影选择，同时改变每处 rank。它支持该配置组合的条件性比较，不是固定 rank 下“多加一个 Q 就提升多少”，也不是本次 GPT-2 代码路径复现了 GPT-3 表 5。

## D. 合并、保存与部署边界

忽略推理时 dropout，并固定某个任务的 A/B，线性性允许写成：

$$
W_{\mathrm{deploy}}=W_0+sBA.
$$

于是前向可以只算一次原尺寸线性投影。这个等式说明**合并后的运算结构**；不证明任意实现已经做了合并，也不证明训练没有额外成本。

实际核验发现两层不同事实：

- 库的 `MergedLinear.train(False)` 在 `merge_weights=True` 且尚未合并时加上更新；回到训练模式时减去更新，`merged` 防止重复加，见 [218–244 行](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/loralib/layers.py#L218-L244)。
- 但所查 GPT-2 `Attention` **显式设置 `merge_weights=False`**，见 [model.py:94–102](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/examples/NLG/src/model.py#L94-L102)。仅调用 `eval()` 不会在这条路径自动合并，前向仍进入更新分支。本例不把它描述成论文的延迟实验脚本，也未核验其他导出工具是否另做合并。

保存方面，[gpt2_ft.py:223–226](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/examples/NLG/src/gpt2_ft.py#L223-L226) 使用 `lora_state_dict`；[utils.py:33–49](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/loralib/utils.py#L33-L49) 默认只筛出 LoRA 参数。这个小文件需要匹配的底座及层配置，不能当成可独立推理的完整模型。合并还涉及一次性计算和浮点舍入；这里没有进行数值等价或延迟实测。

## 整机结果与证据账本

以下均为[论文原始报告](https://arxiv.org/html/2106.09685v2)，不是本次跑出的结果。

| 证据 | 涉及模块 / 归因层级 | 原始数值与条件 | 判断与限制 |
|---|---|---|---|
| G1，表 1 | D 的部署动机；整机前向比较 | GPT-2 medium，batch=1、长度=128、RTX8000，100 次前向；Fine-Tune/LoRA：19.8±2.7 ms；Adapter-L：23.9±2.1 ms；Adapter-H：25.8±2.2 ms，越低越好 | 表内条件可比；Fine-Tune/LoRA 是合并展示的一行，不能拆成两组独立实测，更不能给 A/B/C 各分一次加速。未复现，未核对原始计时日志 |
| G2，表 5 | B+C；预算匹配的配置比较 | GPT-3、18M 可训练参数；WikiSQL 验证准确率：Q-only、r=8 为 70.4%；Q+V、r=4 为 73.7%，表标注跨种子标准差约 0.5% | 条件可比：同预算下改变放置和每处 rank 的联合配置比较。百分点差为 **+3.3**；不是独立 Q/V 贡献，也不是所有任务的通用结论 |
| S1，本例形状推导 | A+B；单层参数数量 | 教学假设的 4096×4096、r=8：16,777,216 对 65,536 | 不是论文测量或性能数据；不调用收益工具把它包装成复现结果 |

G2 的 `73.7−70.4=3.3` 使用的是准确率的**百分点**，不是“相对提升 3.3%”；本例不对精度百分数再求相对增长，也不推断统计显著性。表内统一预算足以支持这里的受限配置差值，不足以消除放置和 rank 同时改变的归因问题。

## 结论、限制与实际完成深度

读者现在可以核对：底座为什么保留、低秩参数的形状和梯度、哪个入口启用适配、Q/V 选择怎样落实、更新输出怎样被注意力消费、何时合并，以及小检查点缺少什么。论文与代码差异也留下了具体定位：A 初始化分布不同；合并能力存在，但所查 GPT-2 配置未开启。

本例没有证明低秩对每个任务都充分，没有把代码快照视为原论文运行记录，也没有把少量参数等同于按相同比例节省显存或加速。要继续到复现，需要匹配的数据、底座、脚本与环境、训练配置、日志、随机种子及明确执行授权。要继续审查创新归属，需要额外读取论文所引前作；这里仅标注论文提出的机制，未做领域首创认证。

**完成层级：论文机制阅读 → 模块划分 → 公式与维度 → 固定提交源码 → 调用与配置 → 原报告数值核对 → 成本与证据限制。未执行：环境安装、训练、复现实测、迁移研究。**

核对：A–D 总览与正文一致；G1/G2/S1 不重复分配模块收益；引用代码已实际检查；缺失与未执行项已标明。本文为原创解释，不包含上游源码或论文全文副本；上游内容保留各自许可。
