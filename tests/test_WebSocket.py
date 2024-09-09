import pytest
from unittest.mock import MagicMock, patch
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from autobahn.twisted.websocket import WebSocketClientFactory
from WebAPIClient.Containers import WebSocketSubscription

@pytest.fixture
def websocket_subscription():
    return WebSocketSubscription()

def test_init(websocket_subscription):
    assert websocket_subscription.callback is None
    assert isinstance(websocket_subscription.factory, WebSocketClientFactory)

def test_init_with_callback():
    callback = MagicMock()
    ws = WebSocketSubscription(callback=callback)
    assert ws.callback == callback

@patch('builtins.print')
def test_on_connect(mock_print, websocket_subscription):
    response = MagicMock()
    response.peer = "test_peer"
    websocket_subscription.onConnect(response)
    mock_print.assert_called_once_with("Server connected: test_peer")

@patch('builtins.print')
def test_on_open(mock_print, websocket_subscription):
    websocket_subscription.subscribe_to_topic = MagicMock()
    websocket_subscription.onOpen()
    mock_print.assert_called_once_with("WebSocket connection open.")
    websocket_subscription.subscribe_to_topic.assert_called_once()

def test_subscribe_to_topic(websocket_subscription):
    websocket_subscription.sendMessage = MagicMock()
    topic = "test_topic"
    websocket_subscription.subscribe_to_topic(topic)
    websocket_subscription.sendMessage.assert_called_once()

def test_on_message_binary(websocket_subscription):
    payload = b"test_binary_payload"
    websocket_subscription.callback = MagicMock()
    websocket_subscription.onMessage(payload, isBinary=True)
    expected_message = f"Binary message received: {len(payload)} bytes"
    websocket_subscription.callback.assert_called_once_with(expected_message)

def test_on_message_text(websocket_subscription):
    payload = "test_text_payload".encode('utf8')
    websocket_subscription.callback = MagicMock()
    websocket_subscription.onMessage(payload, isBinary=False)
    expected_message = f"Text message received: {payload.decode('utf8')}"
    websocket_subscription.callback.assert_called_once_with(expected_message)

def test_on_message_without_callback(websocket_subscription):
    payload = "test_payload".encode('utf8')
    # This should not raise an exception
    websocket_subscription.onMessage(payload, isBinary=False)

@patch('builtins.print')
def test_on_close(mock_print, websocket_subscription):
    reason = "test_reason"
    websocket_subscription.onClose(wasClean=True, code=1000, reason=reason)
    mock_print.assert_called_once_with(f"WebSocket connection closed: {reason}")

@patch('builtins.print')
def test_on_error(mock_print, websocket_subscription):
    failure = Exception("test_failure")
    websocket_subscription.onError(failure)
    mock_print.assert_called_once_with(f"WebSocket connection error: {failure}")