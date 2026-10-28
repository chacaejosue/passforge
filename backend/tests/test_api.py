import string
import unittest

from backend.passforge.app import create_app


class TestPasswordAPI(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def test_health(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "ok")

    def test_generates_password(self):
        response = self.client.post("/api/passwords", json={"length": 24})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["length"], 24)
        self.assertEqual(len(response.json["password"]), 24)
        self.assertIn("estimated_exhaustive_years", response.json)
        self.assertEqual(response.json["guesses_per_second"], 100_000_000_000)

    def test_entropy_estimate_for_minimum_length(self):
        response = self.client.post("/api/passwords", json={"length": 12})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["entropy"], 78.7)
        self.assertGreater(response.json["estimated_exhaustive_years"], 100_000)

    def test_rejects_invalid_options(self):
        response = self.client.post(
            "/api/passwords",
            json={"length": 20, "symbols": "yes"},
        )
        self.assertEqual(response.status_code, 400)

    def test_rejects_boolean_length(self):
        response = self.client.post("/api/passwords", json={"length": True})
        self.assertEqual(response.status_code, 400)

    def test_rejects_length_above_maximum(self):
        response = self.client.post("/api/passwords", json={"length": 256})
        self.assertEqual(response.status_code, 400)

    def test_rejects_all_disabled_options(self):
        response = self.client.post(
            "/api/passwords",
            json={
                "length": 16,
                "lowercase": False,
                "uppercase": False,
                "digits": False,
                "symbols": False,
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_generates_digits_only_when_selected(self):
        response = self.client.post(
            "/api/passwords",
            json={
                "length": 18,
                "lowercase": False,
                "uppercase": False,
                "digits": True,
                "symbols": False,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(all(ch in string.digits for ch in response.json["password"]))

    def test_security_and_cors_headers(self):
        response = self.client.post(
            "/api/passwords",
            json={"length": 16},
            headers={"Origin": "http://localhost:4321"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get("Access-Control-Allow-Origin"),
            "http://localhost:4321",
        )
        self.assertIn("no-store", response.headers.get("Cache-Control", ""))
        self.assertEqual(response.headers.get("X-Content-Type-Options"), "nosniff")
        self.assertEqual(response.headers.get("X-Frame-Options"), "DENY")

    def test_rate_limiting_returns_429(self):
        limited_client = create_app(rate_limit_per_minute=2).test_client()
        self.assertEqual(
            limited_client.post("/api/passwords", json={"length": 16}).status_code,
            200,
        )
        self.assertEqual(
            limited_client.post("/api/passwords", json={"length": 16}).status_code,
            200,
        )
        blocked = limited_client.post("/api/passwords", json={"length": 16})
        self.assertEqual(blocked.status_code, 429)
        self.assertIn("Retry-After", blocked.headers)


if __name__ == "__main__":
    unittest.main()
