# 稿件、研究推导与验证材料

更新日期：2026-11-09。返回[仓库首页](../README.md)。

**当前状态：工作稿。** 本次导入保留被审查的研究正文，仅在稿件顶部补充状态提示；已知正文错误、双语同步及文献核查问题尚未批量修订。查看[本轮检查报告](../reviews/check-2026-11-09.md)后再引用扩展稿。旧评审与本轮报告分别对应各自的材料快照。

| 文件 | 内容与状态 |
|---|---|
| [essay_final.md](essay_final.md) · [essay_final.en.md](essay_final.en.md) | 中英文扩展工作稿；英文仍含中文已修正的旧问题 |
| [propositions_ab.md](propositions_ab.md) | 有序树幺半群汇总与 DAG 路径重数的形式证明 |
| [productive_series.md](productive_series.md) | 流展开、有限部分和与收敛的支持材料 |
| [affine_remainder_research.md](affine_remainder_research.md) | 单链仿射递归的精确残项及截断误差 |
| [branch_remainder_research.md](branch_remainder_research.md) | 加权分支的前沿展开、误差传播与停止界 |
| [red-team-review.md](red-team-review.md) | 导入材料中的旧评审；不代表全部问题的当前状态 |
| [reproduction.md](reproduction.md) | 原有三个基础脚本的详细复现说明 |
| [请先读我.txt](请先读我.txt) | 原材料包的状态说明 |

## 运行五个验证脚本

使用 Python 3，在仓库根目录执行；仅需标准库，不使用移除断言的 `-O` 选项。

```sh
python3 essay/fold_checks.py
python3 essay/propositions_checks.py
python3 essay/productive_series_checks.py
python3 essay/affine_remainder_checks.py
python3 essay/branch_remainder_checks.py
```

本轮检查确认的规模：23 个有序二叉树形、75 个拓扑编号 DAG、5421 组 DAG 权重；单链展开与区间 51840 例、收缩界 32805 例；分支展开与误差界 58320 例。计数沿用脚本口径，不能当作形式化证明。

两份后续研究暂未合入扩展稿，也未完成原创性核查。扩展稿中引用的 `lit-check.md` 未随原材料提供，当前仓库不声称该核查已完成。
