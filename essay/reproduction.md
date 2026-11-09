# Code appendix and reproduction / 代码附录与复现

## Environment / 环境

Verified on CPython 3.9.6. The three scripts use only the Python standard library; no package installation or network connection is required. Run each in a fresh process from the repository root. Exact integer and rational computations are distinguished from the explicitly marked floating-point example.

已在 CPython 3.9.6 验证。三个脚本仅用标准库，无须安装依赖或联网。从仓库根目录分别启动新进程运行。整数及 Fraction 示例使用精确运算；浮点案例单独标明。

```sh
python3 essay/fold_checks.py
python3 essay/propositions_checks.py
python3 essay/productive_series_checks.py
```

All three commands returned exit code 0 in this verification. Do not run Python with `-O`: that removes the assertion checks.

本次三个命令均退出码 0。请勿加 `-O`，它会移除断言检查。

## Script map / 脚本分工

| Script | Scope / 范围 | What success establishes / 成功意味着什么 |
|---|---|---|
| fold_checks.py | Subtraction, Fibonacci counts, tail recursion, traversal, Ackermann, floating-point grouping, a five-node DAG / 减法、调用计数、尾递归、遍历、浮点与五节点图 | Printed illustrative outcomes; some checks are assertions, others are demonstrations / 输出例证，部分有断言，部分仅打印 |
| propositions_checks.py | Monoid tree example and additive DAG multiplicities / 树汇总与路径重数 | Assertions agree on the stated finite enumeration and examples / 指定有限范围内的断言一致 |
| productive_series_checks.py | Lazy state unfolding and rational partial sums / 惰性展开与有理数部分和 | Equality of finite prefixes and recursive sums for N=0..20 / 所检验前缀与有限递归和一致 |

The scripts are executable appendices, not formal proof assistants. Their checks do not establish novelty, arbitrary-input correctness, productivity of all generators, or convergence of arbitrary series.

脚本是可执行附录，不是形式化证明系统。检查结果不证明原创性、任意输入正确性、一般生成器的生产性或任意级数的收敛。

## Verified values and counting conventions / 数字与计数口径

| Quantity / 项目 | Verified result / 核实结果 | Interpretation / 解释 |
|---|---|---|
| Right subtraction / 右嵌套减法 | 2 | rsub([3,2,1]) uses terminal seed 0 / 带终止种子 0 |
| Left subtraction / 左折叠减法 | 0 | lfold([3,2,1]) starts from 3 / 从首元素 3 起算 |
| Fibonacci value / 返回值 | 6765 | Both implementations at n=20 / 两种实现相同 |
| Naive Fibonacci evaluations / 朴素函数体执行数 | 21891 | Counter incremented at body entry / 每次进入函数体计一次 |
| Memoized Fibonacci evaluations / 记忆化函数体执行数 | 21 | Fresh unbounded lru_cache; cache hits do not enter the body / 空的无限缓存，命中不执行函数体 |
| Tail-recursive sum / 尾递归和 | 10 | Value only; not constant-stack evidence / 只说明返回值，不说明常量栈 |
| Traversal / 遍历 | ['a', 'b', 'c'] | Logged execution order / 日志记录顺序 |
| Ackermann | ack(2,3)=9 | One finite sample / 一个有限样例 |
| Float grouping / 浮点括号 | 0.6000000000000001 versus 0.6 | On the verified runtime / 本次运行环境 |
| Five-node DAG / 五节点图 | V(r)=7, weighted sum=7, m(c)=2 | fold_checks.py: all five local weights are 1 / 五个局部权值均为 1 |
| Four-node diamond / 四节点菱形图 | 16 versus unweighted 11 | propositions_checks.py: weights [1,2,3,5], path counts [1,1,1,2] |
| Parallel-edge diamond / 增加平行边 | 21 versus unweighted 11 | Path counts [1,1,1,3] / 路径重数变化 |
| Tree shapes / 树形 | 23 | All ordered binary shapes with 0..4 nodes, including empty tree / 含空树，节点数 0..4 |
| DAGs / 图数量 | 75 | All edge subsets i→j with i<j, for 1..4 numbered vertices / 固定拓扑编号的简单图枚举，不是非同构图计数 |
| Weighted cases / 权重情况 | 5421 | Each graph paired with every weight vector in {-1,0,1}^n / 每个图遍历全部三值权重向量 |
| Geometric sums / 几何部分和 | N=0..20: P_N=R(N)=1−2^(−N) | Fraction arithmetic / 有理数精确运算 |
| Selected partial sums / 指定部分和 | N=0,1,2,4,8: 0,1/2,3/4,15/16,255/256 | Errors: 1,1/2,1/4,1/16,1/256 / 对应误差 |
| Constant-one prefix sums / 常数流前缀和 | [1,2,3,4,5,6] | Nonconvergence follows from formula P_N=N, not six observations / 不收敛依据一般公式 |
| Alternating prefix sums / 交替流前缀和 | [1,0,1,0,1,0] | Nonconvergence follows from distinct even/odd subsequences / 不收敛依据奇偶子列 |

The values 7 and 16 are for different DAG examples and are both correct. Do not present them as measurements of the same graph.

7 与 16 属于不同图例，均正确，不能写成同一图的两次结果。

Enumeration detail: tree counts are 1+1+2+5+14=23. DAG counts are 1+2+8+64=75. Weight-case counts are 3+18+216+5184=5421. Graphs with unreachable vertices are included; those vertices have root-path multiplicity zero and are excluded from the reachable-node sum.

枚举说明：含不可达节点的编号图也参与检查；不可达节点路径重数为零，不贡献根的值。平行边由独立示例覆盖，不在简单图穷举中。

## Execution boundaries / 执行边界

CPython does not eliminate the tail-call frames used by tsum. In this implementation list slicing also allocates new lists. A loop rewrite is required before claiming constant call-stack use; no benchmark or asymptotic memory measurement is provided here. fold_checks.py raises the recursion limit for its Ackermann demonstration; this is not a general remedy for recursion resources. Run the supplied small inputs.

CPython 中 tsum 的尾调用仍增加调用栈；列表切片还会分配新列表。需要改写为循环才能就此实现声称常量调用栈，本附录未测量内存。提高递归深度上限不保证资源安全或任意输入终止。

The unfold generator stores its current state without an explicit prefix cache. This describes this implementation only. Lazy streams can also be implemented with memoized tails; neither absence nor presence of memoization follows from the mathematical anamorphism definition. The test collects 20 pairs into a list for inspection, so the test harness itself retains a finite prefix.

unfold 生成器无显式前缀缓存，仅描述本实现；惰性流可以记忆化，数学 ana 定义不指定缓存策略。演示为了检查把 20 对输出收集成列表，因此测试程序确实保留有限前缀。

IEEE-style exceptional values require care: NaN is not equal to itself; +∞+(−∞) produces NaN; +0 and −0 compare equal but have different signs. The ordinary finite-number grouping example does not establish a universal bitwise commutativity statement over all floats.

NaN、无穷大与有符号零不能直接套用普通实数等式。有限浮点括号例只展示结合律失败，不支持所有浮点数逐位交换性的一般断言。
