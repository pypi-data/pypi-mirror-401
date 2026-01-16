import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Add the project root to the python path so we can import retell_lib
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock environment variables before importing RetellManager
with patch.dict(os.environ, {
    "TWILIO_ACCOUNT_SID": "ACmock",
    "TWILIO_AUTH_TOKEN": "mock_token",
    "TWILIO_PHONE_NUMBER": "+1234567890",
    "RETELL_API_KEY": "mock_retell_key",
    "WEBHOOK_URL": "https://example.com"
}):
    from retell_lib.retell_client import RetellManager

class TestRetellManager(unittest.TestCase):
    @patch.dict(os.environ, {
        "TWILIO_ACCOUNT_SID": "ACmock",
        "TWILIO_AUTH_TOKEN": "mock_token",
        "TWILIO_PHONE_NUMBER": "+1234567890",
        "RETELL_API_KEY": "mock_retell_key",
        "RETELL_AGENT_ID": "mock_agent_id"
    })
    def setUp(self):
        self.manager = RetellManager()
        # Mock the clients
        self.manager.twilio_client = MagicMock()
        self.manager.retell_client = MagicMock()

    def test_start_outbound_call(self):
        # Mock Retell register response
        mock_register_response = MagicMock()
        mock_register_response.audio_websocket_url = "wss://api.retellai.com/socket"
        self.manager.retell_client.call.register.return_value = mock_register_response
        
        # Mock Twilio call creation
        self.manager.twilio_client.calls.create.return_value.sid = "CA123"
        
        sid = self.manager.start_outbound_call("+15550000000")
        
        # Verify Retell register called
        self.manager.retell_client.call.register.assert_called_once()
        
        # Verify Twilio create called with TwiML
        self.manager.twilio_client.calls.create.assert_called_once()
        call_args = self.manager.twilio_client.calls.create.call_args[1]
        self.assertEqual(call_args['to'], "+15550000000")
        self.assertIn("<Stream url=\"wss://api.retellai.com/socket\" />", call_args['twiml'])
        self.assertEqual(sid, "CA123")

    def test_delete_room(self):
        self.manager.delete_room("CA123")
        # Retell client end_call should be called
        self.manager.retell_client.call.end_call.assert_called_with(call_id="CA123")
        # Twilio client update should be called
        self.manager.twilio_client.calls.assert_called_with("CA123")
        self.manager.twilio_client.calls("CA123").update.assert_called_with(status='completed')

    def test_start_recording(self):
        self.manager.start_recording("CA123")
        self.manager.twilio_client.calls("CA123").recordings.create.assert_called_once()

    def test_mute_participant(self):
        self.manager.mute_participant("CA123", "user", "track", True)
        self.manager.twilio_client.calls("CA123").update.assert_called_with(muted=True)

if __name__ == '__main__':
    unittest.main()
