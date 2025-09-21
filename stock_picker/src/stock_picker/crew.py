# from crewai import Agent, Crew, Process, Task
# from crewai.project import CrewBase, agent, crew, task
# from crewai_tools import SerperDevTool
# from pydantic import BaseModel, Field
# from typing import List
# import ast
# import json


# # ---------------------------
# # Pydantic Models
# # ---------------------------
# class TrendingCompany(BaseModel):
#     """ A company that is in the news and attracting attention """
#     name: str = Field(description="Company name")
#     ticker: str = Field(description="Stock ticker symbol")
#     reason: str = Field(description="Reason this company is trending in the news")


# class TrendingCompanyList(BaseModel):
#     """ List of multiple trending companies that are in the news """
#     companies: List[TrendingCompany] = Field(description="List of companies trending in the news")


# class TrendingCompanyResearch(BaseModel):
#     """ Detailed research on a company """
#     name: str = Field(description="Company name")
#     market_position: str = Field(description="Current market position and competitive analysis")
#     future_outlook: str = Field(description="Future outlook and growth prospects")
#     investment_potential: str = Field(description="Investment potential and suitability for investment")


# class TrendingCompanyResearchList(BaseModel):
#     """ A list of detailed research on all the companies """
#     research_list: List[TrendingCompanyResearch] = Field(description="Comprehensive research on all trending companies")


# # ---------------------------
# # Helper Function
# # ---------------------------
# def fix_list_field(data, field_name):
#     """
#     Fix a field that may be returned as a string instead of a list.
#     Supports both Python-style strings and JSON-style strings.
#     """
#     if isinstance(data.get(field_name), str):
#         try:
#             data[field_name] = ast.literal_eval(data[field_name])
#         except Exception:
#             try:
#                 data[field_name] = json.loads(data[field_name])
#             except Exception:
#                 pass
#     return data


# # ---------------------------
# # Crew Definition
# # ---------------------------
# @CrewBase
# class StockPicker():
#     """StockPicker crew"""

#     agents_config = 'config/agents.yaml'
#     tasks_config = 'config/tasks.yaml'

#     # -------- Agents ----------
#     @agent
#     def trending_company_finder(self) -> Agent:
#         return Agent(
#             config=self.agents_config['trending_company_finder'],
#             tools=[SerperDevTool()]
#         )

#     @agent
#     def financial_researcher(self) -> Agent:
#         return Agent(
#             config=self.agents_config['financial_researcher'],
#             tools=[SerperDevTool()]
#         )

#     @agent
#     def stock_picker(self) -> Agent:
#         return Agent(
#             config=self.agents_config['stock_picker']
#         )

#     # -------- Tasks ----------
#     @task
#     def find_trending_companies(self) -> Task:
#         def output_handler(raw_output):
#             clean_output = fix_list_field(raw_output, "companies")
#             return TrendingCompanyList(**clean_output)

#         return Task(
#             config=self.tasks_config['find_trending_companies'],
#             output_pydantic=TrendingCompanyList,
#             output_handler=output_handler,  # Post-processor fix
#         )

#     @task
#     def research_trending_companies(self) -> Task:
#         return Task(
#             config=self.tasks_config['research_trending_companies'],
#             output_pydantic=TrendingCompanyResearchList,
#             output_json_converter=lambda raw: fix_list_field(raw, "research_list")
#         )

#     @task
#     def pick_best_company(self) -> Task:
#         return Task(
#             config=self.tasks_config['pick_best_company'],
#         )

#     # -------- Crew ----------
#     @crew
#     def crew(self) -> Crew:
#         """Creates the StockPicker crew"""

#         manager = Agent(
#             config=self.agents_config['manager'],
#             allow_delegation=True
#         )

#         return Crew(
#             agents=self.agents,
#             tasks=self.tasks,
#             process=Process.hierarchical,
#             verbose=True,
#             manager_agent=manager,
#         )


from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

@CrewBase
class StockPicker():
    """StockPicker crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # --- Agents ---
    @agent
    def trending_company_finder(self) -> Agent:
        return Agent(
            config=self.agents_config['trending_company_finder'],
            tools=[SerperDevTool()]
        )

    @agent
    def financial_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_researcher'],
            tools=[SerperDevTool()]
        )

    @agent
    def stock_picker(self) -> Agent:
        return Agent(
            config=self.agents_config['stock_picker']
        )

    # --- Tasks ---
    @task
    def find_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['find_trending_companies']
        )

    @task
    def research_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['research_trending_companies']
        )

    @task
    def pick_best_company(self) -> Task:
        return Task(
            config=self.tasks_config['pick_best_company']
        )

    # --- Crew ---
    @crew
    def crew(self) -> Crew:
        """Creates the StockPicker crew"""

        manager = Agent(
            config=self.agents_config['manager'],
            allow_delegation=True
        )

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            verbose=True,
            manager_agent=manager,
        )
