@echo off
chcp 65001 >nul
REM 一键运行完整实验流程（Windows版本）

echo ========================================================================
echo 心理咨询系统 - 完整实验流程
echo ========================================================================
echo.
echo 本脚本将执行以下步骤：
echo 1. 添加知识库文件（心理学知识 + 用户档案）
echo 2. 运行对比实验（裸LLM vs RAG vs 完整系统）
echo 3. 生成可视化图表和分析报告
echo.
pause
echo.

REM 步骤1: 添加知识库
echo ========================================================================
echo 步骤 1/3: 添加知识库
echo ========================================================================
python examples\add_knowledge.py

if errorlevel 1 (
    echo.
    echo ❌ 错误: 知识库添加失败
    echo 请检查：
    echo   1. 是否安装了所有依赖: pip install -r requirements.txt
    echo   2. 是否配置了API密钥（如果使用API模式）
    echo   3. data\sample_knowledge\ 和 data\sample_user_info\ 是否存在
    pause
    exit /b 1
)

echo.
pause
echo.

REM 步骤2: 运行对比实验
echo ========================================================================
echo 步骤 2/3: 运行对比实验
echo ========================================================================
echo 注意: 此步骤可能需要几分钟时间，请耐心等待...
echo.

python examples\comparison_experiment.py

if errorlevel 1 (
    echo.
    echo ❌ 错误: 对比实验失败
    echo 请检查配置文件和LLM后端设置
    pause
    exit /b 1
)

echo.
pause
echo.

REM 步骤3: 生成可视化
echo ========================================================================
echo 步骤 3/3: 生成可视化图表
echo ========================================================================

python examples\visualize_results.py

if errorlevel 1 (
    echo.
    echo ❌ 错误: 可视化生成失败
    echo 可能需要安装: pip install matplotlib numpy
    pause
    exit /b 1
)

echo.
echo ========================================================================
echo ✅ 完整实验流程执行成功！
echo ========================================================================
echo.
echo 生成的文件位置：
echo   📊 图表: experiments\figures\
echo   📄 详细报告: experiments\detailed_comparison.md
echo   📝 响应示例: experiments\response_examples.md
echo   📦 原始数据: experiments\comparison_report_*.json
echo.
echo 这些文件可以直接用于论文写作！
echo.
echo 下一步：
echo   1. 查看 experiments\ 目录中的所有结果
echo   2. 将图表插入到论文中
echo   3. 引用实验数据和案例分析
echo.
echo 祝论文写作顺利！🎓
echo ========================================================================
pause
