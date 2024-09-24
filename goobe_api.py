from dotenv import load_dotenv
from flask import Flask, request, jsonify
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_functions_agent
from goobe_tools import google_trends, youtube_link, video_to_text # Certifique-se de que goobe_tools esteja definido

load_dotenv()

app = Flask(__name__)

@app.route('/goobe/query', methods=['GET'])
def goobe():
    try:
        query = request.args.get('query')
        if not query:
            return jsonify({'error': 'Parâmetro "query" é obrigatório.'}), 400

        llm = ChatOpenAI(model='gpt-4', temperature=0.5) 
        toolkit = [google_trends, youtube_link, video_to_text]
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", """You are Goobe The Duck! a mix of DuckDuckGo, YouTube and Google, You purpose of life is help the User, use the available tools.
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

        # Retorne apenas a resposta do agente
        agent_response = result['output'] 
        return jsonify({'response': agent_response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)