from openai import OpenAI
from typing import Optional, List, Dict, Any
import json


class AIUtilityClient:
    """
    Class wrapper for interacting with OpenAI API.
    Supports topic-based feedback + custom-topic feedback via function calling.
    """

    def __init__(self, api_key: str, base_url: str, deployment_name: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.deployment_name = deployment_name

        # PRESET TOPICS
        self.prompts = {
            "daily_conversation": (
                "You are a friendly and encouraging native English speaker providing conversational feedback. "
                "Analyze the user's input focusing on natural flow, conversational phrases, and grammar. "
                "Use bullet points for suggestions."
            ),
            "travel": (
                "You are an expert travel guide and English coach. "
                "Review the user's response in a travel context, focusing on clarity, politeness, and travel vocabulary."
            ),
            "job_interview": (
                "You are an experienced HR Manager and English coach. "
                "Evaluate the user's job interview response. Focus on tone, clarity, and professionalism."
            ),
            "technology": (
                "You are a Tech Journalist and language expert. "
                "Analyze the user's discussion about technology. Focus on technical accuracy and advanced vocabulary."
            ),
            "free_talk": (
                "You are a friendly conversational partner and English tutor. "
                "Give natural responses and 2–3 gentle suggestions for improvement."
            ),
        }

        # FUNCTION CALLING TOOLS
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "extract_keywords",
                    "description": "Extract the single most relevant keyword/topic from the user's text.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "keyword": {
                                "type": "string",
                                "description": "A topic keyword (e.g., 'technology', 'finance', 'cooking').",
                            }
                        },
                        "required": ["keyword"],
                    },
                },
            }
        ]

    # -------------------------------------------------------------
    # Function the AI can call
    # -------------------------------------------------------------
    def extract_keywords(self, keyword: str):
        """Executed when the model calls the extract_keywords function."""
        return {"keyword": keyword}

    # -------------------------------------------------------------
    # INTERNAL CHAT COMPLETION (RAW RESPONSE)
    # -------------------------------------------------------------
    def _raw_completion(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[list] = None
    ) -> Any:
        """Return the raw OpenAI response (not string)."""
        return self.client.chat.completions.create(
            model=self.deployment_name,
            messages=messages,
            tools=tools
        )

    # -------------------------------------------------------------
    # MAIN FEEDBACK FUNCTION
    # -------------------------------------------------------------
    def generate_feedback(self, user_text: str, topic: str) -> str:
        topic = topic.lower().replace(" ", "_")

        # ---------------------------------------------------------
        # 1. PRESET TOPIC HANDLER
        # ---------------------------------------------------------
        if topic in self.prompts:
            system_prompt = self.prompts[topic]

            response = self._raw_completion([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ])

            return response.choices[0].message.content

        # ---------------------------------------------------------
        # 2. CUSTOM TOPIC USING FUNCTION CALLING
        # ---------------------------------------------------------
        if topic == "custom_topic":
            print("[INFO] Extracting keyword via Function Calling...")

            # Step 1: Ask AI to extract keyword
            initial_response = self._raw_completion(
                messages=[
                    {
                        "role": "user",
                        "content": f"Extract the single most important topic keyword from this text: \"{user_text}\""
                    }
                ],
                tools=self.tools
            )

            msg = initial_response.choices[0].message

            # Model MUST trigger a function call
            if not msg.tool_calls:
                return "Error: Model did not call the extract_keywords tool."

            # Step 2: Parse function call
            tool_call = msg.tool_calls[0]
            function_args = json.loads(tool_call.function.arguments)
            extracted_keyword = function_args["keyword"].lower()

            print(f"[INFO] Keyword extracted = {extracted_keyword}")

            # Step 3: Prepare system prompt from keyword
            if extracted_keyword in self.prompts:
                system_prompt = self.prompts[extracted_keyword]
            else:
                system_prompt = (
                    f"You are an English Speaking Coach specializing in **{extracted_keyword.upper()}**. "
                    "Give detailed, domain-specific, friendly feedback. Use bullet points."
                )

            # Step 4: Ask AI to give final feedback
            final_response = self._raw_completion([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ])

            return final_response.choices[0].message.content

        # ---------------------------------------------------------
        # ERROR: UNKNOWN TOPIC
        # ---------------------------------------------------------
        return "Error: Invalid topic. Choose a preset topic or 'custom_topic'."

    # -------------------------------------------------------------
    # FREE CHAT
    # -------------------------------------------------------------
    def custom_chat(self, prompt: str):
        response = self._raw_completion([{"role": "user", "content": prompt}])
        return response.choices[0].message.content


# -----------------------------------------------------------------
# USAGE EXAMPLE
# -----------------------------------------------------------------

if __name__ == "__main__":
    API_KEY = "sk-YfSO3RgAtWp8-SBGwXva1w"
    BASE_URL = "https://aiportalapi.stu-platform.live/jpe"
    MODEL_NAME = "gpt-4o-mini"

    ai = AIUtilityClient(API_KEY, BASE_URL, MODEL_NAME)

    # TEST #1 — Should match technology
    print("\n=== TEST 1: Should match Technology ===")
    text1 = "AI is growing very fast and changing our future rapidly."
    print(ai.generate_feedback(text1, "custom_topic"))

    # TEST #2 — New topic (finance)
    print("\n=== TEST 2: Should create Finance coach ===")
    text2 = "I want to invest money using compound interest and buy some stocks."
    print(ai.generate_feedback(text2, "custom_topic"))

    # TEST #3 — Travel topic (final)
    print("\n=== TEST 3==")
    text3 = "When I travel to Europe, I often get confused at customs and immigration. I want to improve my English so I can ask for directions and talk to hotel staff more confidently."
    print(ai.generate_feedback(text3, "custom_topic"))

