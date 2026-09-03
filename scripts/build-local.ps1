[CmdletBinding()]
param(
    [string[]]$Datasets = @("cbdb", "ctext", "niutrans"),
    [switch]$InstallDependencies
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$PipelineRoot = Split-Path -Parent $PSScriptRoot
Push-Location $PipelineRoot
try {
    $VenvPython = Join-Path $PipelineRoot ".venv\Scripts\python.exe"
    if (Test-Path -LiteralPath $VenvPython) {
        $Python = $VenvPython
    } else {
        $PythonCommand = Get-Command python -ErrorAction Stop
        $Python = $PythonCommand.Source
    }

    if ($InstallDependencies) {
        & $Python -m pip install -r requirements.txt
        if ($LASTEXITCODE -ne 0) { throw "依赖安装失败" }
    }

    foreach ($Dataset in $Datasets) {
        & $Python -m src.history_data_pipeline download $Dataset
        if ($LASTEXITCODE -ne 0) { throw "下载失败: $Dataset" }
    }

    & $Python -m src.history_data_pipeline parse
    if ($LASTEXITCODE -ne 0) { throw "解析失败" }

    & $Python -m src.history_data_pipeline build --from-staging
    if ($LASTEXITCODE -ne 0) { throw "构建数据库失败" }

    & $Python -m src.history_data_pipeline validate
    if ($LASTEXITCODE -ne 0) { throw "数据校验失败" }

    & $Python -m src.history_data_pipeline stats
    if ($LASTEXITCODE -ne 0) { throw "统计生成失败" }

    & $Python -m src.history_data_pipeline export
    if ($LASTEXITCODE -ne 0) { throw "导出失败" }

    # --- Layer 3/4：Backbone 校验 + dist 构建（应用只读 dist/） ---
    & $Python -m src.history_data_pipeline backbone validate
    if ($LASTEXITCODE -ne 0) { throw "Backbone 校验失败" }

    & $Python -m src.history_data_pipeline backbone build --knowledge (Join-Path $PipelineRoot "data\normalized\history.duckdb")
    if ($LASTEXITCODE -ne 0) { throw "Backbone 构建失败" }

    & $Python -m src.history_data_pipeline backbone coverage
    if ($LASTEXITCODE -ne 0) { throw "Backbone 覆盖报告失败" }

    & $Python -m pytest -q
    if ($LASTEXITCODE -ne 0) { throw "测试失败" }
} finally {
    Pop-Location
}
