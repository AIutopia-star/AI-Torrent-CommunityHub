from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class User:
    id: int
    username: str
    email: str
    password_hash: str
    created_at: datetime
    is_admin: bool = False

@dataclass
class AIModel:
    id: int
    name: str
    description: str
    version: str
    license: str
    upload_date: datetime
    update_date: datetime
    download_count: int
    view_count: int
    user_id: int
    username: str
    torrent_file: str
    magnet_link: Optional[str]
    model_img: str
    file_size: int
    tags: List[str] = None

@dataclass
class ModelImage:
    id: int
    filename: str
    model_id: int
    is_primary: bool = False