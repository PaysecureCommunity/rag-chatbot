import os
import streamlit as st
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.firecrawl import FirecrawlTools  # 🔥 Firecrawl for scraping

load_dotenv()

DOCS_URL = "https://developer.paysecure.net/"

class PaysecureAgent:
    """AI Agent for Paysecure, using Firecrawl to scrape and retrieve documentation."""
    
    def __init__(self, firecrawl_api_key: str, gemini_api_key: str, model_id: str = "gemini-1.5-flash"):
        self.agent = Agent(
            model=Gemini(id=model_id, api_key=gemini_api_key),
            tools=[FirecrawlTools(scrape=True)],  # 🔥 Firecrawl tool for scraping docs
            instructions=[
                "You are an AI assistant for Paysecure, a payment processing company.",
                f"Scrape and search for API and integration answers from {DOCS_URL} using Firecrawl.",
                "Provide clear, concise, and accurate answers based on Paysecure's developer documentation."
            ],
            markdown=True,
            show_tool_calls=True,
            description="I am the Paysecure AI assistant, helping employees and merchants with queries about PaySecure's products and documentation."
        )
    
    def respond(self, query: str) -> str:
        """Scrape and generate a response using Firecrawl for retrieving relevant documentation."""
        response = self.agent.run(f"""User Query: {query}
        
        Scrape {DOCS_URL} and provide a clear, concise answer using Firecrawl.""")
        
        return response.content if response else "I'm unable to retrieve an answer at the moment."

def main():
    st.set_page_config(page_title="Paysecure AI Assistant", page_icon="💳", layout="wide")

    firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    if not firecrawl_api_key or not gemini_api_key:
        st.error("⚠️ Missing API keys. Please set FIRECRAWL_API_KEY and GEMINI_API_KEY as environment variables.")
        return
    
    model_id = "gemini-1.5-flash"  # Default model
    st.session_state.agent = PaysecureAgent(firecrawl_api_key, gemini_api_key, model_id)

    st.title("💳 PaySecure AI Assistant")
    st.write("Ask me anything about PaySecure's products and documentation!")

    query = st.text_area("Enter your query:", "How do I integrate PaySecure into my e-commerce website?")

    if st.button("Ask AI"):
        with st.spinner("Fetching response..."):
            response = st.session_state.agent.respond(query)
            st.markdown(response)

if __name__ == "__main__":
    main()
