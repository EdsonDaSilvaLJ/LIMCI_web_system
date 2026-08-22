from django.test import TestCase


class CoreApiTests(TestCase):
    def test_health_endpoint(self):
        response = self.client.get("/api/v1/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_modules_endpoint(self):
        response = self.client.get("/api/v1/modules")

        self.assertEqual(response.status_code, 200)

        modules = response.json()
        self.assertEqual(len(modules), 2)
        self.assertEqual(
            {module["slug"] for module in modules},
            {"renal", "leukemia"},
        )
