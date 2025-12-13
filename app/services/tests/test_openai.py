from django.test import SimpleTestCase

from app.services.open_ai import AIUtilityClient


class TestOpenAI(SimpleTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        
        cls.API_KEY = "sk-YfSO3RgAtWp8-SBGwXva1w"
        cls.BASE_URL = "https://aiportalapi.stu-platform.live/jpe"
        cls.MODEL_NAME = "gpt-4o-mini"

        cls.ai = AIUtilityClient(
            api_key=cls.API_KEY, base_url=cls.BASE_URL, deployment_name=cls.MODEL_NAME
        )

    def test_custom_topic_technology(self) -> None:
        """Test technology topic"""
        text = "AI is growing very fast and changing our future rapidly."

        result = self.ai.generate_feedback(text, "custom_topic")

        self.assertIsNotNone(result)
        self.assertTrue(len(result) > 20)

    def test_custom_topic_finance(self) -> None:
        """Test finance topic"""
        text = "I want to invest money using compound interest and buy some stocks."

        result = self.ai.generate_feedback(text, "custom_topic")

        self.assertIsNotNone(result)
        self.assertTrue(len(result) > 20)

    def test_custom_topic_travel(self) -> None:
        """Test travel topic"""
        text = (
            "When I travel to Europe, I often get confused at customs and immigration. "
            "I want to improve my English so I can ask for directions and talk to hotel staff more confidently."  # noqa: E501
        )

        result = self.ai.generate_feedback(text, "custom_topic")

        self.assertIsNotNone(result)
        self.assertTrue(len(result) > 20)
