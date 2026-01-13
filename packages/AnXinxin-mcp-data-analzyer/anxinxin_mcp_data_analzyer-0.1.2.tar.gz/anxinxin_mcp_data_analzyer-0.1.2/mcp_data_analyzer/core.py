from mcp.server import Server
from mcp.types import TextContent, Tool
import httpx
import json
import os
import asyncio
import os
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, Any, List

# -------------------------- 全局配置（必须加，解决matplotlib中文乱码+负号显示问题） --------------------------
plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
# 设置图表清晰度
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 150

# 重写JSON序列化器，让它认识numpy的所有数值类型
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer): return int(obj)
        if isinstance(obj, np.floating): return float(obj)
        return super().default(obj)

# 替换全局序列化方法
json.JSONEncoder.default = NumpyEncoder.default
# ==========================================================================================


class DataAnalyzerServer(Server):
    def __init__(self, name):
        super().__init__(name)
        self.__amap_key = None

        @property
        def amap_key(self):
            return self._amap_key
        
        @amap_key.setter
        def amap_key(self,value):
            self._amap_key = value


app = DataAnalyzerServer("DataAnalyzer")


@app.call_tool()
async def call_tool(name:str,arguments:dict)->list[TextContent]:
    if name == "data_overview":
        return await data_overview(arguments["data_path"])
    elif name == "visualize_data":
        data_path = arguments["arguments"]
        index = arguments["index"]
        values = arguments["values"]
        aggfunc = arguments.get("aggfunc","sum")
        out_dir = arguments.get("output_dir", "./output")
        return await visualize_data(arguments[data_path,index,values,aggfunc,out_dir])
    elif name == "data_summary":
        return await data_summary(arguments["data_path"])
    else:
        return  [TextContent(type="text", text=f"not support function call")]


@app.list_tools()
async def list_tools()->list[Tool]:
    return [
        Tool(
            name="data_overview",
            description="获取数据的大概情况，例如表头信息、表头对应的字段类型、数据条数",
            inputSchema={
                "type":"object",
                "properties":{
                    "data_path":{
                        "type":"string",
                        "description":"数据文件的路径，支持.csv|.xlsx|.xls格式"
                    }
                },
                "required":["data_path"]
            }
        ),
        Tool(
            name="visualize_data",
            description="通过数据透视的方式可视化数据",
            inputSchema={
                "type":"object",
                "properties":{
                    "data_path":{
                        "type":"string",
                        "description":"数据文件的路径，支持.csv|.xlsx|.xls格式"
                    },
                    "index":{
                        "type":"array",
                        "description":"数据透视的索引列名列表, 支持1~2维度, 如[‘城市’，‘季度’]",
                        "items":{
                            "type":"array"
                        }
                    },
                    "values":{
                        "type":"array",
                        "description":"需要聚合的数值列表, 如['销量', '销售额']",
                        "item":{
                            "type":"string"
                        }

                    },
                    "aggfunc":{
                        "type":"string",
                        "description":"聚合函数, 支持sum | mean | count | max | min | median | std | var, 默认是sum"
                    },
                    "out_dir":{
                        "type":"string",
                        "description":"聚合图标的保存目录, 默认./output"
                    }
                },
                "required":["data_path","index","value"]
            }
        ),
        Tool(
            name="data_summary",
            description="获取数据的汇总分析情况，例如整体数据的平均值、中位数、方差等等",
            inputSchema={
                "type":"object",
                "properties":{
                    "data_path":{
                        "type":"string",
                        "description":"数据文件的路径，支持.csv|.xlsx|.xls格式"
                    }
                },
                "required":["data_path"]
            }
        ),

    ]

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Any, List

# ========== 新增1行：解决matplotlib无GUI环境绘图报错（必加，Windows/MCP必踩坑） ==========
plt.switch_backend('AGG')

