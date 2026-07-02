import os
import sys

# Ensure the backend directory is in the path to import app modules
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.services.qdrant_service import qdrant_service
from app.ai_modules.vertex_embeddings import vertex_embeddings

MOCK_DOCUMENTS = [
    {
        "payload": {
            "title": "WHO Advisory: Masks and Transmission",
            "text": "The World Health Organization (WHO) advises that masks are a key measure to suppress transmission and save lives. Misinformation regarding masks causing hypoxia is unfounded.",
            "source": "WHO.int",
            "category": "WHO advisories",
            "date": "2023-01-15"
        }
    },
    {
        "payload": {
            "title": "Gov Notification: Election Integrity",
            "text": "Official government notification: Electronic Voting Machines (EVMs) are standalone devices without networking capabilities. Claims of remote hacking via Wi-Fi are technically impossible.",
            "source": "Election Commission",
            "category": "Government notifications",
            "date": "2024-03-10"
        }
    },
    {
        "payload": {
            "title": "Fact-Check: Viral Video of Protest",
            "text": "The viral video claiming to show a recent violent protest in the capital is actually from a 2018 movie set in Europe. The claim is completely fabricated.",
            "source": "AltNews",
            "category": "Fact-check articles",
            "date": "2024-05-20"
        }
    },
    {
        "payload": {
            "title": "News Archive: Economic Policy Change",
            "text": "In 2016, the government introduced the demonetization policy to curb black money. Claims that the policy was reversed in 2024 are false.",
            "source": "Reuters Archive",
            "category": "News archives",
            "date": "2016-11-08"
        }
    }
]

def seed_database():
    print("Initializing embedding model...")
    # Generate vectors for each document
    docs_to_insert = []
    
    for doc in MOCK_DOCUMENTS:
        text_to_embed = f"{doc['payload']['title']}. {doc['payload']['text']}"
        print(f"Embedding: {doc['payload']['title']}")
        vector = vertex_embeddings.get_embedding(text_to_embed)
        if vector:
            doc["vector"] = vector
            docs_to_insert.append(doc)
            
    print(f"Generated {len(docs_to_insert)} vectors.")
    print("Inserting into Qdrant...")
    
    success = qdrant_service.insert_documents(docs_to_insert)
    if success:
        print("Successfully seeded Qdrant database.")
    else:
        print("Failed to seed Qdrant database.")

if __name__ == "__main__":
    seed_database()
