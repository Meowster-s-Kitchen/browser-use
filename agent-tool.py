from dataclasses import dataclass
from langchain_openai import ChatOpenAI
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use import Agent, Controller, SystemPrompt
from browser_use.utils import print_color

class MySystemPrompt(SystemPrompt):
    def important_rules(self) -> str:
        # Get existing rules from parent class
        existing_rules = super().important_rules()

        # Add your custom rules
        new_rules = """
					# MOST IMPORTANT RULES
					## 1. Source Verification
					- Require multiple independent sources to verify information
					- Prioritize official documentation and primary sources
					- Document all sources used with complete citations
					## 2. Temporal Analysis
					- Analyze data across multiple timeframes:
					- Past 7 days for immediate trends
					- Past 30 days for short-term patterns
					- Past 6 months for medium-term developments
					- Past year for long-term context
					- Clearly state the timeframe of all data points
					- Note when financial market data may be outdated
					## 3. Methodology
					- Establish foundational definitions before proceeding with analysis
					- Ignore promotional content and focus on substantive information
					- Document methodology and assumptions clearly
					## 4. Output Format
					- Present findings in formal research report structure
					- Include:
					- Executive summary
					- Methodology section
					- Detailed analysis
					- Complete source citations
					- Timestamp of data collection
					- Limitations of analysis
					## 5. Quality Control
					- Verify all technical terms and concepts
					- Cross-reference data points across sources
					- Highlight any discrepancies or contradictions
					- Note confidence levels in conclusions
					- Scroll the page by 550 pixel 
                    """
        # Make sure to use this pattern otherwise the exiting rules will be lost
        return f'{existing_rules}\n{new_rules}'


class search_agent:
    def __init__(self):
        self.browser = None

    def create(self, search_keyword: str) -> Agent:
        # Create browser instance if it doesn't exist
        if not self.browser:
            self.browser = Browser(
                config=BrowserConfig(
                    headless=True
                )
            )
        
        return Agent(
            task=f"{search_keyword}",
            llm=ChatOpenAI(model="gpt-4o", temperature=0.2),
            controller=Controller(),
            browser=self.browser,
            system_prompt_class=MySystemPrompt,
            retry_delay=0,
            use_vision=False
        )

    async def search(self, agent: Agent, max_steps: int) -> str:
        try:
            result = await agent.run(max_steps=max_steps)
            agent.create_history_gif(font_size=12)
            return str(result.final_result())
        except Exception as e:
            raise Exception(f"Error search: {str(e)}")
        finally:
            # Ensure browser cleanup
            if self.browser:
                await self.browser.close()
                self.browser = None


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from typing import Optional

app = FastAPI(title="Search Engine")

class SearchRequest(BaseModel):
    query: str
    max_steps: int = 100

class SearchResponse(BaseModel):
    status: str
    result: Optional[str] = None
    error: Optional[str] = None


@app.post("/search", response_model=SearchResponse)
async def perform_search(request: SearchRequest):
    search_engine = search_agent()
    try:
        print_color(request.query, 'green')
        agent = search_engine.create(request.query)
        result = await search_engine.search(agent, request.max_steps)
        return SearchResponse(
            status="success",
            result=result
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
