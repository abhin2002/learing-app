from dotenv import load_dotenv
import os
from openai import OpenAI
import time
from typing_extensions import override
from openai import AssistantEventHandler
from langchain_community.callbacks.manager import get_openai_callback
 
# First, we create a EventHandler class to define
# how we want to handle the events in the response stream.
 
class EventHandler(AssistantEventHandler):    
  @override
  def on_text_created(self, text) -> None:
    print(f"", end="", flush=True)
      
  @override
  def on_text_delta(self, delta, snapshot):
    print(delta.value, end="", flush=True)
      
  def on_tool_call_created(self, tool_call):
    print(f"\n> your friend", flush=True)
  
  def on_tool_call_delta(self, delta, snapshot):
    if delta.type == 'code_interpreter':
      if delta.code_interpreter.input:
        print(delta.code_interpreter.input, end="", flush=True)
      if delta.code_interpreter.outputs:
        print(f"", flush=True)
        for output in delta.code_interpreter.outputs:
          if output.type == "logs":
            print(f"\n{output.logs}", flush=True)

def get_assistant_response(mat):
    load_dotenv()

    # Initialize OpenAI client
    
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    client = OpenAI(api_key=openai_api_key)

    # Create an assistant
    assistant = client.beta.assistants.create(
        name="Tutor",
        instructions="You are a personal tutor. Write and run code to answer math and logical questions. Break down the questions and answer them step by step, explaining each step. Questions can be both logical and mathematical.",
        tools=[
            {
                "type": "code_interpreter"
            }
        ],
        model="gpt-4"
    )

    # Create a thread for the assistant
    thread = client.beta.threads.create()

    # Insert messages into the thread
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=mat
    )

    # Execute the assistant and obtain a response
    response = ""
    with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Please address the user as friend.you should give the enire output in a natural way like humans.you should be polite and dedicated.",
        event_handler=EventHandler(),
    ) as stream:
        for chunk in stream:
            if hasattr(chunk, 'value'):
                response += chunk.value

   
    return response

# # Call the function and print the assistant's response
# print(get_assistant_response("What is the square of 499"))
