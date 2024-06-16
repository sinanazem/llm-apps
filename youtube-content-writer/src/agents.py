from crewai import Agent

from langchain_openai import ChatOpenAI
from tools import yt_tool
import os


# Set environment variables
os.environ['OPENAI_API_BASE'] = 'http://localhost:11434/v1'
os.environ['OPENAI_MODEL_NAME'] = 'llama2'
os.environ['OPENAI_API_KEY'] = 'NA'

llm = ChatOpenAI(
    model = "crewai-llama2",
    base_url = "http://localhost:11434/v1")



## Create a senior blog content researcher
blog_researcher = Agent(
    role = 'Blog Researcher from Youtube Videos',
    goal = 'get the relevant video transcription for the topic {topic} from the provided Yt channel',
    verbose=True,
    memory=True,
    backstory=(
       "Expert in understanding videos in AI Data Science , Machine Learning And GEN AI and providing suggestion" 
    ),
    llm = llm,
    tools=[yt_tool],
    allow_delegation=True
)


## creating a senior blog writer agent with YT tool
blog_writer = Agent(
    role='Blog Writer',
    goal='Narrate compelling tech stories about the video {topic} from YT video',
    verbose=True,
    memory=True,
    backstory=(
        "With a flair for simplifying complex topics, you craft"
        "engaging narratives that captivate and educate, bringing new"
        "discoveries to light in an accessible manner."
    ),
    llm = llm,
    tools=[yt_tool],
    allow_delegation=False


)
