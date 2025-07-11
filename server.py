# from mcp.server.fastmcp import FastMCP
# import requests
# from bs4 import BeautifulSoup
# from youtube_transcript_api import YouTubeTranscriptApi
# import re
# from typing import List, Dict, Optional

# # Create an MCP server
# mcp = FastMCP("Enhanced Demo")

# # Add the original addition tool
# @mcp.tool()
# def add(a: int, b: int) -> int:
#     """Add two numbers"""
#     return a + b

# # Add the original greeting resource
# @mcp.resource("greeting://{name}")
# def get_greeting(name: str) -> str:
#     """Get a personalized greeting"""
#     return f"Hello, {name}!"

# # YouTube video information tool
# @mcp.tool()
# def get_youtube_video_info(video_url: str) -> Dict:
#     """
#     Get information about a YouTube video including title, channel, and basic stats.
    
#     Args:
#         video_url: URL of the YouTube video
    
#     Returns:
#         Dictionary containing video information
#     """
#     try:
#         # Extract video ID from URL
#         video_id = None
#         if "youtube.com/watch?v=" in video_url:
#             video_id = video_url.split("watch?v=")[1].split("&")[0]
#         elif "youtu.be/" in video_url:
#             video_id = video_url.split("youtu.be/")[1].split("?")[0]
        
#         if not video_id:
#             return {"error": "Invalid YouTube URL"}
        
#         # Get the video page content
#         response = requests.get(f"https://www.youtube.com/watch?v={video_id}")
#         if response.status_code != 200:
#             return {"error": f"Failed to fetch video (Status code: {response.status_code})"}
        
#         # Parse with BeautifulSoup
#         soup = BeautifulSoup(response.text, 'html.parser')
        
#         # Extract title
#         title = soup.find("meta", property="og:title")
#         title = title["content"] if title else "Unknown title"
        
#         # Extract channel name
#         channel = soup.find("link", itemprop="name")
#         channel = channel["content"] if channel else "Unknown channel"
        
#         # Return video information
#         return {
#             "video_id": video_id,
#             "title": title,
#             "channel": channel,
#             "url": f"https://www.youtube.com/watch?v={video_id}"
#         }
    
#     except Exception as e:
#         return {"error": f"Error retrieving video information: {str(e)}"}

# # YouTube transcript/summary tool
# @mcp.tool()
# def get_youtube_summary(video_url: str, max_length: int = 200) -> Dict:
#     """
#     Get a summary of a YouTube video based on its transcript.
    
#     Args:
#         video_url: URL of the YouTube video
#         max_length: Maximum length of the summary in words
    
#     Returns:
#         Dictionary containing the summary and transcript details
#     """
#     try:
#         # Extract video ID from URL
#         video_id = None
#         if "youtube.com/watch?v=" in video_url:
#             video_id = video_url.split("watch?v=")[1].split("&")[0]
#         elif "youtu.be/" in video_url:
#             video_id = video_url.split("youtu.be/")[1].split("?")[0]
        
#         if not video_id:
#             return {"error": "Invalid YouTube URL"}
        
#         # Get transcript
#         try:
#             transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
#         except Exception as e:
#             return {"error": f"Could not retrieve transcript: {str(e)}"}
        
#         # Combine transcript text
#         full_transcript = " ".join([item['text'] for item in transcript_list])
        
#         # Create a simple summary (first X words)
#         words = full_transcript.split()
#         summary = " ".join(words[:min(max_length, len(words))])
        
#         if len(words) > max_length:
#             summary += "..."
        
#         return {
#             "video_id": video_id,
#             "transcript_length": len(words),
#             "summary": summary,
#             "full_transcript": full_transcript[:5000] + ("..." if len(full_transcript) > 5000 else "")
#         }
    
#     except Exception as e:
#         return {"error": f"Error generating summary: {str(e)}"}

# # Google News fetching tool
# @mcp.tool()
# def get_latest_news(query: Optional[str] = None, num_results: int = 5) -> List[Dict]:
#     """
#     Get the latest news from Google News.
    
#     Args:
#         query: Optional search query to filter news
#         num_results: Maximum number of news results to return
    
#     Returns:
#         List of news articles with title, source, and URL
#     """
#     try:
#         # Base URL
#         url = "https://news.google.com/rss"
#         if query:
#             # Use search query if provided
#             url = f"https://news.google.com/rss/search?q={query}"
        
#         # Make request
#         response = requests.get(url)
#         if response.status_code != 200:
#             return [{"error": f"Failed to fetch news (Status code: {response.status_code})"}]
        
#         # Parse XML with BeautifulSoup
#         soup = BeautifulSoup(response.text, 'xml')
        
#         # Extract news items
#         items = soup.find_all('item', limit=num_results)
        
