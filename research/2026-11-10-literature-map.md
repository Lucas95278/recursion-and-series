# 本轮文献定位：哪些想法已经存在

日期：2026-11-10。范围：针对本轮候选方向的小范围先行工作核查，不是全面综述，也不替代旧稿缺失的 `lit-check.md`。

## 1. 直接相关的三份原始论文

### L6：路径求和及绝对可和条件

Dmitry M. Malioutov, Jason K. Johnson, Alan S. Willsky. **Walk-Sums and Belief Propagation in Gaussian Graphical Models.** Journal of Machine Learning Research 7 (2006), 2031–2064。

- [出版社页面](https://www.jmlr.org/papers/v7/malioutov06a.html)
- [原文 PDF](https://jmlr.csail.mit.edu/papers/volume7/malioutov06a/malioutov06a.pdf)
- 本轮定位：§3.1，印刷页 2039–2040，特别是 Proposition 1。已对照原 PDF 第 10 页图像，核查矩阵绝对值、谱半径及收敛对象。

该文在其 Gaussian 模型中明确区分按长度合并的路径贡献与路径任意排序的绝对可和性；条件涉及 ρ(R) 与 ρ(|R|) 的区别。

**对本项目的影响：** “路径可以带符号”“绝对路径界比聚合界更保守”“任意重排需要更强条件”不能宣称为本项目的新发现。原文的对称性、正定性及 Gaussian 模型前提，也不能原样套给本项目任意非对称递归矩阵；本轮有限矩阵命题在研究笔记中另外给证明。

本项目多重图另须区分 B_uv=Σ_e|c_e| 与 |C_uv|=|Σ_ec_e|，不应把二者混记。

### L7：局部推送及不变量

Reid Andersen, Fan Chung, Kevin Lang. **Local Graph Partitioning using PageRank Vectors.** 2006 年完整稿。

- [作者机构托管的原文 PDF](https://www.cs.cmu.edu/~15859n/RelatedWork/local_partitioning_full.pdf)
- 本轮定位：§3，PDF 第 6–7 页，push 操作及 Lemma 1。已对照第 6 页原始图像核查不变量。

该文用近似向量与残余向量维护 PageRank 不变量，通过局部 push 移动残余并证明停止条件与成本界。

**对本项目的影响：** 单节点推送、维护“已算部分加剩余部分”的不变量、依据残余大小选择局部操作，这些基本策略已有充分背景。PageRank 的概率、非负性与随机游走条件不自动适用于本项目任意正负权矩阵。

### L8：最直接的单分量线性系统近似

Asuman Ozdaglar, Devavrat Shah, Christina Lee Yu. **Asynchronous Approximation of a Single Component of the Solution to a Linear System.** arXiv:1411.2647，最初提交于 2014 年；本轮下载的 PDF 标注 v4，2019-01-21。

- [arXiv 记录](https://arxiv.org/abs/1411.2647)
- [原文 PDF](https://arxiv.org/pdf/1411.2647)
- 本轮定位：§1.3、§4.1–§4.3、§5 及相应局部更新讨论。特别核查 PDF 第 2–3 页的不变量与第 7 页的选点、停止条件。没有把整篇论文全部定理视为已经逐项重证。

该文直接研究 x=Gx+z 的单个坐标近似，维护 x_i=已算值+r^Tx。其异步结果使用 ρ(|G|)<1 及相应调度前提。§4.2 已讨论最大残余坐标与按残余抽样；不能把这些策略作为本轮新发现。

**需要精确对齐的差异：** 本轮笔记另引入节点各自的有限层数 ℓ_u，先形成 (C^ℓ_u) 的对应行，再验证共同权重下的收缩条件。所得宏矩阵允许使用原始 |C| 不可收缩但 C 稳定的例子。暂未核实这种逐行可变幂证书及成本率是否已在更广泛的多项式预处理、异步线性迭代或路径求和文献中出现。

因此目前可以说“得到一个可证明、可继续查文献的具体表述”，不能说“首次提出更一般的单分量算法”。

## 2. 伴随残差已有成熟背景

[dolfin-adjoint 官方文档：Applications of adjoints / Error estimation](https://www.dolfin-adjoint.org/en/latest/documentation/maths/5-applications.html) 的搜索返回内容讨论基于目标量的误差估计，并将原问题残差与伴随问题联系起来。本轮未成功取得该页面的完整正文，故此处仅作为背景入口。

本项目使用的有限线性恒等式 z^T d 可直接由转置方程推导。它与目标导向误差估计相连；不要把一般 PDE 的高阶余项公式直接套用，也不要将这个线性恒等式认定为原创。

## 3. 尚待精读的相邻方向

本轮搜索发现以下原始资料线索，但未完成全文比对，只能用于安排后续阅读：

- [Bertsekas 与 Tsitsiklis：Convergence Rate and Termination of Asynchronous Iterative Algorithms](https://www.mit.edu/~jnt/Papers/C-89-rate_termination-Crete.pdf)：调度、加权最大范数及停止认证。
- [Estimation in Gaussian Graphical Models Using Tractable Subgraphs](https://ptolemy.berkeley.edu/projects/truststc/pubs/267/cjw_walksum_tsp07.pdf)：搜索内容显示其研究自适应子图、block Gauss–Seidel 和路径求和，可能与“分组保留抵消”密切相关。
- [Variable Degree Schwarz Methods](https://users.wpi.edu/~msarkis/papers/ICASE_Sarkis.pdf)：局部选择多项式阶数的已有工作。其模型和实现未与本项目逐项对齐，不能仅因用词相似就说等价，也不能忽略它来断言本项目首次使用不同层数。

## 4. 目前不能宣称的内容

1. 递归与矩阵 Neumann 级数的联系是本项目发现的。
2. 路径符号抵消与绝对可和性的差异是新理论。
3. 单分量近似、残余推送或最大残余选点是本项目首创。
4. 伴随残差恒等式是新结果。
5. 有一个证书进度界，就自动证明方法比全局求解更快。
6. 本轮小范围检索没看到完全相同的表述，就证明可变层数证书具有原创性。
7. 有限矩阵的稳定性命题已经解决无限递归或一般程序终止问题。

## 5. 检索与取得方式

使用系统网页搜索发现原始来源。按本机偏好，通过 IceWalk 本地 MCP 尝试读取三处网页，均因 webdriver-manager 的驱动锁等待超时失败。未切换到 Firecrawl，也未改动驱动锁。随后直接取得原始论文 PDF 并提取相关页，必要处渲染核对。官方伴随文档的直接 HTTP 读取未取得可核验的完整本地结果，不能记为通读。

论文下载件及图像只用于本地核查，不随研究笔记提交到仓库。此次核查有取得范围和阅读范围限制，不能作为“全部相关文献已核查完毕”的声明。
