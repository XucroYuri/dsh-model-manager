import unittest

from dsh_model_manager import disable_model, enable_model, list_models

FIXTURE = {
    "ui-onboarding": {"welcomeNoticeVersion": "x"},
    "llm-pi-ai": {
        "providers": {
            "deepseek": {
                "apiKeyEnv": "DEEPSEEK_API_KEY",
                "models": [{"id": "deepseek-v4-flash"}, {"id": "deepseek-v4-pro", "name": "DeepSeek V4 Pro"}],
            }
        }
    },
}


class ManagerTests(unittest.TestCase):
    def test_list(self):
        rows = list_models(FIXTURE)
        self.assertEqual(rows[0][1], "deepseek-v4-flash")
        self.assertEqual(len(rows), 2)

    def test_enable_adds(self):
        settings = __import__("copy").deepcopy(FIXTURE)
        self.assertTrue(enable_model(settings, "deepseek", "deepseek-r1"))
        rows = list_models(settings)
        self.assertEqual(len(rows), 3)

    def test_enable_existing_noop(self):
        settings = __import__("copy").deepcopy(FIXTURE)
        self.assertFalse(enable_model(settings, "deepseek", "deepseek-v4-flash"))

    def test_disable_removes(self):
        settings = __import__("copy").deepcopy(FIXTURE)
        self.assertTrue(disable_model(settings, "deepseek", "deepseek-v4-flash"))
        rows = list_models(settings)
        self.assertEqual([r[1] for r in rows], ["deepseek-v4-pro"])

    def test_disable_missing_noop(self):
        settings = __import__("copy").deepcopy(FIXTURE)
        self.assertFalse(disable_model(settings, "deepseek", "missing"))


if __name__ == "__main__":
    unittest.main()
