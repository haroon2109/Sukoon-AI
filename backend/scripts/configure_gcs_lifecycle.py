import os
import sys
from google.cloud import storage

def enable_privacy_lifecycle(bucket_name: str):
    """
    Configures a Google Cloud Storage bucket with an aggressive 
    Object Lifecycle Rule to automatically delete all media 
    files exactly 1 day after upload.
    
    This acts as an automated garbage collector, ensuring strict
    user privacy and optimal cloud resource usage.
    """
    print(f"Connecting to Google Cloud to configure lifecycle rules for bucket: {bucket_name}...")
    
    try:
        # Initialize the Google Cloud Storage client
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)

        # Clear existing rules to avoid conflicts
        bucket.clear_lifecyle_rules()

        # Define the new privacy-first lifecycle rule
        # Action: Delete the object
        # Condition: Age is 1 day (24 hours)
        bucket.add_lifecycle_delete_rule(age=1)

        # Apply the changes to the live bucket
        bucket.patch()
        
        print("\n✅ SUCCESS: Automated Garbage Collection Enforced!")
        print(f"-> All user media uploaded to '{bucket_name}' will now self-destruct exactly 24 hours after verification.")
        print("-> Your cloud costs are optimized and user privacy is guaranteed.")
        
    except Exception as e:
        print(f"\n❌ ERROR: Failed to configure bucket lifecycle. Details:\n{str(e)}")
        print("\nMake sure your GOOGLE_APPLICATION_CREDENTIALS environment variable is set properly.")
        sys.exit(1)

if __name__ == "__main__":
    # Allow passing bucket name via command line arg or environment variable
    target_bucket = os.environ.get("GCS_BUCKET_NAME")
    
    if len(sys.argv) > 1:
        target_bucket = sys.argv[1]
        
    if not target_bucket:
        print("Usage: python configure_gcs_lifecycle.py [BUCKET_NAME]")
        print("Or set the GCS_BUCKET_NAME environment variable.")
        sys.exit(1)
        
    enable_privacy_lifecycle(target_bucket)
