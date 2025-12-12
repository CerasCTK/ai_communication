from openai import OpenAI
from typing import Optional, List, Dict

class AIUtilityClient:
    """
    Class wrapper for interacting with the OpenAI API (or Custom Base URL).
    Specialized for generating feedback based on specific topics.
    """

    def __init__(self, api_key: str, base_url: str, deployment_name: str = "gpt-4o-mini"):
        """
        Initializes the OpenAI Client.
        
        :param api_key: Your API key.
        :param base_url: Custom API base URL.
        :param deployment_name: The model or deployment name.
        """
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )
        self.deployment_name = deployment_name
        # Prompts are defined here
        self.prompts = {
            "daily_conversation": (
                "You are a friendly and encouraging native English speaker providing conversational feedback. "
                "Analyze the user's input focusing on natural flow, common conversational phrases, and basic grammar. "
                "Provide suggestions to make the response sound more natural in daily communication. Use bullet points."
            ),
            "travel": (
                "You are an expert travel guide and English coach. "
                "Review the user's response in a travel context. Focus on practical vocabulary (e.g., booking, directions, customs), clarity, and politeness required in travel situations. "
                "Suggest practical alternatives where necessary."
            ),
            "job_interview": (
                "You are an experienced HR Manager and English coach. "
                "Evaluate the user's response as part of a job interview. Focus on professionalism, clarity, conciseness, tone, and the effective use of professional vocabulary. "
                "Provide constructive advice on improving the impact of their answer."
            ),
            "technology": (
                "You are a Tech Journalist and language expert. "
                "Analyze the user's discussion on technology trends. Focus on the accuracy of technical terms, the coherence of complex ideas, and advanced vocabulary. "
                "Offer feedback on how to discuss technology topics more articulately."
            ),
            "free_talk": (
                "You are a conversational partner and an English tutor. "
                "Provide gentle and general feedback on the user's input, treating it as a casual conversation. Focus primarily on maintaining flow and basic comprehensibility. "
                "Start by responding naturally to their statement, then offer 2-3 brief language suggestions."
            )
        }

    def _get_completion(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> Optional[str]:
        """
        Internal function to call the chat completion API and handle errors.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"API call error: {e}")
            return None

    def generate_feedback(self, user_text: str, topic: str) -> str:
        """
        Generates feedback/review for the user's text (transcript) based on the topic.
        
        :param user_text: The text (or transcript) requiring feedback.
        :param topic: The feedback topic (Must be a key in self.prompts, e.g., 'daily_conversation').
        :return: Detailed feedback content from the AI.
        """
        topic = topic.lower().replace(" ", "_") # Normalize topic
        
        # Check if the topic is valid
        if topic not in self.prompts:
            valid_topics = ", ".join(self.prompts.keys())
            return f"Error: Invalid topic '{topic}'. Please select one of the following topics: {valid_topics}"
            
        system_prompt = self.prompts[topic]

        user_content = f"TEXT FOR FEEDBACK:\n\"\"\"{user_text}\"\"\"\n\nFEEDBACK:"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]

        # Call the internal function to get the result
        result = self._get_completion(messages)
        
        if result:
            return result
        else:
            return "Feedback generation failed due to system error."

    def custom_chat(self, prompt: str) -> str:
        """
        Free chat function for general queries outside of instruction generation.
        """
        messages = [{"role": "user", "content": prompt}]
        result = self._get_completion(messages)
        return result if result else "Error."

# --- USAGE SECTION ---

if __name__ == "__main__":
    # 1. Configuration
    API_KEY = "sk-YfSO3RgAtWp8-SBGwXva1w"
    BASE_URL = "https://aiportalapi.stu-platform.live/jpe"
    MODEL_NAME = "gpt-4o-mini"

    # 2. Initialize the object (Instance)
    my_ai_assistant = AIUtilityClient(
        api_key=API_KEY,
        base_url=BASE_URL,
        deployment_name=MODEL_NAME
    )

    # 3. Define the user's text
    user_input_text = "I am live in Ha Noi. Yesterday I go to cinema with my friend and we see a very interested film."
    
    # 4. CHOOSE A VALID TOPIC KEY
    topic_choice_key = "daily_conversation"

    # 5. Call the Feedback generation function
    print(f"--- Generating feedback for the text: \"{user_input_text}\" with topic: {topic_choice_key} ---")
    
    feedback = my_ai_assistant.generate_feedback(
        user_text=user_input_text, 
        topic=topic_choice_key
    )

    # 6. Print the result
    print("\nRESULT:\n")
    print(feedback)