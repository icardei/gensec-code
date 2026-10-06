from fastmcp import FastMCP
from auth import get_drive_service

mcp = FastMCP("Google Drive")

@mcp.tool("list_files")
async def list_files():
    """
    List files in Google Drive.
    """
    service = get_drive_service()
    
    results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    
    if not items:
        return "No files found in Google Drive."
    
    file_list = [f"{item['name']} (ID: {item['id']})" for item in items]
    return "\n".join(file_list)

@mcp.tool("get_file")
async def get_file(file_id: str):
    """
    Get a file from Google Drive by its ID.
    """
    service = get_drive_service()
    
    try:
        file = service.files().get(fileId=file_id, fields='id, name').execute()
        return f"File found: {file['name']} (ID: {file['id']})"
    except Exception as e:
        return f"Error retrieving file: {str(e)}"
    
@mcp.tool("rename_file")
async def rename_file(file_id: str, new_name: str):
    """
    Rename a file in Google Drive by referencing with it's file ID.
    """
    body = {'name': new_name}

    service = get_drive_service()
    try:
        service.files().update(fileId=file_id, body=body).execute()
    except Exception as e:
        return f"Error: {str(e)}"
    
@mcp.tool("delete_file")
async def delete_file(file_id: str):
    """
    Delete a file in Google Drive by referencing with it's file ID.
    """
    service = get_drive_service()
    
    try:
        service.files().delete(fileId=file_id).execute()
        return f"File with ID {file_id} deleted successfully."
    except Exception as e:
        return f"Error deleting file: {str(e)}"

@mcp.tool("create_folder")
async def create_folder(folder_name: str):
    """
    Create a folder in Google Drive.
    """
    service = get_drive_service()
    
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    
    try:
        folder = service.files().create(body=file_metadata, fields='id').execute()
        return f"Folder created with ID: {folder['id']}"
    except Exception as e:
        return f"Error creating folder: {str(e)}"
    

if __name__ == "__main__":
    mcp.run(transport='http', host="0.0.0.0", port=8080)