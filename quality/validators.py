from __future__ import annotations

import duckdb
import pandas as pd


DATABASE_PATH = "data/processed/hospital_prices.duckdb"


def run_quality_checks() -> pd.DataFrame:
    con = duckdb.connect(DATABASE_PATH)

    checks = []

    def add_check(
        name: str,
        sql: str,
    ):
        result = con.execute(sql).fetchone()[0]

        checks.append(
            {
                "check_name": name,
                "failed_records": result,
                "status": (
                    "PASS"
                    if result == 0
                    else "FAIL"
                ),
            }
        )

    # ---------------------------------------------------------
    # Completeness
    # ---------------------------------------------------------

    add_check(
        "Hospital name missing",
        """
        SELECT COUNT(*)
        FROM hospital
        WHERE hospital_name IS NULL
        """,
    )

    add_check(
        "Service description missing",
        """
        SELECT COUNT(*)
        FROM service
        WHERE description IS NULL
        """,
    )

    add_check(
        "Payer name missing",
        """
        SELECT COUNT(*)
        FROM payer_charge
        WHERE payer_name IS NULL
        """,
    )

    # ---------------------------------------------------------
    # Uniqueness
    # ---------------------------------------------------------

    add_check(
        "Duplicate service IDs",
        """
        SELECT COUNT(*) - COUNT(DISTINCT service_id)
        FROM service
        """,
    )

    add_check(
        "Duplicate charge IDs",
        """
        SELECT COUNT(*) - COUNT(DISTINCT charge_id)
        FROM standard_charge
        """,
    )

    add_check(
        "Duplicate payer charge IDs",
        """
        SELECT COUNT(*)
             - COUNT(DISTINCT payer_charge_id)
        FROM payer_charge
        """,
    )

    # ---------------------------------------------------------
    # Referential integrity
    # ---------------------------------------------------------

    add_check(
        "Orphan payer charges",
        """
        SELECT COUNT(*)
        FROM payer_charge p
        LEFT JOIN standard_charge c
            ON p.charge_id = c.charge_id
        WHERE c.charge_id IS NULL
        """,
    )

    add_check(
        "Orphan service codes",
        """
        SELECT COUNT(*)
        FROM service_code sc
        LEFT JOIN service s
            ON sc.service_id = s.service_id
        WHERE s.service_id IS NULL
        """,
    )

    # ---------------------------------------------------------
    # Numeric validity
    # ---------------------------------------------------------

    add_check(
        "Negative gross charges",
        """
        SELECT COUNT(*)
        FROM standard_charge
        WHERE gross_charge < 0
        """,
    )

    add_check(
        "Negative negotiated dollar charges",
        """
        SELECT COUNT(*)
        FROM payer_charge
        WHERE negotiated_dollar < 0
        """,
    )

    add_check(
        "Minimum greater than maximum",
        """
        SELECT COUNT(*)
        FROM standard_charge
        WHERE minimum > maximum
        """,
    )

    # ---------------------------------------------------------
    # Charge-type consistency
    # ---------------------------------------------------------

    add_check(
        "Dollar charge missing negotiated dollar",
        """
        SELECT COUNT(*)
        FROM payer_charge
        WHERE charge_type = 'DOLLAR'
          AND negotiated_dollar IS NULL
        """,
    )

    add_check(
        "Percentage charge missing percentage",
        """
        SELECT COUNT(*)
        FROM payer_charge
        WHERE charge_type = 'PERCENTAGE'
          AND negotiated_percentage IS NULL
        """,
    )

    add_check(
        "Algorithm charge missing algorithm",
        """
        SELECT COUNT(*)
        FROM payer_charge
        WHERE charge_type = 'ALGORITHM'
          AND negotiated_algorithm IS NULL
        """,
    )

    con.close()

    return pd.DataFrame(checks)