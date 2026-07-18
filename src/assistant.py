import os
import json
import glob
from openai import OpenAI
from src.training.threat_analyzer import AxiomHiveThreatAnalyzer
from src.utils.data_ingestion import AxiomHiveDataIngestor
from src.utils.image_processor import AxiomHiveImageProcessor

class AxiomHiveAssistant:
    """
    The central AI Assistant for the AxiomHive repository.
    Integrates documentation RAG and functional system modules.
    """

    def __init__(self):
        self.client = OpenAI()
        self.threat_analyzer = AxiomHiveThreatAnalyzer()
        self.ingestor = AxiomHiveDataIngestor()
        self.docs_path = "docs/**/*.md"
        self.system_prompt = (
            "You are the AxiomHive AI Assistant. Your mission is to support strategic command, "
            "intelligence analysis, and operational tasks with absolute professional integrity. "
            "You operate under the Non-Harm Principle. You have access to the full repository "
            "documentation and functional modules for threat analysis, data ingestion, and image processing."
        )

    def _get_context_from_docs(self, query):
        """Simple RAG implementation: find relevant documentation content."""
        doc_files = glob.glob(self.docs_path, recursive=True)
        context = ""
        for doc_file in doc_files:
            with open(doc_file, 'r') as f:
                content = f.read()
                # Simple keyword matching for relevance (can be expanded to vector search)
                if any(word.lower() in content.lower() for word in query.split()):
                    context += f"\n--- Source: {doc_file} ---\n{content[:1000]}..." # Truncated for context window
        return context

    def chat(self, user_input):
        """Main interaction loop for the assistant."""
        context = self._get_context_from_docs(user_input)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "system", "content": f"Context from repository documentation:\n{context}"},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

    def analyze_threat(self, payload):
        """Delegates to the functional threat analyzer."""
        return self.threat_analyzer.analyze_intelligence(payload)

    def ingest_data(self, raw_data):
        """Delegates to the functional data ingestor."""
        return self.ingestor.process_payload(raw_data)

    def process_image(self, source, output, brand_text="AXIOMHIVE"):
        """Delegates to the functional image processor."""
        processor = AxiomHiveImageProcessor(source)
        processor.apply_editorial_grade().add_branding(brand_text).save(output)
        return f"Image processed and saved to {output}"

if __name__ == "__main__":
    # Example usage:
    # assistant = AxiomHiveAssistant()
    # print(assistant.chat("Explain the Non-Harm Principle in AxiomHive."))
    pass