#         news_list = []
#         for item in items:
#             title = item.title.text if item.title else "No title"
#             source = item.source.text if item.source else "Unknown source"
#             link = item.link.text if item.link else "#"
#             pub_date = item.pubDate.text if item.pubDate else "Unknown date"
            
#             news_list.append({
#                 "title": title,
#                 "source": source,
#                 "link": link,
#                 "published_date": pub_date
#             })
        
#         return news_list
    
#     except Exception as e:
#         return [{"error": f"Error fetching news: {str(e)}"}]

# # Resource endpoint for news
# @mcp.resource("news://{query}")
# def news_resource(query: str = "") -> Dict:
#     """Get news based on a query"""
#     return {"news": get_latest_news(query)}

# # Resource endpoint for YouTube video
# @mcp.resource("youtube://{video_id}")
# def youtube_resource(video_id: str) -> Dict:
#     """Get information about a YouTube video"""
#     video_url = f"https://www.youtube.com/watch?v={video_id}"
#     info = get_youtube_video_info(video_url)
#     summary = get_youtube_summary(video_url)
    
#     return {
#         "info": info,
#         "summary": summary
#     }

# # Start the server if this file is executed directly
# if __name__ == "__main__":
#     # Start the server on default port 8000
#     import uvicorn
#     print("Starting Enhanced MCP Server on http://localhost:8000")
#     uvicorn.run("server:mcp", host="0.0.0.0", port=8000)
from mcp.server.fastmcp import FastMCP
import requests
from typing import Optional

NOTES_API_URL = "http://localhost:3000"
auth_token: Optional[str] = None

mcp = FastMCP("Notes App MCP Server")

@mcp.tool()
def login(email: str, password: str) -> dict:
    """
    Authenticate the user using email and password credentials.

    This tool sends a login request to the server, retrieves a JWT token upon
    successful authentication, and stores it for use in subsequent API calls.

    Args:
        email (str): The user's registered email address.
        password (str): The user's password.

    Returns:
        dict: A dictionary with a success message and the JWT token if login is successful.
    
    Raises:
        Exception: If login succeeds but no token is found in the response.
    """
    global auth_token
    response = requests.post(f"{NOTES_API_URL}/login", json={"email": email, "password": password})
    response.raise_for_status()
    result = response.json()

    auth_token = result.get("accessToken")
    if not auth_token:
        raise Exception("Login succeeded but no token found in response.")
    
    return {"message": "Login successful", "token": auth_token}

def get_auth_headers() -> dict:
    """
    Internal helper to create Authorization headers using the stored JWT token.

    Returns:
        dict: Headers including Bearer token for authorized API calls.

    Raises:
        Exception: If the user has not logged in yet.
    """
    if not auth_token:
        raise Exception("You must login first before using this command.")
    return {"Authorization": f"Bearer {auth_token}"}

@mcp.tool()
def create_note(title: str, content: str) -> dict:
    """
    Create a new note with the specified title and content.

    This tool sends a POST request to the note creation endpoint with the 
    given title and content. It requires the user to be authenticated.

    Args:
        title (str): The title of the note.
        content (str): The body/content of the note.

    Returns:
        dict: A dictionary containing the newly created note's details (e.g., ID, title, content, timestamps).
    """
    headers = get_auth_headers()
    data = {"title": title, "content": content}
    response = requests.post(f"{NOTES_API_URL}/add-note", json=data, headers=headers)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def delete_note(note_id: str) -> dict:
    """
    Delete an existing note by its unique identifier.

    Sends a DELETE request to remove the note permanently from the user's note list.
    Requires authentication.

    Args:
        note_id (str): The ID of the note to be deleted.

    Returns:
        dict: A dictionary confirming the deletion status.
    """
    headers = get_auth_headers()
    response = requests.delete(f"{NOTES_API_URL}/delete-note/{note_id}", headers=headers)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def get_notes() -> list:
    """
    Fetch all notes created by the currently authenticated user.

    Sends a GET request to retrieve a list of all notes for the user.
    Each note includes metadata such as ID, title, content, and timestamps.

    Returns:
        list: A list of dictionaries representing each note.
    """
    headers = get_auth_headers()
    response = requests.get(f"{NOTES_API_URL}/get-notes", headers=headers)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def get_user() -> dict:
    """
    Retrieve the profile information of the currently authenticated user.

    Sends a GET request to the user endpoint. Requires the user to be logged in.

    Returns:
        dict: A dictionary containing user information (e.g., ID, email, creation date).
    """
    headers = get_auth_headers()
    response = requests.get(f"{NOTES_API_URL}/get-user", headers=headers)
    response.raise_for_status()
    return response.json()

# Start server
if __name__ == "__main__":
    import uvicorn
    print("Starting Enhanced MCP Server on http://localhost:8000")
    uvicorn.run("server:mcp", host="0.0.0.0", port=8000)
