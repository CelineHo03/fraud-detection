import redis
from redis.commands.json.path import Path 
import uuid
from datetime import datetime
from typing import Dict, Any, Optional 
from app.config import settings

class RedisClient:
    def __init__(self):
        self.client = redis.Redis(
            host = settings.redis_host,
            port = settings.redis_port,
            db = settings.redis_db,
            decode_responses = True
        )
        self._ensure_streams()
    
    def _ensure_streams(self):
        """Create consumer groups """
        try:
            self.client.xgroup_create(
                name= settings.ingest_stream,
                groupname = settings.ingest_group,
                id ='0',
                mkstream = True
            )
        except redis.exceptions.ResponseError as e:
            if 'BUSYGROUP' not in str(e):
                raise
    
    def ping(self) -> bool:
        """Test Redis connection"""
        return self.client.ping()
    
    def json_set(self, key: str, data: Dict[str, Any]) -> bool:
        """Store JSON document"""
        return self.client.json().set(key, Path.root_path(), data)
    
    def json_get(self, key:str) -> Optional[Dict[str, Any]]:
        """Retrieve JSON document"""
        return self.client.json().get(key)
    
    def stream_add(self, stream_name: str, data: Dict[str, Any]) -> str:
        """Add message to stream"""
        return self.client.xadd(stream_name, data)
    
    def generate_id(self) -> str:
        """Generate unique application ID"""
        return str(uuid.uuid4())
    
    def get_timestamp(self) -> str:
        """Get ISO timestamp"""
        return datetime.utcnow().isoformat()

    def add_to_ingest_stream(self, application_id: str, 
                            submission_type: str,
                            content: str) -> str:
        """
        Add a new submission to the ingest stream
        
        Args:
            application_id: Unique ID for this submission
            submission_type: 'text' or 'screenshot'
            content: The message text or file path
        
        Returns:
            Stream message ID
        """
        data = {
            "application_id": application_id,
            "type": submission_type,
            "content": content,
            "timestamp": self.get_timestamp()
        }
        
        return self.stream_add(settings.ingest_stream, data)
    
    def create_application(self, 
                          submission_type: str,
                          content: str,
                          metadata: Optional[Dict] = None) -> str:
        """
        Create a new fraud detection application
        
        Args:
            submission_type: 'text' or 'screenshot'
            content: The message text or file path
            metadata: Optional extra info (source, phone number, etc.)
        
        Returns:
            application_id
        """
        # Generate unique ID
        app_id = self.generate_id()
        
        # Create application document
        application = {
            "id": app_id,
            "type": submission_type,
            "content": content,
            "metadata": metadata or {},
            "status": "submitted",
            "created_at": self.get_timestamp(),
            "updated_at": self.get_timestamp(),
            "agents": {
                "doc_auth": {
                    "status": "pending",
                    "score": None,
                    "details": {}
                },
                "text_similarity": {
                    "status": "pending", 
                    "score": None,
                    "matches": []
                }
            },
            "final_score": None,
            "fraud_likelihood": None
        }
        
        # Store in RedisJSON
        key = f"application:{app_id}"
        self.json_set(key, application)
        
        # Add to ingest stream for processing
        self.add_to_ingest_stream(app_id, submission_type, content)
        
        return app_id

redis_client = RedisClient()