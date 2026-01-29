# LeetCLI

**LeetCLI** is a command-line interface (CLI) tool to interact with [LeetCode](https://leetcode.com) directly from your terminal.  
You can search, view, download, run sample testcases, and submit solutions without opening a browser.

---

## Features

-Login/logout using your `LEETCODE_SESSION` cookie.

-List problems with pagination.

-Search problems by keyword.

-View problem description in Markdown.

-Download starter code for your preferred language.

-Run official sample testcases locally.

-Submit solutions to LeetCode.

-Show daily challenge and user stats.

---
## LeetCode CLI – Commands

| Command | Example | Description |
|--------|---------|-------------|
| **login** | `lc login` | Login by pasting `LEETCODE_SESSION` cookie |
| **logout** | `lc logout` | Remove saved session |
| **list** | `lc list --limit 50 --skip 0` | List problems with optional pagination |
| **search** | `lc search "two sum"` | Search problems by keyword and pick one to view |
| **view** | `lc view two-sum` | View full problem description by slug |
| **download** | `lc download two-sum --lang python3` | Download starter code |
| **run** | `lc run two-sum --file solution.py --lang python3` | Run your solution on LeetCode’s official sample testcases |
| **submit** | `lc submit two-sum solution.py` | Submit solution to LeetCode |
| **daily** | `lc daily` | Show today’s daily challenge |
| **stats** | `lc stats` | Show stats for logged-in user or given username |
| **home** | `lc` | Show welcome screen |
| **help** | `lc help` | Show this help table |


---
## Installation

Install via pip:

```bash
pip install leetcode-terminal


