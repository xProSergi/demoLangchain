import os
from dotenv import load_dotenv
from tools.search import search
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

class SimpleReActAgent:
    def __init__(self):
       
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Environment variable is not defined")

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            api_key=api_key
        )

    def run(self, question: str) -> str:
        
        observation = search(question)

     
        prompt = f"""
        Use the following information to answer the question clearly:
        {observation}

        Question: {question}

        Provide only the final answer, without explanations.
        """
        response = self.llm.invoke(prompt)

       
        print("Answer:", response.content)
        return response.content