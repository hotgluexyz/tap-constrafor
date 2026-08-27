"""Stream type classes for tap-constrafor."""

from __future__ import annotations

from typing import Any

from hotglue_singer_sdk import typing as th
from typing_extensions import override

from tap_constrafor.client import INCREMENTAL_DATETIME_FORMAT, ConstraforStream

LOCATION = th.ObjectType(
    th.Property("longitude", th.NumberType),
    th.Property("latitude", th.NumberType),
)

ADDRESS = th.ObjectType(
    th.Property("line1", th.StringType),
    th.Property("city", th.StringType),
    th.Property("state", th.StringType),
    th.Property("country", th.StringType),
    th.Property("postal_code", th.StringType),
    th.Property("location", LOCATION),
)

POLICY_PROJECT = th.ObjectType(
    th.Property("id", th.IntegerType),
    th.Property("name", th.StringType),
    th.Property("number", th.StringType),
    th.Property("client_id", th.IntegerType),
    th.Property("created_at", th.DateTimeType),
    th.Property("updated_at", th.DateTimeType),
)

DETAIL_PROJECT = th.ObjectType(
    th.Property("id", th.IntegerType),
    th.Property("name", th.StringType),
    th.Property("number", th.StringType),
    th.Property("client_id", th.IntegerType),
    th.Property("created_at", th.DateTimeType),
    th.Property("updated_at", th.DateTimeType),
    th.Property("type", th.StringType),
    th.Property("active", th.BooleanType),
    th.Property("description", th.StringType),
    th.Property("address", ADDRESS),
)

POLICY_SUBCONTRACTOR = th.ObjectType(
    th.Property("id", th.IntegerType),
    th.Property("name", th.StringType),
    th.Property("created_at", th.DateTimeType),
    th.Property("updated_at", th.DateTimeType),
)

DETAIL_SUBCONTRACTOR = th.ObjectType(
    th.Property("id", th.IntegerType),
    th.Property("name", th.StringType),
    th.Property("description", th.StringType),
    th.Property("address", ADDRESS),
    th.Property("contact_person", th.StringType),
    th.Property("contact_email", th.StringType),
    th.Property("contact_phone", th.StringType),
    th.Property("contact_fax", th.StringType),
    th.Property("federal_tax_id", th.StringType),
    th.Property("created_at", th.DateTimeType),
    th.Property("updated_at", th.DateTimeType),
)

DOCUMENT = th.ObjectType(
    th.Property("id", th.IntegerType),
    th.Property("name", th.StringType),
    th.Property("url", th.StringType),
)

POLICY_INSURANCE_REQUEST = th.ObjectType(
    th.Property("id", th.IntegerType),
    th.Property("start_date", th.DateType),
    th.Property("project", POLICY_PROJECT),
    th.Property("subcontractor", POLICY_SUBCONTRACTOR),
    th.Property("created_at", th.DateTimeType),
    th.Property("updated_at", th.DateTimeType),
)

DETAIL_INSURANCE_REQUEST = th.ObjectType(
    th.Property("id", th.IntegerType),
    th.Property("start_date", th.DateType),
    th.Property("project", DETAIL_PROJECT),
    th.Property("subcontractor", DETAIL_SUBCONTRACTOR),
    th.Property("documents", th.ArrayType(DOCUMENT)),
)

LIMIT_VALUE = th.CustomType({"type": ["number", "string", "null"]})

LIMITS = th.ObjectType(
    th.Property("aggregate_limit", LIMIT_VALUE),
    th.Property("e_l_each_accident", LIMIT_VALUE),
    th.Property("combined_single_limit", LIMIT_VALUE),
)


class InsurancePolicyStream(ConstraforStream):
    """Constrafor insurance policies."""

    name = "insurance_policy"
    path = "/insurance-policy"
    primary_keys = ["id"]
    replication_key = "updated_at"
    records_jsonpath = "$[*]"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("insurance_requests", th.ArrayType(POLICY_INSURANCE_REQUEST)),
        th.Property("type", th.StringType),
        th.Property("status", th.StringType),
        th.Property("insurance_carrier_name", th.StringType),
        th.Property("policy_number", th.StringType),
        th.Property("submitted_on", th.DateType),
        th.Property("approved_on", th.DateTimeType),
        th.Property("expiration_date", th.DateType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
    ).to_dict()

    @override
    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        starting = self.get_starting_time(context)
        params["updated_after"] = starting.strftime(INCREMENTAL_DATETIME_FORMAT)
        return params

    @override
    def get_child_context(self, record: dict, context: dict | None) -> dict:
        return {"insurance_policy_id": record["id"]}


class InsurancePolicyDetailStream(ConstraforStream):
    """Constrafor insurance policy details."""

    name = "insurance_policy_detail"
    path = "/insurance-policy/{insurance_policy_id}"
    parent_stream_type = InsurancePolicyStream
    primary_keys = ["id"]
    records_jsonpath = "$"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("insurance_requests", th.ArrayType(DETAIL_INSURANCE_REQUEST)),
        th.Property("type", th.StringType),
        th.Property("status", th.StringType),
        th.Property("insurance_carrier_name", th.StringType),
        th.Property("policy_number", th.StringType),
        th.Property("submitted_on", th.DateType),
        th.Property("approved_on", th.DateTimeType),
        th.Property("expiration_date", th.DateType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("insurance_carrier_naic", th.StringType),
        th.Property("limits", LIMITS),
        th.Property(
            "additional_insureds",
            th.CustomType({"type": ["array", "object", "null"]}),
        ),
        th.Property("comment", th.StringType),
    ).to_dict()
