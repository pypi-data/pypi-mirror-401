# -*- coding: utf-8 -*-

"""
本模块功能：马科维茨模型求解方法，拉格朗日乘数法，二次规划法
所属工具包：证券投资分析工具SIAT 
SIAT：Security Investment Analysis Tool
创建日期：2026年1月3日
最新修订日期：2026年1月4日
作者：王德宏 (WANG Dehong, Peter)
作者单位：北京外国语大学国际商学院
作者邮件：wdehong2000@163.com
版权所有：王德宏
用途限制：仅限研究与教学使用，不可商用！商用需要额外授权。
特别声明：作者不对使用本工具进行证券投资导致的任何损益负责！
"""
#==============================================================================
#统一屏蔽一般性警告
import warnings; warnings.filterwarnings("ignore")   
#==============================================================================
  
from siat.common import *
from siat.translate import *
from siat.security_trend2 import *

import pandas as pd
import numpy as np
import datetime
import cvxpy as cp
#==============================================================================
import matplotlib.pyplot as plt
#统一设定绘制的图片大小：数值为英寸，1英寸=100像素
#plt.rcParams['figure.figsize']=(12.8,7.2)
plt.rcParams['figure.figsize']=(12.8,6.4)
plt.rcParams['figure.dpi']=300
plt.rcParams['font.size'] = 13
plt.rcParams['xtick.labelsize']=11 #横轴字体大小
plt.rcParams['ytick.labelsize']=11 #纵轴字体大小

title_txt_size=16
ylabel_txt_size=14
xlabel_txt_size=14
legend_txt_size=14

#设置绘图风格：网格虚线
plt.rcParams['axes.grid']=True

#处理绘图汉字乱码问题
import sys; czxt=sys.platform
if czxt in ['win32','win64']:
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置默认字体

if czxt in ['darwin','linux']: #MacOSX
    #plt.rcParams['font.family'] = ['Arial Unicode MS'] #用来正常显示中文标签
    plt.rcParams['font.family']= ['Heiti TC']


# 解决保存图像时'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False 
#==============================================================================
#全局变量定义
RANDOM_SEED=1234567890

#==============================================================================
# 基于投资组合成分证券的价格 DataFrame（prices）计算：
# 1. 各个成分证券的期望收益率
# 2. 修正后的半正定的收益率协方差矩阵 
#==============================================================================

