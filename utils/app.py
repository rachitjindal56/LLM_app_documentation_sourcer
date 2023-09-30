import openai
from metaphor_python import Metaphor
import streamlit as st
import json
import re
import os
from dotenv import load_dotenv
load_dotenv("./config/.env")

if 'type'     not in st.session_state   : st.session_state.type = ''
if 'language' not in st.session_state   : st.session_state.language = ''
if 'status'   not in st.session_state   : st.session_state.status = False
if 'traits'   not in st.session_state   : st.session_state.traits = None
if 't_status' not in st.session_state   : st.session_state.t_status = False

openai.api_key = os.getenv("OPENAI_API_KEY")

if st.session_state.traits != None:
    SYSTEM_PROMPT = f"""
    About User: {st.session_state.traits}
    Analyze the user about provided to create effective search query tailored to user
    
    You are a personal assistant of a software developer that caters to the person requests by providing appropriate data ans responses. You are 
    provided with a user query that can contain the details that might need to be extracted from provided functions. 
    Make call to the functions accordingly the answer the question.
    """
    
else:
    SYSTEM_PROMPT = """
    You are a personal assistant of a software developer that caters to the person requests by providing appropriate data ans responses. You are 
    provided with a user query that can contain the details that might need to be extracted from provided functions. 
    Make call to the functions accordingly the answer the question.
    """

def post_processing(data: str) -> str:
    
    CLEANR = re.compile('<.*?>') 
    
    df = re.sub("\n+","\n",data.lstrip().rstrip())
    df = re.sub("\t+","\t",df)
    df = re.sub("\s+"," ",df)
    df = re.sub(CLEANR,"",df)
    
    return df

def metaphor_search_for_data(query):
    
    metaphor = Metaphor(os.getenv("METAPHORE_API_KEY"))

    response = metaphor.search(
        query,
        num_results=5,
        use_autoprompt=True,
    ).results
    
    ids = []
    for i in response:
        ids.append(i.id)
            
    contents = metaphor.get_contents(ids).contents
    extracts = []
    
    for i in contents:
        extracts.append(post_processing(i.extract))
    
    return "\n\n".join(extracts)


def metaphor_search_for_documentation(query: str, programming_language: str = None) -> tuple:
    
    metaphor = Metaphor(os.getenv("METAPHORE_API_KEY"))

    if programming_language is not None:
        response = metaphor.search(
            f"{query}, Programming Language for documentation: {programming_language}",
            num_results=3,
            use_autoprompt=True,
        ).results
    
    else:
        response = metaphor.search(
            query,
            num_results=2,
            use_autoprompt=True,
        ).results
    
    ids = []
    links = []
    for i in response:
        ids.append(i.id)
        links.append(i.url)
    
    contents = metaphor.get_contents(ids).contents
    extracts = []
    
    for i in contents:
        extracts.append(post_processing(i.extract))
    
    return ("\n\n".join(extracts), links)


def run_conversation(query: str):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ],
        functions=[
            {
                "name": "metaphor_search_for_data",
                "description": "Search for data on open internet, or want to seach for any information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                          "type": "string",
                          "description": "Single and effective search query string",
                          }
                        },
                    "required": ["query"]
                },
            },
            {
                "name": "metaphor_search_for_documentation",
                "description": "Search for library, package, developer documentation for developer",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                          "type": "string",
                          "description": "Single and effective search query string on what documentation and what implementation to search for (shouldn't contain programming language)",
                          },
                        "programming_language": {
                          "type": "string",
                          "description": "Programming language",
                          }
                        },
                    "required": ["query"]
                },
            },
            {
                "name": "get_data",
                "description": "For fetching the review related to a product",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                          "type": "string",
                          "description": "The name to product whose review needs to be fetched",
                          }
                        },
                    "required": ["query"],
                },
            }
        ],
        function_call="auto",
    )

    message = response["choices"][0]["message"]
    print(message)
    if message.get("function_call"):
        function_name = message["function_call"]["name"]

        print(function_name,json.loads(message['function_call']['arguments']))

        if function_name == 'metaphor_search_for_data':
            
            st.session_state.type = 'data'
            
            function_response = metaphor_search_for_data(
                query=json.loads(message['function_call']['arguments'])["query"]
            )
            
            if st.session_state.traits != None:
                SYSTEM_PROMPT_2 = f"""
                About User: {st.session_state.traits}
                
                You are required to analyze the user and responsed in their tone and speech. Make sure to response as you know user we well.
                You are provided with the context details, answer the questions of the user query based on the provided context:
                
                context: {function_response}
                """
                
            else:
                SYSTEM_PROMPT_2 = f"""
                You are provided with the context details, answer the questions of the user query based on the provided context:
                
                context: {function_response}
                """
                
        elif function_name == 'metaphor_search_for_documentation':
            
            st.session_state.type = 'doc'
            st.session_state.language = json.loads(message['function_call']['arguments'])['programming_language'] if 'programming_language' in json.loads(message['function_call']['arguments']).keys() else "None"
            
            function_response = metaphor_search_for_documentation(
                query=json.loads(message['function_call']['arguments'])["query"],
                programming_language=json.loads(message['function_call']['arguments'])['programming_language'] if 'programming_language' in json.loads(message['function_call']['arguments']).keys() else None
            )
            
            if st.session_state.traits != None:
                SYSTEM_PROMPT_2 = f"""
                About User: {st.session_state.traits}
                
                You are required to analyze the user and responsed in their tone and speech. Make sure to response as you know user we well.
                You are provided with the documentation, and implementation details, answer the question of the user query based on the provided context:
                context: {function_response[0]}
                
                Added these links: {function_response[1]} for reference
                """
                
            else:
                SYSTEM_PROMPT_2 = f"""
                You are provided with the documentation, and implementation details, answer the question of the user query based on the provided context:
                context: {function_response[0]}
                
                Added these links: {function_response[1]} for reference
                """

        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT_2},
                {"role": "user", "content": query}
            ]
        )
        message = second_response["choices"][0]["message"]
    
    return message['content']