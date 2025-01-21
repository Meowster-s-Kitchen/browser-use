from langchain_openai import ChatOpenAI
import asyncio

from browser_use import Agent, SystemPrompt,Browser,BrowserConfig

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


async def main():

    agent = Agent(
        browser=Browser(BrowserConfig(headless=True)),
        task = """ 這個工具中 https://github.com/browser-use/browser-use?tab=readme-ov-file 可以用什麼方法登入自有的帳戶，例如facebook,Twiter？幫我看看程式碼 """,
        llm=ChatOpenAI(model="gpt-4o-mini",temperature=0.1),
        retry_delay=0,
        system_prompt_class=MySystemPrompt
    )
    result = await agent.run()
    print(result.model_thoughts())

asyncio.run(main())