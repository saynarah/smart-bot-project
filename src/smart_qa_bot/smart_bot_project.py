from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import (   ChatPromptTemplate)
from langchain_core.output_parsers import ( StrOutputParser,  PydanticOutputParser)
from langchain.chat_models import init_chat_model
from langchain_core.messages import (
    HumanMessage, 
    SystemMessage, 
    AIMessage, 
    ChatMessage, 
    ToolMessage)

from pydantic import BaseModel, Field
from typing import List, Optional
from langsmith import traceable, Client, tracing_context
from langsmith.run_helpers import get_current_run_tree, get_tracing_context

load_dotenv()

if os.getenv("LANGSMITH_API_KEY"):
    os.environ["LANGSMITH_TRACING"] = "True"
    os.environ.setdefault(
        "LANGSMITH_PROJECT", "Smart Q&A Bot Project") ## Replace by your project's name on LangSmith
    ## print(f"Langsmith is configured. - Project: {os.getenv('LANGSMITH_PROJECT')}")

langsmith_client = Client()

class QAResponse(BaseModel):
    answer: str = Field(description="The answer provided by the model")
    confidence: str = Field(description="Confidence level of the answer, e.g., 'high', 'medium', 'low'")
    reasoning: str = Field(description="Reasoning behind the answer")
    follow_up_questions: List[str] = Field(
        default_factory=list, 
        description="List of follow-up questions for further clarification")
    sources_needed: bool = Field(
        default=False, 
        description="Indicates if sources are needed for the answer"
    )

class SmartQABot:
    def __init__(
        self, 
        model_name: str = "gpt-4o-mini",
        temperature: float = 0.3
    ):
        self.llm = init_chat_model(
            model=model_name, 
            temperature=temperature
            ).with_structured_output(QAResponse)
        self.parser = PydanticOutputParser(pydantic_object=QAResponse)
        # Prompt Template
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a knowledgeable Q&A assistant for fitness exercises.

                    Your guidelines:
                    - Answer questions accurately and concisely.
                    - Keep your answer up to 3 bullet points with a 2-3 lines each.
                    - Do not use "**" to bold parts of the text. Avoid the bold.
                    - Be honest about uncertainty - set confidence to 'low' if unsure.
                    - Provide clear explanations supporting your answers.
                    - Suggest relevant follow-up questions.
                    - Indicate if external sources would help.
                    - Your scope is Fitness, Wellness, Exercises and Sports.
                    - Don't answer questions outside your scope.

                    Always respond with accurate, helpful information."""
                ),
                (
                    "human",
                    "{question}"
                )
            ]
        )

        self.chain = self.prompt | self.llm

    @traceable(
        name="ask_question", 
        run_type="chain", 
        project_name="Smart Q&A Bot Project", ## Replace by your project's name on LangSmith
        client=langsmith_client)
    def ask(self, question: str) -> QAResponse:
        try:
            response = self.chain.invoke({"question": question})
            return response
        except Exception as e:
            return QAResponse(
                    answer = "I'm sorry, I couldn't process your question at this time.",
                    confidence = "low",
                    reasoning = str(e),
                    follow_up_questions = ["Could you try again later or rephrase your question?"],
                    sources_needed = True,
                        )
    
    @traceable(
        name="ask_batch", 
        run_type="chain", 
        project_name="Smart Q&A Bot Project", ## Replace by your project's name on LangSmith
        client=langsmith_client)
    def ask_batch(self, questions: List[str]) -> List[QAResponse]:
        inputs = [{"question": q} for q in questions]
        return self.chain.batch(inputs)


def demo_qa_bot():
    bot = SmartQABot()
    questions = [
        "What are the benefits of cardio exercises? ",
        "How can I improve flexibility?",
        "How can I boost my stamina?"
    ]

    print("-" * 50)
    print("SMART Q&A (FITNESS & WELLNESS) BOT")
    print("-" * 50)

    for question in questions:
        response = bot.ask(question)
        print(f"Question: {question}")
        print(f"Answer: {response.answer}")
        print(f"Confidence: {response.confidence}")
        print(f"Reasoning: {response.reasoning}")
        print(f"Follow-up Questions: {response.follow_up_questions}")
        print(f"Sources Needed: {response.sources_needed}")
        print("-" * 50)

@traceable(
        name="demo_error_handling", 
        run_type="chain", 
        project_name="Smart Q&A Bot Project", ## Replace by your project's name on LangSmith
        client=langsmith_client)
def demo_error_handling():

    bot = SmartQABot()

    print("\n" + "=" * 60)
    print("ERROR HANDLING DEMO")
    print("=" * 60)

    long_question = "What is " + "very " * 100 + "important?"

    response = bot.ask(long_question)
    print(f"Handled gracefully: {response.confidence}")

@traceable(
        name="demo_batch_processing", 
        run_type="chain", 
        project_name="Smart Q&A Bot Project", 
        client=langsmith_client)
def demo_batch_processing():

    bot = SmartQABot()

    questions = [
        "How can I build muscle?",
        "How does sleep affect recovery?",
        "How can I prevent sports injuries?"
]

    print("\n" + "=" * 60)
    print("BATCH PROCESSING DEMO")
    print("=" * 60)

    response = bot.ask_batch(questions)
    
    for q, r in zip(questions, response):
        print(f"\n{q}")
        print(f" -> {r.answer[:100]}...")
        print(f" Confidence: {r.confidence}")


if __name__ == "__main__":

    with tracing_context(
        enabled=True, 
        project_name="Smart Q&A Bot Project", 
        client=langsmith_client):

        try:
            demo_qa_bot()
            demo_error_handling()
            demo_batch_processing()

        finally:
            langsmith_client.flush()
 