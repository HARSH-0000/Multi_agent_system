from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from tool import web_search, web_scrape
from dotenv import load_dotenv
import os
load_dotenv()

#model setup
llm = ChatOpenAI(
    model="z-ai/glm-5.1", 
    temperature=0
)

def create_agent(model, tools):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert research assistant. Use the provided tools to rigorously find, extract, and synthesize deep and nuanced information. Avoid shallow summaries.\n\nConversation History:\n{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])
    agent = create_tool_calling_agent(model, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

#agent1
def search_agent():
    return create_agent(model=llm, tools=[web_search])

#agent2
def reader_agent():
    return create_agent(model=llm, tools=[web_scrape])

#creating chain

#chain1 writer
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a world-class academic researcher and technical writer. Your task is to write a highly detailed, comprehensive, and exhaustive report on the given topic based on the provided research and conversation history.\n\nConversation History:\n{chat_history}"),
    ("human", """Write a comprehensive, long-form report on the topic: {topic}
     
     research={content}

Structure the report with the following sections (use Markdown):
1. **Executive Summary**: High-level overview of the findings.
2. **Detailed Findings**: In-depth analysis of the scraped content, broken down by themes or subtopics. Expand on nuances.
3. **Implications & Future Outlook**: What this means for the field, industry, or users.
4. **Conclusion**: A strong closing summary.
5. **References**: A bulleted list of all URLs and sources used.

Requirements:
- Target length: ~1000 words.
- Tone: Professional, objective, and academic.
- Use inline citations where appropriate.
- Synthesize the provided content deeply, avoid shallow summaries.
"""),
])


writer_chain=writer_prompt | llm | StrOutputParser()


critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that critiques the given report and provides suggestions for improvement."),
    ("human", """Review the following report and provide constructive feedback on how to improve it. Focus on the clarity, coherence, and depth of the content. Also, suggest any additional information or sources that could enhance the report."""
    ),

])
critic_chain=critic_prompt | llm | StrOutputParser()