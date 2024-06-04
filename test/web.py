import os
from dotenv import load_dotenv
from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchRun
from langchain.memory import ConversationBufferMemory
from langchain.agents import ConversationalChatAgent, AgentExecutor
from langchain_community.callbacks.manager import get_openai_callback
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent,create_react_agent, create_openai_functions_agent
from langchain.prompts import PromptTemplate
from langchain.agents.agent_types import AgentType
from langchain.chains import LLMMathChain, LLMChain
from langchain.chains import LLMMathChain
from langchain_community.llms import OpenAI



load_dotenv()

def create_chatbot(question):
   
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    chat_template = """
    Your job is to give answer to the {user_input} youu are getting.you are a knwoledge source .
    Use web search if required after anlaysing the {user_input}. Be as detailed as possible, but don't make up any information that's not correct.dont halucinate.be specific.

   """
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True,output_key="output",prompt_template=chat_template)
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, streaming=False)
    tools = [DuckDuckGoSearchRun(name="Search")]
    chat_agent = ConversationalChatAgent.from_llm_and_tools(llm=llm, tools=tools)
    
    executor = AgentExecutor.from_agent_and_tools(
        agent=chat_agent,
        tools=tools,
        memory=memory,
        return_intermediate_steps=False,
        handle_parsing_errors=True,
    )
    
    with get_openai_callback() as cb:
        response = executor.invoke(question)
        total_tokens = cb.total_tokens
        print(f"Total cost: {(total_tokens/1000)*.002}")
   
    
    return response





# def logical(question):
#     
#     llm = ChatOpenAI(model_name="gpt-4o", openai_api_key=openai_api_key, streaming=False)

#     word_problem_template = """You are a reasoning agent tasked with solving the user's logic-based questions.
#     Logically arrive at the solution, and be factual. In your answers, clearly detail the steps involved and give
#     the final answer. Provide the response in bullet points. Question  {question} Answer"""
    
#     math_assistant_prompt = PromptTemplate(
#         input_variables=["question"],
#         template=word_problem_template
#     )

#     word_problem_chain = LLMChain(llm=llm, prompt=math_assistant_prompt)
#     word_problem_tool = Tool.from_function(name="Reasoning Tool", func=word_problem_chain.run,
#                                            description="Useful for when you need to answer logic-based/reasoning questions.")

#     problem_chain = LLMChain(llm=llm, prompt=math_assistant_prompt)
#     math_tool = Tool.from_function(name="Calculator", func=problem_chain.run,
#                                    description="Useful for when you need to answer numeric questions. This tool is only for math questions and nothing else. Only input math expressions, without text")

#     agent = create_openai_functions_agent(
#         tools=[math_tool, word_problem_tool],
#         llm=llm,
#         prompt=math_assistant_prompt
#     )
#     result = agent.run(question)
#     return result




# extracted_text = "There were 10 friends playing a video game online when 7 players quit. If each player left had 8 lives, how many lives did they have total?"
# response = logical(extracted_text)


