import os
import tempfile
import logging
import yt_dlp
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

def is_social_video_url(url: str) -> bool:
    """Checks if the URL is likely a social media video platform."""
    social_domains = ['instagram.com', 'youtube.com', 'youtu.be', 'tiktok.com', 'twitter.com', 'x.com', 'facebook.com']
    url_lower = url.lower()
    return any(domain in url_lower for domain in social_domains)

def download_social_video(url: str) -> Tuple[Optional[bytes], str, str]:
    """
    Downloads a video from a social URL.
    Returns (video_bytes, text_metadata, mime_type)
    """
    try:
        # Create a temporary directory to store the downloaded file
        with tempfile.TemporaryDirectory() as temp_dir:
            outtmpl = os.path.join(temp_dir, 'video.%(ext)s')
            
            ydl_opts = {
                'format': 'best[ext=mp4]/best', # Prefer mp4 for Gemini
                'outtmpl': outtmpl,
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                # Try to skip downloading playlists if a user accidentally links one
                'noplaylist': True,
                'max_filesize': 50 * 1024 * 1024 # Limit to 50MB to protect backend
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                
                title = info_dict.get('title', '')
                description = info_dict.get('description', '')
                text_metadata = f"Title: {title}\nDescription: {description}"
                
                ext = info_dict.get('ext', 'mp4')
                mime_type = f"video/{ext}"
                if ext not in ['mp4', 'webm', 'mov']:
                    mime_type = "video/mp4" # fallback
                    
                filename = ydl.prepare_filename(info_dict)
                
                if not os.path.exists(filename):
                    # Sometimes the extension is slightly different
                    filename = os.path.join(temp_dir, f"video.{ext}")
                    
                with open(filename, 'rb') as f:
                    video_bytes = f.read()
                    
                return video_bytes, text_metadata, mime_type
                
    except Exception as e:
        logger.error(f"Failed to download video from {url}: {e}")
        return None, "", ""
