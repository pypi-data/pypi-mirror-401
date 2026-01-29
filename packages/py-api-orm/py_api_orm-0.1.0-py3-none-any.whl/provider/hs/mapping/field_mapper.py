import json
import os
from dataclasses import dataclass
from typing import Dict, TypeVar

from provider.hs.helpers import ObjectType

from lib.provider.hs.client import get_all_properties

T = TypeVar("T")


@dataclass
class FieldMapping:
    hs_object_type: ObjectType
    fields: Dict[str, str]


class HubSpotFieldMapper:

    def __init__(self, mapping_file_path: str):
        self._mapping_file_path = mapping_file_path
        self.field_mappings: Dict[str, FieldMapping] = {}

        self._load_mappings()

    def _load_mappings(self):
        # Create an absolute path to the mapping file
        abs_project_root_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../..")
        )
        abs_mapping_file_path = os.path.join(
            abs_project_root_path, self._mapping_file_path
        )

        with open(abs_mapping_file_path, "r", encoding="utf-8-sig") as mapping_file:
            mapping_data = json.load(mapping_file)

        if not isinstance(mapping_data, dict):
            raise TypeError("Mapping file must be a JSON object")

        object_mapping = mapping_data["mappings"]
        if not isinstance(object_mapping, list):
            raise TypeError(
                f"Invalid mapping structure for {self._mapping_file_path}. "
                f"'mappings' must be a list"
            )

        # Create field mappings
        for mapping in object_mapping:
            if "hs_object_type" not in mapping or "fields" not in mapping:
                raise ValueError(
                    f"Invalid mapping structure for {self._mapping_file_path}"
                )

            object_type = getattr(ObjectType, mapping["hs_object_type"].upper())
            mapping = FieldMapping(hs_object_type=object_type, fields=mapping["fields"])
            self._verify_properties_exist(mapping)
            self.field_mappings[object_type] = mapping

    def map_fields(self, source_object: dict, hs_object_type: str):
        # if not is_dataclass(source_object):
        #    raise TypeError("Source object must be a dataclass instance")

        # source_dict = asdict(source_object)
        res = {}

        field_mapping = self.field_mappings[hs_object_type]

        for external_field, hs_property in field_mapping.fields.items():
            if external_field in source_object:
                value = source_object[external_field]

                res[hs_property] = value

        return res

    @staticmethod
    def _verify_properties_exist(mapping: FieldMapping):
        all_properties = get_all_properties(mapping.hs_object_type).results
        property_names = [prop.name for prop in all_properties]

        for prop in mapping.fields.values():
            if prop not in property_names:
                raise ValueError(
                    f"Hubspot property '{prop}' does not exist for "
                    f"{mapping.hs_object_type}"
                )