async def data_overview(data_path: str) -> Dict[str, Any]:
    """
    异步获取数据的概览信息
    :param data_path: 数据文件的路径，支持.csv|.xlsx|.xls格式
    :return: 结构化的字典数据，包含所有概览信息
    """
    try:
        # 校验文件是否存在
        if not os.path.exists(data_path):
            return {"code": -1, "msg": f"错误：文件路径不存在 -> {data_path}", "data": None}
        
        # 异步读取不同格式的文件 + 解决中文乱码
        file_suffix = data_path.strip().split(".")[-1].lower()
        if file_suffix == "csv":
            df = pd.read_csv(data_path, encoding='utf-8-sig')  # ✔️ 修复中文乱码
        elif file_suffix in ["xlsx", "xls"]:
            df = pd.read_excel(data_path)
        else:
            return {"code": -1, "msg": f"错误：不支持的文件格式 -> {file_suffix}，仅支持csv/xlsx/xls", "data": None}
        
        # 整理数据概览核心信息 ✔️ 全部修复序列化报错点，极简修改
        data_info = {
            "数据总行数": len(df),
            "数据总列数": len(df.columns),
            "表头字段列表": list(df.columns),
            "字段对应数据类型": {k: str(v) for k, v in df.dtypes.items()},  # ✔️ 核心修复：Dtype对象转字符串
            "各字段非空值数量": dict(df.count().astype(int).fillna(0)),      # ✔️ 核心修复：Int64转原生int
            "各字段缺失值数量": dict(df.isnull().sum().astype(int).fillna(0)), # ✔️ 核心修复：Int64转原生int
            "各字段缺失值占比(%)": dict(round(df.isnull().sum() / len(df) * 100, 2))
        }
        
        return {"code": 0, "msg": "数据概览获取成功", "data": data_info}
    
    except Exception as e:
        return {"code": -1, "msg": f"数据概览读取失败：{str(e)}", "data": None}


async def data_summary(data_path: str) -> Dict[str, Any]:
    """
    异步获取数据的完整汇总分析（数值型字段）
    :param data_path: 数据文件的路径，支持.csv|.xlsx|.xls格式
    :return: 结构化的字典数据，包含所有统计指标
    """
    try:
        # 校验文件是否存在
        if not os.path.exists(data_path):
            return {"code": -1, "msg": f"错误：文件路径不存在 -> {data_path}", "data": None}
        
        # 异步读取不同格式的文件 + 解决中文乱码
        file_suffix = data_path.strip().split(".")[-1].lower()
        if file_suffix == "csv":
            df = pd.read_csv(data_path, encoding='utf-8-sig')  # ✔️ 修复中文乱码
        elif file_suffix in ["xlsx", "xls"]:
            df = pd.read_excel(data_path)
        else:
            return {"code": -1, "msg": f"错误：不支持的文件格式 -> {file_suffix}，仅支持csv/xlsx/xls", "data": None}
        
        # 只对【数值型字段】做汇总统计（平均值/中位数/方差等），过滤文本/时间类型
        numeric_df = df.select_dtypes(include=['int64', 'float64'])
        if numeric_df.empty:
            return {"code": 0, "msg": "数据中无数值型字段，无需统计", "data": None}
        
        # 获取完整统计指标 + 补充中位数/方差
        describe_df = numeric_df.describe().round(2)
        describe_df.loc["median"] = numeric_df.median().round(2)  # 中位数
        describe_df.loc["var"] = numeric_df.var().round(2)       # 方差
        describe_df.loc["std"] = numeric_df.std().round(2)       # 标准差
        
        # 转换为结构化字典 ✔️ 核心修复：浮点型特殊类型转原生float，序列化必过
        summary_info = describe_df.astype(float).fillna(0).to_dict()
        
        return {"code": 0, "msg": "数据汇总分析获取成功", "data": summary_info}
    
    except Exception as e:
        return {"code": -1, "msg": f"数据汇总分析失败：{str(e)}", "data": None}