def member_returns_covariance(prices: pd.DataFrame, freq: str = "D",
                              check_positive_semidefinite: bool = True,
                              printout: bool = True) -> tuple:
    """
    基于投资组合成分证券的价格DataFrame，计算成分证券的预期收益率和协方差矩阵。
    可选对协方差矩阵进行半正定修正，以满足二次规划法的要求。
    参数：
    prices：价格DataFrame，索引=日期，列=证券名称，值=价格
    freq：收益率频率（D=日, W=周, M=月），用于计算年化收益率
    check_positive_semidefinite：是否检查并修正半正定协方差
    printout：是否打印结果
    
    返回：
    成分证券的预期收益率expected_returns，协方差矩阵cov_matrix
    """
    # ========== 1. 计算对数收益率（金融领域更常用，符合正态分布假设） ==========
    # 对数收益率 = ln(今日价格/昨日价格)
    returns = np.log(prices / prices.shift(1)).dropna()  # 剔除第一行NaN
    
    # ========== 2. 计算年化期望收益率 ==========
    # 先计算日/周/月均收益率，再年化（按交易日数量）
    freq_map = {"D": 252, "W": 52, "M": 12}  # 年化因子（交易日天数）
    daily_mean = returns.mean()
    expected_returns = daily_mean * freq_map[freq]  # 年化期望收益率
    
    # ========== 3. 计算原始协方差矩阵（年化） ==========
    # 日协方差矩阵 × 年化因子 = 年化协方差矩阵
    cov_matrix = returns.cov() * freq_map[freq]
    
    # ========== 4. 修正协方差矩阵（保证半正定） ==========
    if check_positive_semidefinite:
        # 特征值分解，将负特征值替换为极小正数
        eigenvals, eigenvecs = np.linalg.eig(cov_matrix)
        # 替换负特征值（允许微小浮点误差，设为1e-8）
        eigenvals[eigenvals < 1e-8] = 1e-8
        # 重构半正定矩阵
        cov_matrix_fixed = eigenvecs @ np.diag(eigenvals) @ eigenvecs.T
        # 修正浮点误差导致的非对称（协方差矩阵必须对称）
        cov_matrix_fixed = (cov_matrix_fixed + cov_matrix_fixed.T) / 2
        
        cov_matrix_fixed = np.round(cov_matrix_fixed, 6)  # 保留6位小数
    else:
        cov_matrix_fixed = np.round(cov_matrix, 6)  # 保留6位小数
    
    # 转换为numpy数组（方便CVXPY计算）
    expected_returns = np.round(expected_returns.values,6)

    # 输出结果
    if printout:
        titletxt1=text_lang("年化预期收益率","Annualized Expected Returns")
        print(f"\n=== {titletxt1} ===")
        print(pd.Series(expected_returns, index=prices.columns).round(4))
        
        titletxt2=text_lang("年化协方差矩阵","Annualized Covariance Matrix")
        if check_positive_semidefinite:
            titletxt2x=text_lang("（半正定修正后）","(Adjusted to Positive Semidefinite)")
        else:
            titletxt2x=''
        print(f"\n=== {titletxt2}{titletxt2x} ===")
        print(pd.DataFrame(cov_matrix_fixed, index=prices.columns, columns=prices.columns).round(4))
        
    if check_positive_semidefinite and printout:
        eigenvals = np.linalg.eigvals(cov_matrix_fixed)
        titletxt3=text_lang("协方差矩阵的特征根（半正定修正后）","Eigens of Adjusted Covariance Matrix")
        print(f"\n=== {titletxt3} ===")
        print(np.round(eigenvals, 8))
        
        print(text_lang("是否半正定？","Positive semidefinite?"), all(eigenvals >= -1e-8))  # 允许微小浮点误差
        
    member_names=list(prices.columns)
    
    return expected_returns, cov_matrix_fixed, member_names

# ========== 示例：测试代码 ==========
if __name__ == "__main__":
    # 构造模拟价格DataFrame
    """
    dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
    np.random.seed(42)  # 固定随机种子，结果可复现
    price_data = np.random.rand(len(dates), 4) * 100 + 50  # 4只证券，价格50-150
    prices = pd.DataFrame(
        price_data,
        index=dates,
        columns=["证券A", "证券B", "证券C", "证券D"]
    )
    """
    stocks=["601939.SS","600000.SS","601998.SS","601229.SS"]
    prices=security_trend(stocks,indicator='Adj Close',graph=False)

    
    # 计算期望收益率和修正后的协方差矩阵（按日收益率年化）
    expected_returns, cov_matrix, member_names = member_returns_covariance(prices)

    """
    收益率计算说明：
    1. 用对数收益率（np.log(prices/prices.shift(1))）而非简单收益率，满足可加性，更符合正态分布假设；
    2. dropna() 剔除第一行 NaN（无昨日价格无法计算收益率）。
    3. 年化处理：
    金融领域通常需要年化收益率 / 协方差，避免不同时间频率的结果无法对比；
    年化因子：日频 252（年交易日数）、周频 52、月频 12。
    4. 协方差矩阵修正核心：
    （1）特征值分解后，将负特征值替换为1e-8（极小正数），保证矩阵半正定；
    （2）最后修正矩阵对称性（浮点运算可能导致轻微非对称），符合协方差矩阵的数学特性。
    （3）验证半正定：
    计算修正后矩阵的特征值，若所有特征值≥0（允许微小浮点误差），则满足 CVXPY 的 DCP 规则。
    5. 核心流程：价格→对数收益率→年化期望收益率 / 协方差矩阵→特征值修正半正定矩阵；
    关键修复：通过特征值替换解决协方差矩阵非半正定导致的 CVXPY 报错；
    实用要点：对数收益率 + 年化处理是金融计算的标准做法，修正后的矩阵完全适配凸优化规则。
    """
