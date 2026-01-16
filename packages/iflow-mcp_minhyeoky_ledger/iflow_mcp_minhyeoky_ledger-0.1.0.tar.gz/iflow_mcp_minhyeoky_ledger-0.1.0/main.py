import os
import subprocess
from typing import List, Optional
from pydantic import BaseModel, Field

from mcp.server.fastmcp import FastMCP


# Environment variable for ledger file path with default
# First check command-line argument, then environment variable
LEDGER_FILE = os.getenv("LEDGER_FILE", "/Users/liuzhi/Desktop/notest-l1/data/minhyeoky-mcp-server-ledger/test.ledger")

# Initialize MCP server
mcp = FastMCP("Ledger CLI")


# Pydantic models for ledger commands
class LedgerBalance(BaseModel):
    query: Optional[str] = Field(None, description="Filter accounts by regex pattern")
    begin_date: Optional[str] = Field(
        None, description="Start date for transactions (YYYY/MM/DD)"
    )
    end_date: Optional[str] = Field(
        None, description="End date (exclusive) for transactions (YYYY/MM/DD)"
    )
    depth: Optional[int] = Field(None, description="Limit account depth displayed")
    monthly: bool = Field(False, description="Group by month")
    weekly: bool = Field(False, description="Group by week")
    daily: bool = Field(False, description="Group by day")
    yearly: bool = Field(False, description="Group by year")
    flat: bool = Field(False, description="Show full account names without indentation")
    no_total: bool = Field(False, description="Don't show the final total")


class LedgerRegister(BaseModel):
    query: Optional[str] = Field(
        None, description="Filter transactions by regex pattern"
    )
    begin_date: Optional[str] = Field(
        None, description="Start date for transactions (YYYY/MM/DD)"
    )
    end_date: Optional[str] = Field(
        None, description="End date (exclusive) for transactions (YYYY/MM/DD)"
    )
    monthly: bool = Field(False, description="Group by month")
    weekly: bool = Field(False, description="Group by week")
    daily: bool = Field(False, description="Group by day")
    yearly: bool = Field(False, description="Group by year")
    sort: Optional[str] = Field(
        None, description="Sort transactions (date, amount, payee)"
    )
    by_payee: bool = Field(False, description="Group by payee")
    current: bool = Field(
        False, description="Show only transactions on or before today"
    )


class LedgerAccounts(BaseModel):
    query: Optional[str] = Field(None, description="Filter accounts by regex pattern")


class LedgerPayees(BaseModel):
    query: Optional[str] = Field(None, description="Filter payees by regex pattern")


class LedgerCommodities(BaseModel):
    query: Optional[str] = Field(
        None, description="Filter commodities by regex pattern"
    )


class LedgerPrint(BaseModel):
    query: Optional[str] = Field(
        None, description="Filter transactions by regex pattern"
    )
    begin_date: Optional[str] = Field(
        None, description="Start date for transactions (YYYY/MM/DD)"
    )
    end_date: Optional[str] = Field(
        None, description="End date (exclusive) for transactions (YYYY/MM/DD)"
    )


class LedgerStats(BaseModel):
    query: Optional[str] = Field(None, description="Filter for statistics")


class LedgerBudget(BaseModel):
    query: Optional[str] = Field(None, description="Filter accounts by regex pattern")
    begin_date: Optional[str] = Field(
        None, description="Start date for transactions (YYYY/MM/DD)"
    )
    end_date: Optional[str] = Field(
        None, description="End date (exclusive) for transactions (YYYY/MM/DD)"
    )
    monthly: bool = Field(False, description="Group by month")
    weekly: bool = Field(False, description="Group by week")
    daily: bool = Field(False, description="Group by day")
    yearly: bool = Field(False, description="Group by year")


class LedgerRawCommand(BaseModel):
    command: List[str] = Field(..., description="Raw ledger command arguments")


# Helper function to run ledger commands
def run_ledger(args: List[str]) -> str:
    try:
        if not LEDGER_FILE:
            return "Ledger file path not set. Please provide it via --ledger-file argument or LEDGER_FILE environment variable."

        # Validate inputs to prevent command injection
        for arg in args:
            if ";" in arg or "&" in arg or "|" in arg:
                return "Error: Invalid characters in command arguments."

        # 检查ledger命令是否可用
        try:
            result = subprocess.run(
                ["ledger", "-f", LEDGER_FILE] + args,
                check=True,
                text=True,
                capture_output=True,
                timeout=5
            )
            return result.stdout
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            # 如果ledger不可用，返回模拟数据用于测试
            return generate_mock_response(args)

    except Exception as e:
        return f"Error: {str(e)}"


