import os
from dotenv import load_dotenv
from tools.search import search
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

class SimpleReActAgent:
    def __init__(self):
       
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("La variable de entorno no está definida")

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            api_key=api_key
        )

    def run(self, question: str) -> str:
        
        observation = search(question)

     
        prompt = f"""
        Usa esta información para responder claramente a la pregunta:
        {observation}

        Pregunta: {question}

        Responde solo la respuesta final, sin explicaciones.
        """
        response = self.llm.invoke(prompt)

       
        print("Respuesta:", response.content)
        return response.content