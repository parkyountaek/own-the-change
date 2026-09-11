import copy
import importlib.util
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/prepare_question.py"
SPEC = importlib.util.spec_from_file_location("prepare_question", SCRIPT)
QUESTION = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(QUESTION)


def payload():
    return {"choices": ["Preserve spaces", "Collapse whitespace", "Reject empty input", "Remove all spaces"],
            "answer": "Collapse whitespace", "unsure": "I'm not sure", "previous_positions": []}


class PrepareQuestionTests(unittest.TestCase):
    def test_five_question_sequence_preserves_content_key_and_input(self):
        for seed in range(40):
            request = payload()
            rng = random.Random(seed)
            for _ in range(5):
                original = copy.deepcopy(request)
                result = QUESTION.prepare_question(request, rng)
                self.assertEqual(request, original)
                self.assertEqual(len(result["choices"]), 5)
                self.assertEqual(set(result["choices"][:4]), set(request["choices"]))
                self.assertEqual(result["choices"][-1], request["unsure"])
                self.assertEqual(result["choices"][result["answer_position"] - 1], request["answer"])
                if request["previous_positions"]:
                    self.assertNotEqual(result["answer_position"], request["previous_positions"][-1])
                request["previous_positions"].append(result["answer_position"])

    def test_every_position_can_be_used_without_a_fixed_cycle(self):
        for previous in ([], [1], [2], [3], [4], [1, 2, 3]):
            request = payload()
            request["previous_positions"] = previous
            observed = {QUESTION.prepare_question(request, random.Random(seed))["answer_position"]
                        for seed in range(100)}
            self.assertEqual(observed, set(range(1, 5)) - set(previous[-1:]))

    def test_invalid_inputs_are_rejected_without_mutation(self):
        invalid = [None, [], {}, {**payload(), "extra": "data"}]
        for key, value in [("choices", ["a", "b", "c"]), ("choices", ["a", "a", "c", "d"]),
                           ("choices", ["A", " a ", "c", "d"]), ("choices", ["a", "b", "c", None]),
                           ("answer", "missing"), ("unsure", "Collapse whitespace"), ("unsure", " "),
                           ("previous_positions", [True]), ("previous_positions", [5]),
                           ("previous_positions", [1] * 5), ("previous_positions", "1")]:
            invalid.append({**payload(), key: value})
        for request in invalid:
            with self.subTest(request=request):
                original = copy.deepcopy(request)
                with self.assertRaises(ValueError):
                    QUESTION.prepare_question(request)
                self.assertEqual(original, request)

    def test_cli_is_stateless_and_preserves_localized_text(self):
        request = payload()
        request["unsure"] = "\uc798 \ubaa8\ub974\uaca0\uc74c"
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([sys.executable, str(SCRIPT)], input=json.dumps(request),
                                    cwd=directory, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["choices"][-1], request["unsure"])
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_cli_errors_do_not_echo_payload_or_emit_a_key(self):
        for raw in ('{"private-sentinel":', "private-sentinel" * 4000):
            result = subprocess.run([sys.executable, str(SCRIPT)], input=raw, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")
            self.assertNotIn("private-sentinel", result.stderr)


if __name__ == "__main__":
    unittest.main()
