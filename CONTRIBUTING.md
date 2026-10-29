# 贡献指南 / Contributing

感谢帮助改善证据质量和可读性。中文和英文均可提交 issue 或 pull request。
Issues and pull requests in Chinese or English are welcome.

## 建议提供 / What to include

- 问题、预期行为、最小可复查材料，以及实际观察到的输出；不要上传私密论文、凭据或未授权代码。
  Describe the problem, expected behavior, minimal checkable materials, and observed output. Exclude private papers, credentials, and unauthorized code.
- 涉及数字时保留原值、单位、来源和实验条件。涉及来源对应时提供论文定位、提交与代码路径。
  Preserve original values, units, sources, and protocols for numeric issues; provide paper locators, commits, and paths for source-mapping issues.
- 公共文档修改请同步检查中英文入口与相对链接；技能行为修改请解释适用范围及可能影响。
  Check both language entry points and relative links for documentation changes; explain scope and impact for behavioral changes.

## 修改边界 / Change boundaries

本次发布准备保留了导出快照。后续如需修改技能，单独提交明确的变更并更新快照说明；不要悄悄改动文件而继续声称与导出一致。维护者本机正在使用的 skill 不属于本仓库变更范围。
This publication preparation preserves an exported snapshot. Future skill changes should be explicit and update snapshot documentation; do not silently modify files while claiming export identity. The maintainer's installed skill is outside repository change scope.

脚本变更应验证相关行为，例如可比输入、不同比较协议、单位不一致和 PSNR 单位处理。文档变更核对链接与描述即可。不要为了验证而默认运行论文仓库、训练或批量研究任务。
For helper changes, verify relevant behavior such as comparable inputs, protocol mismatch, unit mismatch, and PSNR handling. Documentation changes need link and description checks. Do not automatically run paper repositories, training, or bulk research tasks.

## 许可 / Licensing

本项目采用 [MIT 许可证](LICENSE)。提交贡献时，请确认有权提供相关材料，贡献须与 MIT 兼容，并保留必要的第三方声明。
This project uses the [MIT License](LICENSE). Contribute only materials you have the right to provide, ensure MIT compatibility, and preserve required third-party notices.
