import unittest

import responses

from storage_service.app.utils import Utils


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.utils = Utils()
        self.res_data = {'method': responses.GET,
                         'url': 'http://example.com/api/123',
                         'body': '{"error": "reason"}',
                         'status': 404,
                         'content_type': 'application/json', }

    def test_generate_id(self):
        new_id = self.utils.generate_id()
        self.assertIsNotNone(new_id)
        self.assertEqual(type(new_id), str)

    @responses.activate
    async def test_request_url(self):
        responses.add(**self.res_data)
        response = await self.utils.request_url('http://example.com/api/123')
        self.assertEqual({'error': 'reason'}, response.json())
        self.assertEqual(404, response.status_code)