async def visualize_data(
    data_path: str,
    index: List[str],
    values: List[str],
    aggfunc: str = "sum",
    out_dir: str = "./output"
) -> Dict[str, Any]:
    """
    异步通过数据透视的方式可视化数据，并保存图表到指定目录
    :param data_path: 数据文件的路径，支持.csv|.xlsx|.xls格式
    :param index: 数据透视的索引列名列表, 支持1~2维度, 如['城市', '季度']
    :param values: 需要聚合的数值列表, 如['销量', '销售额']
    :param aggfunc: 聚合函数, 支持sum | mean | count | max | min | median | std | var, 默认是sum
    :param out_dir: 聚合图表的保存目录, 默认./output
    :return: 结构化的字典数据，包含保存路径+透视表数据
    """
    # 合法聚合函数校验
    valid_aggfuncs = ["sum", "mean", "count", "max", "min", "median", "std", "var"]
    aggfunc = aggfunc.lower()
    if aggfunc not in valid_aggfuncs:
        return {"code": -1, "msg": f"错误：聚合函数非法 -> {aggfunc}，仅支持：{','.join(valid_aggfuncs)}", "data": None}
    
    # 索引维度校验（1-2维度）
    if len(index) not in [1, 2]:
        return {"code": -1, "msg": f"错误：索引维度非法 -> {len(index)}维，仅支持1~2维度", "data": None}

    try:
        # 校验文件是否存在
        if not os.path.exists(data_path):
            return {"code": -1, "msg": f"错误：文件路径不存在 -> {data_path}", "data": None}
        
        # 自动创建输出目录（不存在则创建）
        os.makedirs(out_dir, exist_ok=True)
        
        # 异步读取不同格式的文件 + 解决中文乱码
        file_suffix = data_path.strip().split(".")[-1].lower()
        if file_suffix == "csv":
            df = pd.read_csv(data_path, encoding='utf-8-sig')  # ✔️ 修复中文乱码
        elif file_suffix in ["xlsx", "xls"]:
            df = pd.read_excel(data_path)
        else:
            return {"code": -1, "msg": f"错误：不支持的文件格式 -> {file_suffix}，仅支持csv/xlsx/xls", "data": None}
        
        # 校验传入的列名是否存在于数据中
        all_columns = list(df.columns)
        for col in index + values:
            if col not in all_columns:
                return {"code": -1, "msg": f"错误：字段 {col} 不存在于数据表中，数据表字段：{all_columns}", "data": None}
        
        # ✅ 核心：生成数据透视表
        pivot_df = pd.pivot_table(
            data=df,
            index=index,
            values=values,
            aggfunc=aggfunc,
            fill_value=0  # 缺失值填充为0
        )
        
        # ✅ 核心：绘制可视化图表（适配1/2维度，自动调整样式）
        fig, ax = plt.subplots(figsize=(12, 6))
        pivot_df.plot(kind="bar", ax=ax, width=0.8)
        
        # 设置图表标题和标签
        agg_name = {"sum": "求和", "mean": "平均值", "count": "计数", "max": "最大值", "min": "最小值",
                    "median": "中位数", "std": "标准差", "var": "方差"}.get(aggfunc, aggfunc)
        ax.set_title(f"数据透视分析图 - {agg_name} | 索引：{','.join(index)}", fontsize=14, pad=20)
        ax.set_xlabel("索引维度", fontsize=12)
        ax.set_ylabel(f"{agg_name}数值", fontsize=12)
        ax.legend(title="聚合字段", bbox_to_anchor=(1.02, 1), loc="upper left")
        
        # 自动调整布局，防止标签重叠
        plt.tight_layout()
        
        # 保存图表到指定目录
        file_name = f"透视分析_{'_'.join(index)}_{aggfunc}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.png"
        save_path = os.path.join(out_dir, file_name)
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()  # 关闭画布，释放内存，避免内存泄漏
        
        # 整理返回数据 ✔️ 核心修复：透视表数据序列化报错
        return {
            "code": 0,
            "msg": f"数据透视可视化成功，图表已保存",
            "data": {
                "图表保存路径": save_path,
                "聚合函数": aggfunc,
                "透视索引维度": index,
                "聚合数值字段": values,
                "透视表数据(前10行)": pivot_df.head(10).astype(float).fillna(0).round(2).to_dict(), # ✔️ 修复序列化
                "透视表总行数": len(pivot_df)
            }
        }
    
    except Exception as e:
        return {"code": -1, "msg": f"数据透视可视化失败：{str(e)}", "data": None}

async def serve():
    from mcp.server.stdio import stdio_server
    async def arun():
        async with stdio_server() as streams:
            await app.run(streams[0],streams[1],app.create_initialization_options())
    await arun()


