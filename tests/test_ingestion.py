from pathlib import Path

from ingestion.json_parser import MRFParser


MRF_PATH = Path("data/raw/west_mercy_v3.json")


def get_tables():
    parser = MRFParser(MRF_PATH)
    return parser.parse()


def test_mrf_file_exists():
    assert MRF_PATH.exists()


def test_expected_tables_exist():
    tables = get_tables()

    expected = {
        "hospital",
        "location",
        "service",
        "service_code",
        "standard_charge",
        "payer_charge",
        "contract_provision",
    }

    assert expected.issubset(tables.keys())


def test_hospital():
    hospital = get_tables()["hospital"]

    assert len(hospital) == 1
    assert (
        hospital.loc[0, "hospital_name"]
        == "West Mercy Hospital"
    )
    assert (
        hospital.loc[0, "mrf_version"]
        == "3.0.0"
    )


def test_locations():
    locations = get_tables()["location"]

    assert len(locations) == 3
    assert locations["hospital_id"].nunique() == 1


def test_services():
    services = get_tables()["service"]

    assert len(services) == 22
    assert services["service_id"].is_unique


def test_service_codes():
    codes = get_tables()["service_code"]

    assert not codes.empty
    assert codes["service_code_id"].is_unique


def test_standard_charges():
    charges = get_tables()["standard_charge"]

    assert len(charges) == 22
    assert charges["charge_id"].is_unique


def test_payer_charges():
    payer = get_tables()["payer_charge"]

    assert len(payer) == 39
    assert payer["payer_charge_id"].is_unique


def test_charge_types():
    payer = get_tables()["payer_charge"]

    charge_types = set(
        payer["charge_type"].dropna()
    )

    assert "DOLLAR" in charge_types
    assert "PERCENTAGE" in charge_types
    assert "ALGORITHM" in charge_types


def test_percentage_charge():
    payer = get_tables()["payer_charge"]

    percentage = payer[
        payer["charge_type"] == "PERCENTAGE"
    ]

    assert not percentage.empty
    assert (
        percentage["negotiated_percentage"]
        .notna()
        .all()
    )


def test_algorithm_charge():
    payer = get_tables()["payer_charge"]

    algorithm = payer[
        payer["charge_type"] == "ALGORITHM"
    ]

    assert not algorithm.empty
    assert (
        algorithm["negotiated_algorithm"]
        .notna()
        .any()
    )


def test_contract_provisions():
    contracts = get_tables()[
        "contract_provision"
    ]

    assert len(contracts) == 2
    assert contracts["payer_name"].notna().all()