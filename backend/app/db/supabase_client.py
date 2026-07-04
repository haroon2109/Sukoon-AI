import os
import logging
from supabase import create_client, Client

logger = logging.getLogger(__name__)

# Fetch Supabase configuration from environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

def init_supabase() -> Client:
    """Initialize the Supabase client with error handling."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        logger.warning(
            "SUPABASE_URL or SUPABASE_KEY is missing from environment variables. "
            "Database operations like vector search will fail."
        )
        
        # Return a dummy client that raises an error when used
        class DummyClient:
            def rpc(self, *args, **kwargs):
                raise ValueError("Cannot perform database operations without valid Supabase credentials.")
            
            def table(self, *args, **kwargs):
                raise ValueError("Cannot perform database operations without valid Supabase credentials.")
                
        return DummyClient()
        
    try:
        client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("Successfully initialized actual Supabase Client.")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {str(e)}")
        raise e

# Export the singleton client instance
supabase_client = init_supabase()
