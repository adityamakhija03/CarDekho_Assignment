import ollama
from pydantic_ai.models import Model

class CSVQueryModel(Model):
    """AI model processes natural language queries about CSV data."""
    question: str

class ModelHandler:
    def __init__(self, model_name="llama3:8b"):
        self.model_name = model_name
    
    def process_query(self, question, data_json):
        """Process a natural language query about the CSV data"""
        try:
            if not data_json:
                return "⚠️ Please upload a CSV file first."
            
            
            prompt = f"""
            You are an expert CSV data analyst with extensive knowledge of statistics, data science, and business intelligence. Your task is to analyze a CSV dataset and provide insightful, accurate answers to user questions.

            Given this CSV sample: {data_json}

            Answer the following question thoroughly but concisely: {question}

            Follow these guidelines:
            1. First examine the data structure (column types, value ranges, missing values)
            2. When relevant, provide statistical insights (averages, distributions, outliers)
            3. Identify relationships between variables when appropriate
            4. Format numerical answers precisely (round to 2 decimal places)
            5. If the question is ambiguous, interpret it in the most useful way
            6. If the data is insufficient to answer completely, clearly state what's missing
            7. Prioritize accuracy over speculation
            8. Use business-relevant terminology based on the data domain
            9. Present actionable insights whenever possible
            10. Avoid unnecessary technical jargon unless specifically requested

            Remember that your analysis will inform important business decisions, so be thorough, accurate, and practical in your response.
            """
            
            # Query the Llama model
            response = ollama.chat(model=self.model_name, messages=[
                {"role": "user", "content": prompt}
            ])
            
            return response["message"]["content"]
        
        except Exception as e:
            return f"❌ Error processing query: {str(e)}"