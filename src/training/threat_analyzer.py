import os
import json
from openai import OpenAI

class AxiomHiveThreatAnalyzer:
    """
    Functional threat analysis module for AxiomHive.
    Utilizes LLMs to analyze intelligence data and provide strategic insights.
    """

    def __init__(self):
        # Utilizes pre-configured environment variables for OpenAI
        self.client = OpenAI()
        self.system_prompt = (
            "You are the AxiomHive Strategic AI. Your core directive is the Non-Harm Principle. "
            "Analyze intelligence data for threats, identifying internal inconsistencies and "
            "potential fabrication. Provide reasoning paths and confidence scores."
        )

    def analyze_intelligence(self, data):
        """Analyzes raw intelligence data using LLM."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Analyze this intelligence payload: {json.dumps(data)}"}
                ],
                temperature=0.2
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error during AI analysis: {e}")
            return None

    def generate_defense_brief(self, analysis_result):
        """Generates a structured defense brief based on analysis."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Generate a professional legal defense brief based on the provided threat analysis."},
                    {"role": "user", "content": analysis_result}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating defense brief: {e}")
            return None

if __name__ == "__main__":
    # Example usage:
    # analyzer = AxiomHiveThreatAnalyzer()
    # report = analyzer.analyze_intelligence({"report": "Suspicious activity in sector 7G"})
    # print(report)
    pass