#==============================================================================
def markowitz_by_lagrange(expected_returns, cov_matrix, target_return,
                          member_names=[],
                          printout=True):
    """
    功能：使用拉格朗日乘数法（矩阵解析解）求解马科维茨模型
    参数：
    expected_returns：mu, 投资组合成分证券的年化预期收益率
    cov_matrix：sigma, 投资组合成分证券年化预期收益率的协方差
    target_return：target_r，投资组合的目标收益率
    member_names：用于打印证券名称
    printout：是否打印结果
    
    说明：
    1. 允许卖空（不能限制卖空）。
    2. target_r不受mu中最大收益率的限制，可以超过之。
    3. 计算公式: w = (1/C) * inv(Sigma) * [ (C*target_r - A)*mu + (B - A*target_r)*1 ]
    其中 A = mu' * inv(Sigma) * 1, B = mu' * inv(Sigma) * mu, C = B*D - A^2, D = 1' * inv(Sigma) * 1
    """
    # 检查参数类型
    if not isinstance(expected_returns, np.ndarray):
        expected_returns=np.array(expected_returns)
    if not isinstance(cov_matrix, np.ndarray):
        cov_matrix=np.array(cov_matrix)
    
    # 使用原变量名
    mu, sigma, target_r=expected_returns, cov_matrix, target_return
    
    inv_sigma = np.linalg.inv(sigma)
    ones = np.ones(len(mu))
    
    A = mu @ inv_sigma @ ones
    B = mu @ inv_sigma @ mu
    D = ones @ inv_sigma @ ones
    C = B * D - A**2
    
    # 计算拉格朗日乘子
    lambda_1 = (B - target_r * A) / C
    lambda_2 = (target_r * D - A) / C
    
    # 计算权重
    weights = inv_sigma @ (lambda_1 * ones + lambda_2 * mu)
        
    # 计算投资组合的风险和收益以验证
    optimal_weights = weights
    portfolio_risk = np.sqrt(optimal_weights @ cov_matrix @ optimal_weights)
    portfolio_return = expected_returns @ optimal_weights
    
    # 输出结果
    if printout:
        titletxt1=text_lang("最优权重：拉格朗日乘数法","Optimal Weights: Lagrange Multiplier Method")
        print(f"\n=== {titletxt1} ===")
        if len(member_names) == len(optimal_weights):
            print(pd.Series(optimal_weights, index=member_names).round(4))
        else:
            print(optimal_weights.round(4))
        
        text1=text_lang("投资组合最小化风险（标准差）","Portfolio minimized risk (std)")
        print(f"\n{text1}: {portfolio_risk.round(4)}")
        
        text2=text_lang("投资组合年化目标收益率","Portfolio target return (annualized)")
        print(f"{text2}: {portfolio_return.round(4)}")


    return optimal_weights, portfolio_risk, portfolio_return

if __name__ == "__main__":
    target_return=0.5
    target_return=1.0
    target_return=2.0
    
    optimal_weights, portfolio_risk, portfolio_return=markowitz_by_lagrange(
                                expected_returns, cov_matrix, target_return,
                                member_names)
    
