"""
Reactor SDK Message Types (v1)

These message types are used by the cloud runtime for control (WebSocket) and
application messaging. Outbound application messages should be wrapped in
ApplicationMessage for consistency with existing examples.
"""

from typing import Any, Dict, Literal, Union
from pydantic import BaseModel, Field


class ApplicationMessage(BaseModel):
    """
    Container for user application messages sent over WebSocket.
    """

    type: Literal["application"] = "application"
    data: Any = Field(..., description="User application data (JSON-serializable)")


class WebRTCOfferMessage(BaseModel):
    """WebRTC offer message from client to server"""

    type: Literal["webrtc-offer"] = "webrtc-offer"
    data: Dict[str, Any] = Field(..., description="WebRTC offer SDP")


class WebRTCAnswerMessage(BaseModel):
    """WebRTC answer message from server to client"""

    type: Literal["webrtc-answer"] = "webrtc-answer"
    data: Dict[str, Any] = Field(..., description="WebRTC answer SDP")


# Union of all SDK message types for validation
ReactorMessage = Union[ApplicationMessage, WebRTCOfferMessage, WebRTCAnswerMessage]
