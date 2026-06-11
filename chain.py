import os
from dotenv import load_dotenv
from typing import List

from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

# Langfuse v3 uses langfuse.langchain.CallbackHandler (no constructor args needed)
# Keys are read automatically from LANGFUSE_SECRET_KEY, LANGFUSE_PUBLIC_KEY, LANGFUSE_BASE_URL in .env
try:
    from langfuse.langchain import CallbackHandler as LangfuseCallbackHandler
    LANGFUSE_V3 = True
except ImportError:
    # Fallback for older langfuse versions
    from langfuse.callback import CallbackHandler as LangfuseCallbackHandler
    LANGFUSE_V3 = False


# ---------- Pydantic Model ----------
class LearningPath(BaseModel):
    learning_stages: List[str] = Field(description="Ordered list of learning stages")
    key_topics: List[str] = Field(description="Key topics to cover for the skill")
    learning_goal_summary: str = Field(description="A concise summary of the overall learning goal")


# ---------- LangChain Chain ----------
def build_chain():
    # 1. Output parser
    parser = PydanticOutputParser(pydantic_object=LearningPath)

    # 2. Prompt template
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a Learning Path Generator. You generate structured learning roadmaps.\n"
            "Return valid JSON only — no explanations, no markdown, no extra text.\n\n"
            "{format_instructions}"
        ),
        (
            "human",
            "Generate a structured learning roadmap for the following skill.\n"
            "Rules:\n"
            "- Do not assume prior knowledge\n"
            "- Create logical learning stages\n"
            "- Topics must be relevant to the skill\n\n"
            "Skill: {skill}"
        )
    ]).partial(format_instructions=parser.get_format_instructions())

    # 3. Groq LLM via LangChain
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.3,
        api_key=os.getenv("GROQ_API_KEY")
    )

    # 4. Chain: prompt | llm | parser
    chain = prompt | llm | parser

    return chain


# ---------- Public API ----------
_chain = None

def run_chain(skill: str) -> LearningPath:
    """
    Full LangChain chain: skill → prompt → ChatGroq → PydanticOutputParser → LearningPath.
    Traces the run to Langfuse automatically using .env credentials.
    """
    global _chain
    if _chain is None:
        _chain = build_chain()

    if LANGFUSE_V3:
        # Langfuse v3: CallbackHandler() takes no args — reads from .env automatically
        langfuse_handler = LangfuseCallbackHandler()
    else:
        # Langfuse v2: pass keys explicitly
        langfuse_handler = LangfuseCallbackHandler(
            secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            host=os.getenv("LANGFUSE_BASE_URL"),
            session_id="learning-path-generator",
            user_id="streamlit-user",
            trace_name=f"learning-path:{skill}",
            tags=["learning-path", "groq", "llama-3.1"],
            metadata={"skill": skill},
        )

    return _chain.invoke(
        {"skill": skill},
        config={"callbacks": [langfuse_handler]}
    )