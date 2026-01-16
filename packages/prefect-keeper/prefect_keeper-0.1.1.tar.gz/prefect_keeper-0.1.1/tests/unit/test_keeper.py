from unittest.mock import Mock

import pytest
from keeper_secrets_manager_core import SecretsManager
from keeper_secrets_manager_core.dto.dtos import Record
from pydantic import SecretStr

from prefect_keeper import Keeper


@pytest.fixture
def keeper_block() -> Keeper:
    block = Keeper(ksm_config=SecretStr("toto"))
    block._client = Mock(spec=SecretsManager)

    return block


def test_get_record_by_return_none_when_record_not_found(keeper_block):
    keeper_block._client.get_secrets_with_options.return_value = []

    assert keeper_block.get_record_by_uid("123") is None


def test_get_record_by_uid_return_record_when_multiple_records_found(keeper_block):
    record_1 = Mock(spec=Record)
    record_2 = Mock(spec=Record)
    record_3 = Mock(spec=Record)

    keeper_block._client.get_secrets_with_options.return_value = [record_1, record_2, record_3]

    assert keeper_block.get_record_by_uid("123") == record_1


def test_get_record_by_uid_return_record(keeper_block):
    record = Mock(spec=Record)

    keeper_block._client.get_secrets_with_options.return_value = [record]

    assert keeper_block.get_record_by_uid("123") == record


def test_get_record_by_title_return_none_when_record_not_found(keeper_block):
    keeper_block._client.get_secret_by_title.return_value = None


def test_get_record_by_title_return_record_when_record_found(keeper_block):
    record = Mock(spec=Record)

    keeper_block._client.get_secret_by_title.return_value = record

    assert keeper_block.get_record_by_title("toto") == record
