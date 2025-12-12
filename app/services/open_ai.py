from openai import OpenAI
from typing import Optional, List, Dict

class AIUtilityClient: # Đổi tên Class cho phù hợp với chức năng mới
    """
    Class wrapper để tương tác với OpenAI API (hoặc Custom Base URL).
    Chuyên dùng cho các tác vụ tạo Feedback dựa trên các chủ đề.
    """

    def __init__(self, api_key: str, base_url: str, deployment_name: str = "gpt-4o-mini"):
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )
        self.deployment_name = deployment_name
        # Prompts được định nghĩa ở đây
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
        Hàm nội bộ để gọi API chat completion và xử lý lỗi.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Lỗi khi gọi API: {e}")
            return None

    def generate_feedback(self, user_text: str, topic: str) -> str: # Sửa tên hàm thành generate_feedback
        """
        Tạo feedback/nhận xét cho đoạn văn bản (transcript) của người dùng dựa trên chủ đề.
        
        :param user_text: Đoạn văn bản (hoặc transcript) cần feedback.
        :param topic: Chủ đề feedback (Phải là key trong self.prompts, ví dụ: 'daily_conversation').
        :return: Nội dung feedback chi tiết từ AI.
        """
        topic = topic.lower().replace(" ", "_") # Chuẩn hóa topic
        
        # Kiểm tra topic có hợp lệ không
        if topic not in self.prompts:
            valid_topics = ", ".join(self.prompts.keys())
            return f"Lỗi: Chủ đề '{topic}' không hợp lệ. Vui lòng chọn một trong các chủ đề sau: {valid_topics}"
            
        system_prompt = self.prompts[topic]

        user_content = f"TEXT FOR FEEDBACK:\n\"\"\"{user_text}\"\"\"\n\nFEEDBACK:"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]

        # Gọi hàm nội bộ để lấy kết quả
        result = self._get_completion(messages)
        
        if result:
            return result
        else:
            return "Không thể tạo feedback do lỗi hệ thống."

    def custom_chat(self, prompt: str) -> str:
        """
        Hàm chat tự do nếu bạn muốn hỏi câu khác ngoài instruction.
        """
        messages = [{"role": "user", "content": prompt}]
        result = self._get_completion(messages)
        return result if result else "Lỗi."

# --- PHẦN SỬ DỤNG (USAGE) ---

if __name__ == "__main__":
    # 1. Cấu hình
    API_KEY = "sk-YfSO3RgAtWp8-SBGwXva1w"
    BASE_URL = "https://aiportalapi.stu-platform.live/jpe"
    MODEL_NAME = "gpt-4o-mini"

    # 2. Khởi tạo đối tượng (Instance)
    my_ai_assistant = AIUtilityClient(
        api_key=API_KEY,
        base_url=BASE_URL,
        deployment_name=MODEL_NAME
    )

    # 3. Định nghĩa Text của người dùng
    user_input_text = "I am live in Ha Noi. Yesterday I go to cinema with my friend and we see a very interested film."
    
    # 4. CHỌN CHỦ ĐỀ HỢP LỆ (Dùng chuỗi thay vì số 0)
    topic_choice_key = "daily_conversation" # Ví dụ chọn Daily Conversation

    # 5. Gọi hàm tạo Feedback
    print(f"--- Đang tạo feedback cho đoạn văn bản: \"{user_input_text}\" với chủ đề: {topic_choice_key} ---")
    
    # Sửa cú pháp gọi hàm
    feedback = my_ai_assistant.generate_feedback(
        user_text=user_input_text, 
        topic=topic_choice_key # Truyền vào chuỗi tên chủ đề
    )

    # 6. In kết quả
    print("\nRESULT:\n")
    print(feedback)