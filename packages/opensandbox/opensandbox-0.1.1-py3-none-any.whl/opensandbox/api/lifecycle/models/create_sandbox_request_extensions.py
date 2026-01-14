from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CreateSandboxRequestExtensions")


@_attrs_define
class CreateSandboxRequestExtensions:
    """Opaque container for provider-specific or transient parameters not supported by the core API.

    **Note**: This field is reserved for internal features, experimental flags, or temporary behaviors. Standard
    parameters should be proposed as core API fields.

    **Best Practices**:
    - **Namespacing**: Use prefixed keys (e.g., `storage.id`) to prevent collisions.
    - **Pass-through**: SDKs and middleware must treat this object as opaque and pass it through transparently.

    """

    additional_properties: dict[str, str] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        create_sandbox_request_extensions = cls()

        create_sandbox_request_extensions.additional_properties = d
        return create_sandbox_request_extensions

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> str:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
