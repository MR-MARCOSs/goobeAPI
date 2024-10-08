from flask import Flask, request, jsonify
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_functions_agent
from goobe_tools import google_trends, youtube_link, video_to_text, ddg_search

app = Flask(__name__)

@app.route('/goobe/query', methods=['GET'])
def goobe():
    try:
        query = request.args.get('query')
        if not query:
            return jsonify({'error': 'Parâmetro "query" é obrigatório.'}), 400

        llm = ChatOpenAI(model='gpt-4', temperature=0.5)
        toolkit = [google_trends, youtube_link, video_to_text, ddg_search]
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", """You are Goobe The Duck! a mix of DuckDuckGo, YouTube and Google, Your purpose of life is to help the User, use the available tools.
                If you don't have a tool to answer the question, say no.
                
                Return only the answers in cute and silly language.
                """),
                MessagesPlaceholder("chat_history", optional=True),
                ("human", "{input}"),
                MessagesPlaceholder("agent_scratchpad"),
            ]
        )
        agent = create_openai_functions_agent(llm, toolkit, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=toolkit, verbose=True)
        result = agent_executor.invoke({'input': f'{query}'})
        
        agent_response = result['output'] 
        return jsonify({'response': agent_response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
