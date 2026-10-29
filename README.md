# Paper Code Analyzer · 论文与代码分析

**简体中文** | [English](README.en.md)

把一篇论文拆成可核对的功能模块，说明每个模块从哪里来、改了什么、怎样实现，以及收益证据能支持到哪一步。

本项目是一个供 AI 助手加载的 skill，包含指令、报告模板、参考指南和一个 Python 算术工具。它不是独立运行的论文分析程序。

## 它怎样帮你读论文

1. **先看结构**：用模块总览表建立全貌，沿用同一组编号逐项展开。
2. **分清贡献**：区分继承、新提案、修改和工程实现；从论文本身的前作与基线出发。
3. **讲清机制**：解释输入、输出、公式、状态、约束以及上下游关系。
4. **核对代码**：定位实际检查过的提交、文件、符号、调用路径和配置；缺失证据明确标注。
5. **审查收益**：保留原始数值、单位和实验条件；先判断可比性，再计算变化。整机或联合收益不会被分摊为单模块贡献。

只有你明确要求迁移、替换或适配时，才追加目标约束、跨领域候选和最小验证计划。没有独立消融、没有代码或没有可比实验，都可以是有价值的分析结论。

## 开始使用

将本仓库下载或克隆到一个新的目录。在支持导入 skill 的宿主中，导入包含 `SKILL.md` 的目录，并保持相对目录完整。具体导入入口与工具权限取决于宿主。

如需手动安装到本机已有的自定义 skills 目录，只复制到一个**尚不存在**的 `paper-code-analyzer` 子目录；如果已安装同名版本，先停下并自行选择备份或另一测试环境。不要直接覆盖正在使用的版本。

完整分析请求示例：

> 使用 paper-code-analyzer 分析这篇论文和它的官方代码。先给模块总览，再按相同编号讲前作或基线、机制公式、代码对应及收益证据。没有核验到的部分请标明。论文：[链接或文件]；代码：[链接]。

窄问题也可以直接问：

> 只解释这篇论文的量化模块：输入输出是什么，训练与编码时有什么区别，代码能否对应？

英文输出可加：`Please write the analysis in English.` 文档语言切换不会替换原版技能文件。

## 文档与示例

- [工作流程与分析方法](docs/workflow.zh-CN.md) · [English guide](docs/workflow.en.md)
- [合成示例：证据不足时怎样报告](examples/evidence-example.md)
- [贡献指南 / Contributing](CONTRIBUTING.md)
- [参考项目与来源说明](docs/provenance.md)

## 文件结构

```text
SKILL.md                         原版技能入口
agents/openai.yaml               原版界面元数据
assets/                         原版图标与报告模板
references/                     原版证据、迁移与 3DGS 检查指南
scripts/compute_gains.py         原版收益计算工具
README.md / README.en.md         中英文项目说明
docs/                           面向人的流程和来源说明
examples/                       明确标记的合成示例
CONTRIBUTING.md                  贡献规则
SOURCE_MANIFEST.json             原版文件 SHA-256 清单
```

## 运行条件与边界

论文、补充材料和代码必须能被宿主读取。网页检索、PDF 读取和仓库访问依赖宿主提供的工具；本包不含这些服务，不需要 API 密钥配置。缺少工具时应如实报告证据限制。跨宿主的完整分析行为尚未测试。

`scripts/compute_gains.py` 仅使用 Python 标准库。已用 Python 3.13 检查命令行及代表性数值边界；其他 Python 版本未在本次打包中验证。

```bash
python scripts/compute_gains.py --help
python scripts/compute_gains.py --example
python scripts/compute_gains.py INPUT.json --output OUTPUT.json
```

该工具不验证来源、实验协议或因果关系。`rankable` 只表示输入声明通过算术检查。默认工作方式是只读研究；安装依赖、运行论文仓库代码、训练或修改工程需要另行授权。

## 版本与许可

这是用户于 2026-10-29 提供的技能导出快照。原始 9 个文件保持字节一致，公开说明单独添加，校验值见 `SOURCE_MANIFEST.json`。目前未指定上游版本号。

本项目采用 [MIT 许可证](LICENSE)，版权署名为 `arthas-sws`。允许使用、修改、分发和商用，分发时须保留版权及许可声明。论文、被分析仓库和宿主工具各自的许可不由本项目授予。
