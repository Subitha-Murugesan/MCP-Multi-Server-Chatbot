from mcp.server.fastmcp import FastMCP

mcp=FastMCP("weather")

@mcp.tool()
async def get_weather(city:str)->str:
    """Get the weather of a city"""
    return f"The weather of {city} is sunny"

if __name__=="__main__":
    mcp.run(transport="streamable-http")
    #WHEN we run this server, this server will acts as api endpoint
    #stdio is not run like this, just a standard input output
