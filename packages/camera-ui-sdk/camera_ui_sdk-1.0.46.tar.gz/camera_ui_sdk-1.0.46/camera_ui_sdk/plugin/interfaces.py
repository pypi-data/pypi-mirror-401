from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Generic, Literal, NotRequired, Protocol, TypedDict, runtime_checkable

from typing_extensions import TypeVar as ExtTypeVar

from ..sensor import Detection
from .api import PluginAPI

if TYPE_CHECKING:
    from ..camera import CameraConfig, CameraDevice
    from ..manager import DiscoveredCamera
    from ..storage import DeviceStorage, JsonSchemaWithoutCallbacks
    from ..types import LoggerService

from ..storage import JsonSchema

# TypeVar for generic storage typing in BasePlugin
# Using Mapping as bound since TypedDict is compatible with Mapping but not dict
StorageT = ExtTypeVar("StorageT", bound=Mapping[str, Any], default=dict[str, Any])
"""TypeVar for plugin storage values type. Defaults to dict[str, Any]."""


class ImageMetadata(TypedDict):
    width: int
    height: int


class AudioMetadata(TypedDict):
    mimeType: Literal["audio/mpeg", "audio/wav", "audio/ogg"]


class MotionDetectionPluginResponse(TypedDict):
    detected: bool
    detections: list[Detection]
    videoData: NotRequired[bytes]


class ObjectDetectionPluginResponse(TypedDict):
    detected: bool
    detections: list[Detection]


class AudioDetectionPluginResponse(TypedDict):
    detected: bool
    detections: list[Detection]
    decibels: NotRequired[float]


class BasePlugin(ABC, Generic[StorageT]):
    """
    Base class for all plugins.

    Plugins must extend this class and implement the abstract methods
    for camera lifecycle management.

    Generic type parameter `StorageT` allows typed access to storage.values.

    Example:
        ```python
        class MyStorageValues(TypedDict):
            model_path: str
            threshold: float


        class MyPlugin(BasePlugin[MyStorageValues]):
            async def configureCameras(self, cameras: list[CameraDevice]) -> None:
                # storage.values is typed as MyStorageValues
                model_path = self.storage.values.get("model_path")  # str
                for camera in cameras:
                    await self.onCameraAdded(camera)

            async def onCameraAdded(self, camera: CameraDevice) -> None:
                # Initialize camera controller
                pass

            async def onCameraReleased(self, camera_id: str) -> None:
                # Cleanup camera controller
                pass
        ```
    """

    def __init__(self, logger: LoggerService, api: PluginAPI, storage: DeviceStorage[StorageT]) -> None:
        self.logger = logger
        self.api = api
        self.storage: DeviceStorage[StorageT] = storage

    @property
    def storage_schema(self) -> list[JsonSchema]:
        """Override to define plugin storage schema."""
        return []

    @abstractmethod
    async def configureCameras(self, cameraDevices: list[CameraDevice]) -> None:
        """
        Called on startup with all assigned cameras.

        Args:
            cameraDevices: List of cameras assigned to this plugin
        """
        ...

    @abstractmethod
    async def onCameraAdded(self, camera: CameraDevice) -> None:
        """
        Called when a camera is added/assigned to this plugin at runtime.

        Args:
            camera: The camera device that was added
        """
        ...

    @abstractmethod
    async def onCameraReleased(self, cameraId: str) -> None:
        """
        Called when a camera is removed/unassigned from this plugin at runtime.

        Args:
            cameraId: ID of the camera that was released
        """
        ...


@runtime_checkable
class DiscoveryProvider(Protocol):
    async def onDiscoverCameras(self) -> list[DiscoveredCamera]:
        """
        Scan for cameras and return discovered devices.
        Called by backend when polling or when user triggers manual rescan.

        Returns:
            List of discovered cameras
        """
        ...

    async def onGetCameraSettings(self, camera: DiscoveredCamera) -> list[JsonSchemaWithoutCallbacks]:
        """
        Get connection schema for a specific discovered camera.
        Returns form fields for credentials/settings needed to connect.

        Args:
            camera: The discovered camera

        Returns:
            JSON schema array for the connection form
        """
        ...

    async def onAdoptCamera(
        self, camera: DiscoveredCamera, cameraSettings: dict[str, object]
    ) -> CameraConfig:
        """
        Adopt a discovered camera.
        Provider probes the device and returns camera configuration.
        The backend will create the camera and call onCameraAdded().

        Args:
            camera: The discovered camera
            cameraSettings: User-provided settings from the connection form

        Returns:
            Camera configuration with sources
        """
        ...


@runtime_checkable
class MotionDetectionInterface(Protocol):
    async def testMotion(
        self, video_data: bytes, config: dict[str, Any]
    ) -> MotionDetectionPluginResponse | None: ...

    async def motionSettings(self) -> list[JsonSchema] | None: ...


@runtime_checkable
class ObjectDetectionInterface(Protocol):
    async def testObjects(
        self, image_data: bytes, metadata: ImageMetadata, config: dict[str, Any]
    ) -> ObjectDetectionPluginResponse | None: ...

    async def objectSettings(self) -> list[JsonSchema] | None: ...


@runtime_checkable
class AudioDetectionInterface(Protocol):
    async def testAudio(
        self, audio_data: bytes, metadata: AudioMetadata, config: dict[str, Any]
    ) -> AudioDetectionPluginResponse | None: ...

    async def audioSettings(self) -> list[JsonSchema] | None: ...
