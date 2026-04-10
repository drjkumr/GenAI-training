import os

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	FileReadTool,
	ScrapeWebsiteTool
)





@CrewBase
class AiContentCreationWorkflowCrew:
    """AiContentCreationWorkflow crew"""

    
    @agent
    def writer(self) -> Agent:
        
        return Agent(
            config=self.agents_config["writer"],
            
            
            tools=[				FileReadTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                
                
            ),
            
        )
    
    @agent
    def reviewer(self) -> Agent:
        
        return Agent(
            config=self.agents_config["reviewer"],
            
            
            tools=[				FileReadTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                
                
            ),
            
        )
    
    @agent
    def researcher(self) -> Agent:
        
        return Agent(
            config=self.agents_config["researcher"],
            
            
            tools=[				ScrapeWebsiteTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                
                
            ),
            
        )
    

    
    @task
    def research_latest_ai_trends(self) -> Task:
        return Task(
            config=self.tasks_config["research_latest_ai_trends"],
            markdown=False,
            
            
        )
    
    @task
    def write_blog_post(self) -> Task:
        return Task(
            config=self.tasks_config["write_blog_post"],
            markdown=False,
            
            
        )
    
    @task
    def review_and_polish_blog_post(self) -> Task:
        return Task(
            config=self.tasks_config["review_and_polish_blog_post"],
            markdown=False,
            
            
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the AiContentCreationWorkflow crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,

            chat_llm=LLM(model="openai/gpt-4o-mini"),
        )