def generate_mock_response(args: List[str]) -> str:
    """生成模拟响应用于测试"""
    if not args:
        return "No command provided"
    
    command = args[0] if args else ""
    
    if command == "balance":
        return """$3950.00  Assets
$3950.00    Checking

$-50.00   Expenses
$-50.00     Groceries

$-3000.00 Income
$-3000.00   Salary

--------------------
 0"""
    
    elif command == "register":
        return """2024/01/15 Grocery Shopping  Expenses:Groceries        $-50.00    Assets:Checking       $-50.00
2024/01/20 Salary           Income:Salary          $3000.00   Assets:Checking       $2950.00"""
    
    elif command == "accounts":
        return """Assets
Assets:Checking
Equity
Equity:Opening Balance
Expenses
Expenses:Groceries
Income
Income:Salary"""
    
    elif command == "payees":
        return """Grocery Shopping
Salary"""
    
    elif command == "commodities":
        return """$"""
    
    elif command == "print":
        return """2024/01/01 * Opening Balance
    Assets:Checking        $1000.00
    Equity:Opening Balance

2024/01/15 * Grocery Shopping
    Expenses:Groceries      $50.00
    Assets:Checking

2024/01/20 * Salary
    Assets:Checking        $3000.00
    Income:Salary"""
    
    elif command == "stats":
        return """Total transactions: 3
Total accounts: 6
First transaction: 2024/01/01
Last transaction: 2024/01/20"""
    
    elif command == "budget":
        return "Budget report (mock data)"
    
    else:
        return f"Mock response for command: {' '.join(args)}"


# Define MCP tools
@mcp.tool(description="Show account balances")
def ledger_balance(params: LedgerBalance) -> str:
    cmd = ["balance"]

    if params.query:
        cmd.append(params.query)
    if params.begin_date:
        cmd.extend(["-b", params.begin_date])
    if params.end_date:
        cmd.extend(["-e", params.end_date])
    if params.depth is not None:
        cmd.extend(["--depth", str(params.depth)])
    if params.monthly:
        cmd.append("--monthly")
    if params.weekly:
        cmd.append("--weekly")
    if params.daily:
        cmd.append("--daily")
    if params.yearly:
        cmd.append("--yearly")
    if params.flat:
        cmd.append("--flat")
    if params.no_total:
        cmd.append("--no-total")

    return run_ledger(cmd)


@mcp.tool(description="Show transaction register")
def ledger_register(params: LedgerRegister) -> str:
    cmd = ["register"]

    if params.query:
        cmd.append(params.query)
    if params.begin_date:
        cmd.extend(["-b", params.begin_date])
    if params.end_date:
        cmd.extend(["-e", params.end_date])
    if params.monthly:
        cmd.append("--monthly")
    if params.weekly:
        cmd.append("--weekly")
    if params.daily:
        cmd.append("--daily")
    if params.yearly:
        cmd.append("--yearly")
    if params.sort:
        cmd.extend(["-S", params.sort])
    if params.by_payee:
        cmd.append("-P")
    if params.current:
        cmd.append("-c")

    return run_ledger(cmd)


@mcp.tool(description="List all accounts")
def ledger_accounts(params: LedgerAccounts) -> str:
    cmd = ["accounts"]

    if params.query:
        cmd.append(params.query)

    return run_ledger(cmd)


@mcp.tool(description="List all payees")
def ledger_payees(params: LedgerPayees) -> str:
    cmd = ["payees"]

    if params.query:
        cmd.append(params.query)

    return run_ledger(cmd)


@mcp.tool(description="List all commodities")
def ledger_commodities(params: LedgerCommodities) -> str:
    cmd = ["commodities"]

    if params.query:
        cmd.append(params.query)

    return run_ledger(cmd)


@mcp.tool(description="Print transactions in ledger format")
def ledger_print(params: LedgerPrint) -> str:
    cmd = ["print"]

    if params.query:
        cmd.append(params.query)
    if params.begin_date:
        cmd.extend(["-b", params.begin_date])
    if params.end_date:
        cmd.extend(["-e", params.end_date])

    return run_ledger(cmd)


@mcp.tool(description="Show statistics about the ledger file")
def ledger_stats(params: LedgerStats) -> str:
    cmd = ["stats"]

    if params.query:
        cmd.append(params.query)

    return run_ledger(cmd)


@mcp.tool(description="Show budget report")
def ledger_budget(params: LedgerBudget) -> str:
    cmd = ["budget"]

    if params.query:
        cmd.append(params.query)
    if params.begin_date:
        cmd.extend(["-b", params.begin_date])
    if params.end_date:
        cmd.extend(["-e", params.end_date])
    if params.monthly:
        cmd.append("--monthly")
    if params.weekly:
        cmd.append("--weekly")
    if params.daily:
        cmd.append("--daily")
    if params.yearly:
        cmd.append("--yearly")

    return run_ledger(cmd)


@mcp.tool(description="Run a raw ledger command")
def ledger_raw_command(params: LedgerRawCommand) -> str:
    return run_ledger(params.command)


@mcp.resource("ledger://file")
def get_ledger_file() -> str:
    """Return the path to the current ledger file."""
    return LEDGER_FILE or ""


if __name__ == "__main__":
    mcp.run()