#==============================================================================
def markowitz_by_qp(expected_returns, cov_matrix, target_return,
                    allow_short_selling=True,
                    member_names=[],
                    printout=True):
    """
    使用二次规划方法（CVXPY + OSQP）求解马科维茨模型
    修正点：统一变量名、动态构建约束列表、高精度求解
    参数：
    expected_returns：mu, 投资组合成分证券的年化预期收益率
    cov_matrix：sigma, 投资组合成分证券年化预期收益率的协方差
    target_return：target_r，投资组合的目标收益率
    allow_short_selling：可选允许卖空或禁止卖空
    member_names：用于打印证券名称
    printout：是否打印结果
    
    说明：
    1. 可选允许卖空（能禁止卖空）。
    2. 允许卖空时，target_r不受mu中最大收益率的限制，可以超过之。
    3. 禁止卖空时，target_r受mu中最大收益率的限制，不可以超过之。

    """
    # 检查参数类型
    if not isinstance(expected_returns, np.ndarray):
        expected_returns=np.array(expected_returns)
    if not isinstance(cov_matrix, np.ndarray):
        cov_matrix=np.array(cov_matrix)

    # 使用原变量名
    mu, sigma, target_r=expected_returns, cov_matrix, target_return
    
    # 检查禁止卖空时目标收益率的限制
    if not allow_short_selling:
        if target_return > expected_returns.max():
            note_txt="#Warning: if selling short is not allowed, target return can not exceed highest member return"
            print(note_txt)
            return None,None,None
            
    n = len(mu)
    
    # 1. 定义变量 (资产权重)
    w = cp.Variable(n)
    
    # 2. 定义目标函数 (最小化组合方差)
    risk = cp.quad_form(w, sigma)
    objective = cp.Minimize(risk)
    
    # 3. 构建约束条件列表 (关键：先建立列表)
    constraints = [
        cp.sum(w) == 1,         # 全投资约束
        mu @ w == target_r     # 目标收益约束
    ]
    
    # 4. 逻辑错误修正：若不允许卖空，向列表中添加非负约束
    if not allow_short_selling:
        constraints.append(w >= 0) 
        
    # 5. 实例化问题并求解
    # 必须在所有约束都确定后再创建 Problem 对象
    prob = cp.Problem(objective, constraints)
    
    # 使用 OSQP 求解器，设置极高精度以对齐拉格朗日法
    prob.solve(solver=cp.OSQP, eps_abs=1e-12, eps_rel=1e-12)
    
    # 6. 结果处理
    optimal_weights = w.value
    
    # 健壮性检查：如果无解，返回空
    if optimal_weights is None:
        return None, None, None

    # 计算投资组合的风险和收益以验证
    # 修正点：使用函数参数 mu 和 sigma，而不是外部变量名
    portfolio_risk = np.sqrt(optimal_weights @ sigma @ optimal_weights)
    portfolio_return = mu @ optimal_weights
    
    # 输出结果
    if printout:
        titletxt1=text_lang("最优权重：二次规划法","Optimal Weights: Quadratic Programming Method")
        print(f"\n=== {titletxt1} ===")
        if len(member_names) == len(optimal_weights):
            print(pd.Series(optimal_weights, index=member_names).round(4))
        else:
            print(optimal_weights.round(4))
        
        text1=text_lang("投资组合最小化风险（标准差）","Portfolio minimized risk (std)")
        print(f"\n{text1}: {portfolio_risk.round(4)}")
        
        text2=text_lang("投资组合年化目标收益率","Portfolio target return (annualized)")
        print(f"{text2}: {portfolio_return.round(4)}")

    return optimal_weights, portfolio_risk, portfolio_return

# --- 测试代码 ---
if __name__ == "__main__":
    # 使用附件数据
    expected_returns = np.array([0.10, 0.15, 0.08])
    cov_matrix = np.array([
        [0.0064, 0.00408, 0.00192],
        [0.00408, 0.0225, 0.0018],
        [0.00192, 0.0018, 0.0009]
    ])
    
    # 执行
    w_res, risk_res, ret_res = markowitz_by_qp(expected_returns,cov_matrix, 0.12, allow_short_selling=True)
    
    if w_res is not None:
        print("求解成功！")
        print(f"权重: {np.round(w_res, 4)}")
        print(f"验证收益率: {ret_res:.4f}")

