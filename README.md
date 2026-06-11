 🧠 Learning Path Generator

An AI-powered web application that generates structured learning roadmaps for any skill or domain. Built using LangChain, Groq LLM, Streamlit, Pydantic, and Langfuse, the application helps learners discover the right learning sequence, key topics, and goals without manually creating a study plan.

## 🚀 Key Features

- Generate AI-powered learning roadmaps
- Structured learning stages from beginner to advanced level
- Key topic recommendations for any skill
- Learning goal summary generation
- Pydantic-based output validation
- Multiple chat session support
- Langfuse integration for monitoring and tracing
- Interactive Streamlit user interface

## 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- Groq (Llama 3.1 8B Instant)
- Pydantic
- Langfuse
- Python-dotenv

## 📖 Project Summary

Many learners struggle to identify the correct learning path when starting a new skill due to the abundance of online resources. This project solves that problem by automatically generating a structured roadmap using AI.

The user enters a skill or domain, and the system:
1. Creates a structured prompt using LangChain.
2. Sends the prompt to the Groq LLM.
3. Generates learning stages, key topics, and a learning goal summary.
4. Validates the response using Pydantic.
5. Displays the roadmap through a Streamlit interface.
6. Tracks execution using Langfuse.

## 🎯 Outcome

The Learning Path Generator helps students and professionals save time, follow a logical learning sequence, and achieve their learning goals more efficiently through AI-generated roadmaps.
