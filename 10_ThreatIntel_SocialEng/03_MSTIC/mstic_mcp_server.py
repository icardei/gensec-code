from fastmcp import FastMCP, Context
from msticpy.context.tilookup import TILookup
from msticpy.context.vtlookupv3.vtlookupv3 import VTLookupV3
from msticpy.common.provider_settings import get_provider_settings
import json
import sys
import nest_asyncio

nest_asyncio.apply()

mcp = FastMCP("Mstic")

vt_key = get_provider_settings("TIProviders")["VirusTotal"].args["AuthKey"]

@mcp.tool("ip_info")
async def ip_info(ip_address: str):
    """(CHANGE ME)"""
    result = TILookup().lookup_ioc(observable=ip_address, ioc_type="ipv4", providers=["VirusTotal"])
    details = result.at[0, 'RawResult']
    comm_samples = details['detected_communicating_samples']
    return json.dumps(comm_samples)

@mcp.tool("samples_hash_identification")
async def samples_hash_identification(hash_string: str, ctx: Context = None):
    """(CHANGE ME)"""
    vt_lookup = VTLookupV3(vt_key=vt_key, force_nestasyncio=True)
    result = vt_lookup.get_object(hash_string, "file")
    json_result = result.to_json(orient='records')
    return json_result

if __name__ == "__main__":
    if sys.argv[1] == 'stdio':
        mcp.run(transport="stdio")
    else:
        mcp.run(transport="http", host="0.0.0.0", port=8080)