# ========== 示例：测试代码 ==========
if __name__ == "__main__":
    # --- 数据准备 ---
    expected_returns = np.array([0.10, 0.15, 0.08])
    cov_matrix = np.array([
        [0.0064, 0.00408, 0.00192],
        [0.00408, 0.0225, 0.0018],
        [0.00192, 0.0018, 0.0009]
    ])
    target_return = 0.145
    
    # 执行计算
    weights_lagrange,_,_ = markowitz_by_lagrange(expected_returns, cov_matrix, target_return)
    weights_qp,_,_ = markowitz_by_qp(expected_returns, cov_matrix, target_return)
    
    weights_qp_noshort,_,_ = markowitz_by_qp(expected_returns, cov_matrix, target_return,allow_short_selling=False)
    
    # 打印对比结果
    print(f"目标收益率 (Target Return): {target_return:.2%}")
    print("-" * 50)
    print(f"{'资产':<10} | {'拉格朗日乘数法权重':<15} | {'二次规划(QP)权重':<15} | {'绝对误差':<10}")
    print("-" * 50)
    for i in range(len(expected_returns)):
        err = abs(weights_lagrange[i] - weights_qp[i])
        print(f"资产 {i+1:<7} | {weights_lagrange[i]:>15.6f} | {weights_qp[i]:>15.6f} | {err:>10.2e}")
    
    # 验证收益率
    actual_ret_lagrange = expected_returns @ weights_lagrange
    actual_ret_qp = expected_returns @ weights_qp
    print("-" * 50)
    print(f"验证收益率 (Lagrange): {actual_ret_lagrange:.6f}")
    print(f"验证收益率 (QP):       {actual_ret_qp:.6f}")
    
#==============================================================================
def plot_efficient_frontier(expected_returns, cov_matrix, member_names=[],
                            portfolio_parms=[],
                            loc='best'):
    """
    功能：绘制有效前沿，并对比允许卖空与禁止卖空的差异
    参数：
    expected_returns：mu, 投资组合成分证券的年化预期收益率
    cov_matrix：sigma, 投资组合成分证券年化预期收益率的协方差
    member_names：用于打印证券名称
    
    """
    # 检查参数类型
    if not isinstance(expected_returns, np.ndarray):
        expected_returns=np.array(expected_returns)
    if not isinstance(cov_matrix, np.ndarray):
        cov_matrix=np.array(cov_matrix)

    # 使用原变量名
    mu, sigma=expected_returns, cov_matrix
    
    # 设定收益率范围
    target_rs = np.linspace(min(mu), max(mu), 50)
    
    risks_allow = []
    risks_forbid = []
    
    for r in target_rs:
        # 情况1: 允许卖空
        w_a,_,_ = markowitz_by_qp(mu, sigma, r, True, printout=False)
        if w_a is not None:
            risks_allow.append(np.sqrt(w_a @ sigma @ w_a))
        else:
            risks_allow.append(None)
            
        # 情况2: 禁止卖空
        w_f,_,_ = markowitz_by_qp(mu, sigma, r, False, printout=False)
        if w_f is not None:
            risks_forbid.append(np.sqrt(w_f @ sigma @ w_f))
        else:
            risks_forbid.append(None)

    # 绘图有效边界：对比允许卖空与禁止卖空的有效边界的差异
    #plt.figure(figsize=(10, 6))
    allow_txt=text_lang("允许卖空（最大收益率不受限）",'Allow Short Selling (Unrestricted max return)')
    not_allow_txt=text_lang("禁止卖空（最大收益率受限）",'No Short Selling (Restricted max return)')
    plt.plot(risks_allow, target_rs, 'b--', label=allow_txt)
    plt.plot(risks_forbid, target_rs, 'r-', label=not_allow_txt)
    
    # 绘制各个成分证券的点
    text_offset=0.0005 #标签距离原点的横轴位移
    for i in range(len(mu)):
        if len(mu) != len(member_names):
            #plt.scatter(np.sqrt(sigma[i, i]), mu[i], label=f'Security {i+1}')
            plt.scatter(np.sqrt(sigma[i, i]), mu[i])
            plt.text(np.sqrt(sigma[i, i])+text_offset, mu[i], f'Security {i+1}', fontsize=xlabel_txt_size)
        else:
            #plt.scatter(np.sqrt(sigma[i, i]), mu[i], label=f'{member_names[i]}')
            plt.scatter(np.sqrt(sigma[i, i]), mu[i])
            plt.text(np.sqrt(sigma[i, i])+text_offset, mu[i], f'{member_names[i]}', fontsize=xlabel_txt_size)
    
    # 绘制投资组合的点
    if len(portfolio_parms) == 3:
        plt.scatter(np.sqrt(portfolio_parms[1]), portfolio_parms[0], s=150)
        plt.text(np.sqrt(portfolio_parms[1])+text_offset, portfolio_parms[0], portfolio_parms[2], fontsize=xlabel_txt_size)
    
    titletxt=text_lang("马科维茨模型：有效边界",'Efficient Frontier - Markowitz Model')
    plt.title(titletxt, fontsize=title_txt_size)
    
    xlabeltxt=text_lang("预期风险（标准差）",'Standard Deviation (Risk)')
    plt.xlabel(xlabeltxt, fontsize=xlabel_txt_size)
    
    ylabeltxt=text_lang("预期收益率",'Expected Return')
    plt.ylabel(ylabeltxt, fontsize=ylabel_txt_size)
    
    plt.legend(loc=loc,fontsize=legend_txt_size)
    plt.grid(True)
    plt.show()

