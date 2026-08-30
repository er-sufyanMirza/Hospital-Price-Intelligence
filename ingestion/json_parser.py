from __future__ import annotations

import json
import hashlib
from pathlib import Path
from typing import Any

import pandas as pd


class MRFParser:
    """
    Parser for CMS Hospital Price Transparency JSON MRF v3.x.

    The parser converts the hierarchical CMS JSON structure
    into normalized analytical tables.
    """

    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)

        if not self.file_path.exists():
            raise FileNotFoundError(
                f"MRF file not found: {self.file_path}"
            )

        with self.file_path.open("r", encoding="utf-8") as file:
            self.data: dict[str, Any] = json.load(file)

    def parse(self) -> dict[str, pd.DataFrame]:
        """Parse the complete MRF."""

        return {
            "hospital": self._parse_hospital(),
            "location": self._parse_locations(),
            "service": self._parse_services(),
            "service_code": self._parse_service_codes(),
            "standard_charge": self._parse_standard_charges(),
            "payer_charge": self._parse_payer_charges(),
            "contract_provision": self._parse_contract_provisions(),
        }

    # ------------------------------------------------------------------
    # Hospital
    # ------------------------------------------------------------------

    def _parse_hospital(self) -> pd.DataFrame:
        """Extract hospital-level metadata."""

        license_info = self.data.get(
            "license_information", {}
        )

        row = {
            "hospital_id": self._hospital_id(),
            "hospital_name": self.data.get("hospital_name"),
            "state": license_info.get("state"),
            "license_number": license_info.get(
                "license_number"
            ),
            "mrf_version": self.data.get("version"),
            "last_updated_on": self.data.get(
                "last_updated_on"
            ),
        }

        return pd.DataFrame([row])

    # ------------------------------------------------------------------
    # Locations
    # ------------------------------------------------------------------

    def _parse_locations(self) -> pd.DataFrame:
        """
        Extract locations.

        CMS provides location_name, hospital_address and NPI
        collections independently. We preserve their values without
        inventing positional relationships between them.
        """

        locations = self.data.get("location_name", [])
        addresses = self.data.get("hospital_address", [])
        npis = self.data.get("type_2_npi", [])

        max_count = max(
            len(locations),
            len(addresses),
            len(npis),
            1,
        )

        rows = []

        for index in range(max_count):
            rows.append(
                {
                    "location_id": (
                        f"{self._hospital_id()}_LOC_"
                        f"{index + 1:04d}"
                    ),
                    "hospital_id": self._hospital_id(),
                    "location_name": (
                        locations[index]
                        if index < len(locations)
                        else None
                    ),
                    "hospital_address": (
                        addresses[index]
                        if index < len(addresses)
                        else None
                    ),
                    "npi": (
                        npis[index]
                        if index < len(npis)
                        else None
                    ),
                }
            )

        return pd.DataFrame(rows)

    # ------------------------------------------------------------------
    # Services
    # ------------------------------------------------------------------

    def _parse_services(self) -> pd.DataFrame:
        """Extract unique billable/service descriptions."""

        rows = []

        for index, service in enumerate(
            self.data.get(
                "standard_charge_information", []
            )
        ):
            rows.append(
                {
                    "service_id": (
                        f"{self._hospital_id()}_SVC_"
                        f"{index + 1:06d}"
                    ),
                    "hospital_id": self._hospital_id(),
                    "description": service.get(
                        "description"
                    ),
                }
            )

        return pd.DataFrame(rows)

    # ------------------------------------------------------------------
    # Service codes
    # ------------------------------------------------------------------

    def _parse_service_codes(self) -> pd.DataFrame:
        """Extract all codes associated with each service."""

        rows = []

        for service_index, service in enumerate(
            self.data.get(
                "standard_charge_information", []
            )
        ):
            service_id = (
                f"{self._hospital_id()}_SVC_"
                f"{service_index + 1:06d}"
            )

            for code_index, code_info in enumerate(
                service.get("code_information", [])
            ):
                rows.append(
                    {
                        "service_code_id": (
                            f"{service_id}_CODE_"
                            f"{code_index + 1:03d}"
                        ),
                        "service_id": service_id,
                        "code": code_info.get("code"),
                        "code_type": code_info.get("type"),
                    }
                )

        return pd.DataFrame(rows)

    # ------------------------------------------------------------------
    # Standard charges
    # ------------------------------------------------------------------

    def _parse_standard_charges(self) -> pd.DataFrame:
        """Extract service-level standard charges."""

        rows = []

        for service_index, service in enumerate(
            self.data.get(
                "standard_charge_information", []
            )
        ):
            service_id = (
                f"{self._hospital_id()}_SVC_"
                f"{service_index + 1:06d}"
            )

            for charge_index, charge in enumerate(
                service.get("standard_charges", [])
            ):
                rows.append(
                    {
                        "charge_id": (
                            f"{service_id}_CHG_"
                            f"{charge_index + 1:03d}"
                        ),
                        "service_id": service_id,
                        "setting": charge.get("setting"),
                        "minimum": charge.get("minimum"),
                        "maximum": charge.get("maximum"),
                        "gross_charge": charge.get(
                            "gross_charge"
                        ),
                        "discounted_cash": charge.get(
                            "discounted_cash"
                        ),
                    }
                )

        return pd.DataFrame(rows)

    # ------------------------------------------------------------------
    # Payer charges
    # ------------------------------------------------------------------

    def _parse_payer_charges(self) -> pd.DataFrame:
        """Extract payer-specific negotiated charges."""

        rows = []

        for service_index, service in enumerate(
            self.data.get(
                "standard_charge_information", []
            )
        ):
            service_id = (
                f"{self._hospital_id()}_SVC_"
                f"{service_index + 1:06d}"
            )

            for charge_index, charge in enumerate(
                service.get("standard_charges", [])
            ):
                charge_id = (
                    f"{service_id}_CHG_"
                    f"{charge_index + 1:03d}"
                )

                for payer_index, payer in enumerate(
                    charge.get(
                        "payers_information", []
                    )
                ):
                    dollar = payer.get(
                        "standard_charge_dollar"
                    )

                    percentage = payer.get(
                        "standard_charge_percentage"
                    )

                    algorithm = payer.get(
                        "standard_charge_algorithm"
                    )

                    if dollar is not None:
                        charge_type = "DOLLAR"
                    elif percentage is not None:
                        charge_type = "PERCENTAGE"
                    elif algorithm is not None:
                        charge_type = "ALGORITHM"
                    else:
                        charge_type = "UNKNOWN"

                    rows.append(
                        {
                            "payer_charge_id": (
                                f"{charge_id}_PAYER_"
                                f"{payer_index + 1:03d}"
                            ),
                            "charge_id": charge_id,
                            "payer_name": payer.get(
                                "payer_name"
                            ),
                            "plan_name": payer.get(
                                "plan_name"
                            ),
                            "methodology": payer.get(
                                "methodology"
                            ),
                            "additional_payer_notes": (
                                payer.get(
                                    "additional_payer_notes"
                                )
                            ),
                            "charge_type": charge_type,
                            "negotiated_dollar": dollar,
                            "negotiated_percentage": (
                                percentage
                            ),
                            "negotiated_algorithm": (
                                algorithm
                            ),
                            "median_allowed_amount": (
                                payer.get(
                                    "median_amount"
                                )
                            ),
                            "p10_allowed_amount": (
                                payer.get(
                                    "10th_percentile"
                                )
                            ),
                            "p90_allowed_amount": (
                                payer.get(
                                    "90th_percentile"
                                )
                            ),
                            "allowed_amount_count": (
                                payer.get("count")
                            ),
                        }
                    )

        return pd.DataFrame(rows)

    # ------------------------------------------------------------------
    # Contract provisions
    # ------------------------------------------------------------------

    def _parse_contract_provisions(
        self,
    ) -> pd.DataFrame:
        """Extract general payer contract provisions."""

        rows = []

        for index, provision in enumerate(
            self.data.get(
                "general_contract_provisions", []
            )
        ):
            rows.append(
                {
                    "contract_provision_id": (
                        f"{self._hospital_id()}_CONTRACT_"
                        f"{index + 1:04d}"
                    ),
                    "hospital_id": self._hospital_id(),
                    "payer_name": provision.get(
                        "payer_name"
                    ),
                    "provisions": provision.get(
                        "provisions"
                    ),
                }
            )

        return pd.DataFrame(rows)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _hospital_id(self) -> str:
        """Generate a stable hospital identifier."""

        hospital_name = self.data.get(
            "hospital_name",
            "UNKNOWN_HOSPITAL",
        )

        return (
            hospital_name
            .strip()
            .upper()
            .replace(" ", "_")
        )

    def file_hash(self) -> str:
        """Return SHA-256 hash of the source MRF."""

        sha256 = hashlib.sha256()

        with self.file_path.open("rb") as file:
            for chunk in iter(
                lambda: file.read(1024 * 1024),
                b"",
            ):
                sha256.update(chunk)

        return sha256.hexdigest()