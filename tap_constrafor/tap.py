"""Singer tap for Constrafor."""

from __future__ import annotations

from typing import List

from hotglue_singer_sdk import Tap, Stream
from hotglue_singer_sdk import typing as th

from tap_constrafor.streams import InsurancePolicyDetailStream, InsurancePolicyStream


class TapConstrafor(Tap):
    """Constrafor tap."""

    name = "tap-constrafor"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType,
            required=True,
            description="Constrafor API key (sent as Authorization: Api-Key …)",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="Earliest record date for incremental sync",
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        return [
            InsurancePolicyStream(self),
            InsurancePolicyDetailStream(self),
        ]


if __name__ == "__main__":
    TapConstrafor.cli()
