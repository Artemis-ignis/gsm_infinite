import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
EVAL_REALISTIC = ROOT / "gsm-infinite" / "pred" / "eval_realistic.py"


def load_eval_realistic():
    spec = importlib.util.spec_from_file_location("eval_realistic", EVAL_REALISTIC)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CriteriaOutputTests(unittest.TestCase):
    def setUp(self):
        self.eval_realistic = load_eval_realistic()
        self.example = {"solution": "Reasoning steps. Answer: 123."}

    def test_text_answer_uses_current_reply(self):
        replies = [r"\text{answer: } 7", r"\text{answer: } 123"]

        corrected, total = self.eval_realistic.criteriaoutput(replies, self.example)

        self.assertEqual(corrected, 1)
        self.assertEqual(total, 2)

    def test_text_answer_at_end_of_reply_does_not_raise(self):
        replies = [r"\text{answer: } 123"]

        corrected, total = self.eval_realistic.criteriaoutput(replies, self.example)

        self.assertEqual(corrected, 1)
        self.assertEqual(total, 1)


if __name__ == "__main__":
    unittest.main()
