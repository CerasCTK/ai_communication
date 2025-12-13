import os
from openai import OpenAI
from dotenv import load_dotenv
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
    
    load_dotenv()

    API_KEY = os.getenv("OPENAI_API_KEY")
    BASE_URL = os.getenv("OPENAI_BASE_URL")
    MODEL_NAME = os.getenv("OPENAI_MODEL")

    if not API_KEY:
        raise RuntimeError("OPENAI_API_KEY not found")
        
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