import unittest
from unittest.mock import Mock

from website_leads_database import WebsiteLeadsDatabaseClient


class PublicHelpersTest(unittest.TestCase):
    def setUp(self):
        self.client = WebsiteLeadsDatabaseClient(api_token="test-token")

    def test_count_forces_count_workflow_and_returns_summary(self):
        self.client._run = Mock(return_value={"defaultKeyValueStoreId": "store"})
        self.client._record = Mock(return_value={"total": 123})

        result = self.client.count({"platforms": ["shopify_sites"]})

        self.assertEqual(result, {"total": 123})
        payload = self.client._run.call_args.args[0]
        self.assertEqual(payload["workflow"], "count")
        self.assertTrue(payload["countOnly"])
        self.client._record.assert_called_once_with("store", "COUNT_SUMMARY")

    def test_run_page_forces_export_and_returns_continuation(self):
        self.client._run = Mock(return_value={
            "defaultDatasetId": "dataset",
            "defaultKeyValueStoreId": "store",
        })
        self.client._dataset = Mock(return_value=[{"Root Domain": "example.com"}])
        self.client._record = Mock(return_value={
            "hasMore": True,
            "resumeInput": {"offset": 50},
        })

        result = self.client.run_page({"maxItems": 50, "countOnly": True})

        payload = self.client._run.call_args.args[0]
        self.assertEqual(payload["workflow"], "export")
        self.assertFalse(payload["countOnly"])
        self.assertEqual(result["rows"][0]["Root Domain"], "example.com")
        self.assertEqual(result["continuation"]["resumeInput"]["offset"], 50)
        self.client._record.assert_called_once_with(
            "store", "EXPORT_CONTINUATION", required=False,
        )


if __name__ == "__main__":
    unittest.main()
