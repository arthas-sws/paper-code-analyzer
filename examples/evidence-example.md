# 合成示例 / Synthetic example

本例完全虚构，仅示范输出结构，不是对真实论文或仓库的分析，也不是复现结果。
This example is entirely synthetic. It demonstrates reporting structure, not a real paper analysis or reproduction.

**范围 / Scope:** 假想方法含选择器与编码器；未提供真实论文和源码。模块归属、实现与数值证据均未核验。
An imaginary method contains a selector and a coder. No real paper or source was supplied; provenance, implementation, and measurements are unverified.

| ID | 模块 / Module | 归属 / Attribution | 前后变化 / Change | 代码 / Code | 收益 / Gains |
|---|---|---|---|---|---|
| A | 选择器 / Selector | 未核验 / Unverified | 假设减少待编码元素 / Hypothetically reduces elements to encode | 未提供 / Missing | 无独立消融 / No independent ablation |
| B | 编码器 / Coder | 未核验 / Unverified | 假设编码保留元素 / Hypothetically codes retained elements | 未提供 / Missing | 无独立消融 / No independent ablation |

## A. 选择器 / Selector

解释需要输入、选择规则和输出的实际证据；不能从名称猜测已验证机制。还需检查掩码或索引的存储成本。
The inputs, selection rule, and outputs require actual evidence. A name cannot verify a mechanism. Mask or index storage would also need accounting.

## B. 编码器 / Coder

需要确认编码输入、解码侧可用状态、实际码流及重建路径；训练中的熵估计不足以证明可解码文件大小。
Check coded inputs, decoder-available state, actual bitstream, and reconstruction. A training entropy estimate does not prove decodable file size.

## 整机结果与限制 / System results and limits

假想记录中 baseline 为 100 MB、candidate 为 80 MB，但质量点和协议未知。因此仅保留原值，**不计算差值、百分比、比例或排名**，也不把整机变化归给 A 或 B。
Suppose a fictional record gives 100 MB for the baseline and 80 MB for the candidate, with unknown quality points and protocol. Preserve those originals and **calculate no delta, percentage, ratio, or ranking**. Assign no system difference to A or B.

需要补充：原始结果表、质量约束、存储边界、实际代码提交及独立消融。未执行实验；未提出迁移建议。
Missing: original results table, quality constraints, storage boundary, inspected commit, and independent ablations. No experiments were run and no transfer was requested.
