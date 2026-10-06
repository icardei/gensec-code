from fastmcp import FastMCP
import sqlite3
import sys

mcp = FastMCP("secure_sqlite")
con = sqlite3.connect('db_data/metactf_users.db')

@mcp.tool()
async def fetch_users() -> list:
    """Fetch the users in the database.  Takes no arguments and returns a list of users."""
    cur = con.cursor()
    res = cur.execute('SELECT username from USERS')
    return res.fetchall()

@mcp.tool()
async def fetch_users_pass(username: str) -> str:
   """Useful when you want to fetch a password hash for a particular user.  Takes a username as a string argument.  Returns a string"""
   cur = con.cursor()
   cur.execute(f"SELECT passhash FROM users WHERE username = ?;",(username,))
   row = cur.fetchone()
   if row is None or not isinstance(row, (tuple, list)) or len(row) == 0:
       return ""
   return row[0]

if __name__ == "__main__":
    if sys.argv[1] == 'stdio':
        mcp.run(transport="stdio")
    else:
        mcp.run(transport="http", host="0.0.0.0", port=8080)