# --- 使用拉格朗日法 PDF 中的数据 ---
if __name__ == "__main__":
    # 预期收益率
    mu = np.array([0.10, 0.15, 0.08])
    # 协方差矩阵
    sigma = np.array([
        [0.0064, 0.00408, 0.00192],
        [0.00408, 0.0225, 0.0018],
        [0.00192, 0.0018, 0.0009]
    ])
    
    # 1. 求解特定目标 (如 PDF 中的 12%)
    target = 0.12
    weights = solve_markowitz(mu, sigma, target, allow_short_selling=True)
    
    print(f"目标收益率: {target:.2%}")
    if weights is not None:
        print(f"最优权重分配: {np.round(weights, 4)}")
        print(f"组合风险(标准差): {np.sqrt(weights @ sigma @ weights):.4f}")
    
    # 2. 绘制前沿曲线 (如果在本地运行可查看图表)
    plot_efficient_frontier(mu, sigma, member_names, loc='center')
#==============================================================================
if __name__=='__main__':
    portfolio={'Market':('CN','000001.SS','银行概念基金1号'),
               '601939.SS':.03,'600000.SS':.02,'601998.SS':.8,'601229.SS':.15}
    

def efficient_frontier_demo(portfolio, start='MRY', end='today',
                            indicator='Adj Close', loc='best'):
    """
    功能：给定一个投资组合，演示其有效边界，对比允许卖空与禁止卖空
    参数：
    portfolio：投资组合
    indicator：价格种类，默认前复权价'Adj Close'，假定红利全部再投资，以避免分红的影响
    loc：图例位置，默认自动'best'，多数情况下'center'可能效果更好
    """
    
    # 提取成分证券列表
    _,_,stocklist,_,_=decompose_portfolio(portfolio)
    
    # 收集成分证券价格
    prices=security_trend(stocklist, start=start, end=end, indicator=indicator, graph=False)
    
    # 计算成分证券的期望收益率和协方差矩阵（按日收益率年化）
    expected_returns, cov_matrix, member_names = member_returns_covariance(prices,printout=False)
    
    # 收集投资组合价格
    p_prices=security_trend(portfolio, start=start, end=end, indicator=indicator, graph=False)[[indicator]]
    
    # 计算投资组合的期望收益率和协方差矩阵（按日收益率年化）
    p_expected_returns, p_cov_matrix, _ = member_returns_covariance(p_prices,printout=False)
    p_name=portfolio_name(portfolio)   
    portfolio_parms=[p_expected_returns, p_cov_matrix, p_name]
    
    
    # 绘制有效边界
    plot_efficient_frontier(expected_returns, cov_matrix, member_names, portfolio_parms, loc=loc)
    
    return


#==============================================================================




