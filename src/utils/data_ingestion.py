import json
import requests
import hashlib
import time
from datetime import datetime

class AxiomHiveDataIngestor:
    """
    Functional data ingestion module for AxiomHive.
    Handles secure data acquisition, hashing for integrity, and metadata enrichment.
    """

    def __init__(self, endpoint_url=None):
        self.endpoint_url = endpoint_url
        self.session = requests.Session()

    def fetch_from_api(self, api_url, headers=None):
        """Fetches data from an external API with error handling."""
        try:
            response = self.session.get(api_url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def process_payload(self, raw_data):
        """Enriches raw data with metadata and integrity hashes."""
        payload_str = json.dumps(raw_data, sort_keys=True)
        integrity_hash = hashlib.sha256(payload_str.encode()).hexdigest()
        
        enriched_data = {
            "metadata": {
                "timestamp": datetime.utcnow().isoformat(),
                "integrity_hash": integrity_hash,
                "source": "external_api",
                "version": "1.0.0"
            },
            "payload": raw_data
        }
        return enriched_data

    def save_locally(self, data, filename=None):
        """Saves the enriched payload to a local JSON file."""
        if not filename:
            timestamp = int(time.time())
            filename = f"ingested_data_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to: {filename}")
        return filename

if __name__ == "__main__":
    # Example usage:
    # ingestor = AxiomHiveDataIngestor()
    # raw = {"threat_level": "low", "sector": "A1"}
    # enriched = ingestor.process_payload(raw)
    # ingestor.save_locally(enriched)
    pass
