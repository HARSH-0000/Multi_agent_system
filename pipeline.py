from agents import search_agent, reader_agent, writer_chain, critic_chain

<<<<<<< HEAD
def research_pipeline(topic: str, chat_history: str = ""):
    state={}

    search_agent_exec = search_agent()
    search_result = search_agent_exec.invoke({
        "input": f"Search the web for recent and reliable information on the topic: {topic}",
        "chat_history": chat_history
    })
    state["search_results"] = search_result['output']
    print("Search Results:\n", state["search_results"])

    reader_agent_exec = reader_agent()
    reader_result = reader_agent_exec.invoke({
        "input": f"Extract the URLs from the search results and scrape the content of each URL. Summarize the content for better reading.\nSearch Results:\n{state['search_results']}",
        "chat_history": chat_history
    })
    state["scraped_content"] = reader_result['output']
    print("Scraped Content:\n", state["scraped_content"])
=======
def research_pipeline(topic : str):
    state={}

    search_agent=search_agent()
    search_result=search_agent.invoke({
        "message": f"Search the web for recent and reliable information on the topic: {topic}"
    })
    state["search_results"]=search_result['message'][-1].content
    print("Search Results:\n",state["search_results"])

    reader_agent=reader_agent()
    reader_result=reader_agent.invoke({
        "message": [{"user" f"Extract the URLs from the search results and scrape the content of each URL. Summarize the content for better reading."
        f"\nSearch Results:\n{state['search_results'][:900]}"
        }]


    })
    state["scraped_content"]=reader_result['message'][-1].content
    print("Scraped Content:\n",state["scraped_content"])
>>>>>>> a3e35a63d7a3930343af923c1b88e842743a5533


    writer_result=writer_chain.invoke({
        "topic": topic,
<<<<<<< HEAD
        "content": state["scraped_content"],
        "chat_history": chat_history
=======
        "content": state["scraped_content"]
        

>>>>>>> a3e35a63d7a3930343af923c1b88e842743a5533
    })

    state["report"]=writer_result
    print("Generated Report:\n",state["report"])

    critic_result=critic_chain.invoke({
        "report": state["report"]       
    })
    state["critique"]=critic_result
    print("Critique:\n",state["critique"])
    return state


if __name__=="__main__":
    topic=input("Enter the research topic: ")
    research_pipeline(topic)






