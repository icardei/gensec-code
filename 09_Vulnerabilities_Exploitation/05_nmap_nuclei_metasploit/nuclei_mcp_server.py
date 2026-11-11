from fastmcp import FastMCP, Context
import os

mcp = FastMCP("Nuclei")

@mcp.tool("nuclei_scan")
async def nuclei_scan(target: str, ctx: Context = None):
    """
    Perform an Nuclei vulnerability scan on the specified target. 
    Returns the scan results as a string.
    Example usage:
    nuclei_scan("http://example.com")
    The target can be a URL or an IP address.
    """
    try:
        # Construct the Nuclei command
        command = f"nuclei -u {target} -o /tmp/nuclei_output.txt"
        command = command.replace(";", "").replace("&", "").replace("|", "")
        
        os.system(command)
        
        # Decode the result from bytes to string
        with open("/tmp/nuclei_output.txt", "r") as f:
            return f.read()
    except Exception as e:
        return f"Error during Nuclei scan: {str(e)}"
    
if __name__ == "__main__":
    mcp.run(transport="stdio")
