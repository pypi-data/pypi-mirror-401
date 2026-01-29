"""
Telegram Notifier for sending notifications
"""

from typing import Optional
import requests
import logging

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """
    Telegram bot notifier for sending messages.
    
    Example:
        >>> notifier = TelegramNotifier(
        ...     bot_token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
        ...     chat_id="123456789"
        ... )
        >>> notifier.send("Training completed!")
    """
    
    def __init__(
        self,
        bot_token: str,
        chat_id: str,
    ):
        """
        Initialize Telegram notifier.
        
        Args:
            bot_token: Telegram bot token
            chat_id: Chat ID to send messages to
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
    
    def send(
        self,
        message: str,
        parse_mode: Optional[str] = None,
    ) -> bool:
        """
        Send message to Telegram.
        
        Args:
            message: Message text
            parse_mode: Parse mode (HTML, Markdown, MarkdownV2)
            
        Returns:
            True if successful, False otherwise
        """
        url = f"{self.api_url}/sendMessage"
        data = {
            "chat_id": self.chat_id,
            "text": message,
        }
        if parse_mode:
            data["parse_mode"] = parse_mode
        
        try:
            response = requests.post(url, json=data, timeout=10)
            response.raise_for_status()
            logger.info(f"Sent Telegram message to {self.chat_id}")
            return True
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
            return False
    
    def send_file(
        self,
        file_path: str,
        caption: Optional[str] = None,
    ) -> bool:
        """
        Send file to Telegram.
        
        Args:
            file_path: Path to file
            caption: Optional caption
            
        Returns:
            True if successful, False otherwise
        """
        url = f"{self.api_url}/sendDocument"
        
        try:
            with open(file_path, "rb") as f:
                files = {"document": f}
                data = {"chat_id": self.chat_id}
                if caption:
                    data["caption"] = caption
                
                response = requests.post(url, files=files, data=data, timeout=30)
                response.raise_for_status()
                logger.info(f"Sent file to Telegram: {file_path}")
                return True
        except Exception as e:
            logger.error(f"Error sending file to Telegram: {e}")
            return False
    
    def send_photo(
        self,
        photo_path: str,
        caption: Optional[str] = None,
    ) -> bool:
        """
        Send photo to Telegram.
        
        Args:
            photo_path: Path to photo
            caption: Optional caption
            
        Returns:
            True if successful, False otherwise
        """
        url = f"{self.api_url}/sendPhoto"
        
        try:
            with open(photo_path, "rb") as f:
                files = {"photo": f}
                data = {"chat_id": self.chat_id}
                if caption:
                    data["caption"] = caption
                
                response = requests.post(url, files=files, data=data, timeout=30)
                response.raise_for_status()
                logger.info(f"Sent photo to Telegram: {photo_path}")
                return True
        except Exception as e:
            logger.error(f"Error sending photo to Telegram: {e}")
            return False
