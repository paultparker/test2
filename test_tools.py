import unittest
import json
from app.agent.tools import account_lookup, kb_search, crm_notes

class TestTools(unittest.TestCase):
    def test_account_lookup_success(self):
        result = account_lookup("ACC-123")
        data = json.loads(result)
        self.assertEqual(data["id"], "ACC-123")
        self.assertEqual(data["owner"], "Alice Smith")

    def test_account_lookup_not_found(self):
        result = account_lookup("ACC-999")
        self.assertIn("not found", result)

    def test_kb_search_success(self):
        result = kb_search("wire transfer")
        data = json.loads(result)
        self.assertTrue(len(data) > 0)
        self.assertIn("Wire Transfer Limits", data[0]["title"])

    def test_kb_search_no_results(self):
        result = kb_search("xyz_non_existent_term")
        self.assertIn("No relevant articles", result)

    def test_crm_notes_success(self):
        result = crm_notes("Alice")
        data = json.loads(result)
        self.assertIn("Alice Smith", data)
        self.assertTrue(len(data["Alice Smith"]) > 0)

    def test_crm_notes_not_found(self):
        result = crm_notes("UnknownClient")
        self.assertIn("No CRM notes found", result)

if __name__ == '__main__':
    unittest.main()
