from fastmcp import FastMCP
import sqlite3
import sys

mcp = FastMCP("sqlite")
con = sqlite3.connect('db_data/metactf_users.db')

@mcp.tool()
async def query(query: str) -> list:
    """Query a specified Sqlite3 database. Takes a SQL query string as an input parameter and returns the result of the query as a list of lists."""
    cur = con.cursor()
    res = cur.execute(query)
    con.commit()
    return res.fetchall()

if __name__ == "__main__":
    if sys.argv[1] == 'stdio':
        mcp.run(transport="stdio")
    else:
        mcp.run(transport="http", host="0.0.0.0", port=8080)
