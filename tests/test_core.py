from pathlib import Path
import unittest

from contracts_lab.core import check_response
from contracts_lab.fixture_check import check


class ContractTests(unittest.TestCase):
    def test_empty_and_continuation_pages(self):
        result = check_response({"status": 200, "payload": {"items": [], "next_cursor": None}})
        self.assertEqual(result, {"status": 200, "kind": "page", "item_count": 0, "has_next": False})
        self.assertTrue(check_response({"status": 200, "payload": {"items": [{"id": 3, "name": "Cafe"}], "next_cursor": 3}})["has_next"])

    def test_strict_order_and_cursor_validation(self):
        for ids, cursor in (([2, 1], None), ([1, 1], None), ([1, 2], 1), ([], 1)):
            with self.subTest(ids=ids), self.assertRaises(ValueError):
                check_response({"status": 200, "payload": {"items": [{"id": key, "name": "Cafe"} for key in ids], "next_cursor": cursor}})

    def test_error_contract(self):
        self.assertEqual(check_response({"status": 404, "payload": {"error": {"code": "not_found", "message": "Missing"}}}), {"status": 404, "kind": "error", "code": "not_found"})
        with self.assertRaises(ValueError):
            check_response({"status": 404, "payload": {"message": "Missing"}})

    def test_complete_fixture_corpus(self):
        self.assertGreaterEqual(check(Path(__file__).resolve().parents[1] / "fixtures/cases.jsonl", check_response), 350)


if __name__ == "__main__":
    unittest.main()
