from functools import cached_property
from typing import cast

from keeper_secrets_manager_core import SecretsManager
from keeper_secrets_manager_core.dto.dtos import Record
from keeper_secrets_manager_core.dto.payload import QueryOptions
from keeper_secrets_manager_core.storage import InMemoryKeyValueStorage
from prefect.blocks.core import Block
from pydantic import Field, HttpUrl, SecretStr


class Keeper(Block):
    _logo_url = HttpUrl(
        "https://keepersecurity.com/vault/images/keeper_icons/icon_rounded_256.png"
    )
    _description = """
        A block for interacting with Keeper Security's Secrets Manager.
        This block allows you to securely retrieve secrets stored in Keeper by
        record UID or record title.
    """
    _block_type_name = "Keeper"
    _block_type_slug = "keeper"

    ksm_config: SecretStr = Field(description="The KSM config provided as a base64 encoded string")

    @cached_property
    def _client(self) -> SecretsManager:
        return SecretsManager(
            config=InMemoryKeyValueStorage(config=self.ksm_config.get_secret_value())
        )

    def get_record_by_uid(self, record_uid: str) -> Record | None:
        return next(
            iter(
                cast(
                    list[Record],
                    self._client.get_secrets_with_options(
                        query_options=QueryOptions(records_filter=record_uid, folders_filter=None)
                    ),
                )
            ),
            None,
        )

    def get_record_by_title(self, record_title: str) -> Record | None:
        return self._client.get_secret_by_title(record_title)