"""

=== TEST 1: Should match Technology ===
[INFO] Extracting keyword via Function Calling...
[INFO] Keyword extracted = ai
Great observation! You’ve introduced a relevant topic that’s significant in today’s world. Here’s some friendly feedback to enhance your expression:

- **Clarity and Specificity**: 
  - Instead of saying "AI is growing very fast," you might specify how it's growing. For example, mentioning advancements in natural language processing or machine learning could add depth to your statement.
  - Instead of "changing our future rapidly," consider specifying how AI is affecting particular industries (like healthcare, education, or transportation) or aspects of daily life.

- **Engagement**:
  - To captivate your audience further, you could pose a rhetorical question. For example, "How will these advancements in AI reshape the way we work and communicate?"

- **Examples**:
  - Incorporate specific examples of AI technologies (like autonomous vehicles, virtual assistants, or recommendation systems) to give your audience a clearer picture of what you mean by change.

- **Enhance Vocabulary**:
  - Instead of repeating "changing," consider synonyms like "transforming," "redefining," or "revolutionizing." This can make your writing more dynamic.

- **Sentence Structure**:
  - Consider combining your thoughts into a single, flowing sentence for a more polished effect. For example: "The rapid growth of AI, particularly in fields like healthcare and transportation, is not only reshaping industries but also redefining our daily interactions and future possibilities."

By integrating these suggestions, you can create a more compelling and informative commentary on AI's rapid growth and its future implications. Keep it up!

=== TEST 2: Should create Finance coach ===
[INFO] Extracting keyword via Function Calling...
[INFO] Keyword extracted = investment
That’s a great decision! Investing and understanding compound interest are foundational to building wealth. Here are some detailed, friendly tips to help you along your investment journey:

### Understanding Compound Interest:
- **Definition**: Compound interest is the interest on a loan or deposit calculated based on both the initial principal and the accumulated interest from previous periods. 
- **Importance**: The earlier you start investing and letting your interest compound, the more wealth you can accumulate over time.
- **Formula**: Familiarize yourself with the compound interest formula:
  \[ A = P (1 + r/n)^{nt} \]
  Where:
  - \( A \) = the future value of the investment/loan, including interest
  - \( P \) = the principal investment amount (initial deposit)
  - \( r \) = the annual interest rate (decimal)
  - \( n \) = the number of times that interest is compounded per year
  - \( t \) = the number of years the money is invested for

### Investing in Stocks:
- **Research**: Always do thorough research or consider consulting with a financial advisor before purchasing stocks. Understand the business and market trends.
- **Diversification**: Don’t put all your eggs in one basket. Diversifying your investments can help minimize risks.
- **Long-term Perspective**: Consider investing for the long term to really take advantage of compound interest. The stock market can be volatile in the short term.
- **Investment Accounts**: Look into opening a tax-advantaged account like a Roth IRA or 401(k) if you're investing for retirement, as these can further enhance your compound growth.
- **Regular Contributions**: Consider dollar-cost averaging—investing a fixed amount regularly to reduce the impact of market volatility.

### Additional Investment Strategies:
- **Dividend Stocks**: Look for stocks that pay dividends, as these can be reinvested to capitalize on the power of compounding.
- **ETFs and Index Funds**: These funds can be excellent for beginners as they provide instant diversification and typically have lower fees compared to actively managed funds.

### Mindset and Habits:
- **Be Patient**: Compounding takes time, so be patient with your investments. Significant growth often requires a long timeframe.
- **Stay Informed**: Keep learning about market trends, new investment vehicles, and economic indicators to refine your strategy.
- **Review Regularly**: Keep track of your investments regularly but avoid knee-jerk reactions to market fluctuations.

### Final Thoughts:
- **Set Clear Goals**: Before you start investing, it’s helpful to define what you’re investing for—be it retirement, purchasing a home, or another specific financial goal.
- **Risk Tolerance**: Assess your risk tolerance before making investments. Stocks can provide great returns, but they can also carry greater risks.

By focusing on these areas, you'll be well on your way to making informed investment decisions. Happy investing! If you have any specific questions or need further clarification on anything, feel free to ask.

=== TEST 3==
[INFO] Extracting keyword via Function Calling...
[INFO] Keyword extracted = travel
Your response is clear and expresses your travel concerns well. To enhance clarity and politeness, you might consider specifying the aspects of customs and immigration that confuse you, as this will help others provide targeted advice. Additionally, mentioning specific areas you’d like to improve—such as vocabulary or phrasing related to directions and hotel interactions—could guide your learning process.

Here’s a refined version:

"When I travel to Europe, I sometimes feel confused at customs and immigration procedures. I would like to improve my English skills so I can confidently ask for directions and communicate with hotel staff. Any tips on vocabulary or common phrases that would be useful in these situations would be greatly appreciated!"

This version maintains your original message while incorporating a more polite tone and a request for specific guidance, making it easier for others to assist you.
"""