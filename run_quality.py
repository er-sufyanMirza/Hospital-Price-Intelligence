from quality.validators import run_quality_checks
from quality.profiler import profile_tables


def main():

    print("=" * 70)
    print("HOSPITAL PRICE INTELLIGENCE")
    print("DATA QUALITY REPORT")
    print("=" * 70)

    print("\nTABLE PROFILE")
    print("-" * 70)

    profile = profile_tables()

    print(
        profile.to_string(
            index=False
        )
    )

    print("\nQUALITY CHECKS")
    print("-" * 70)

    checks = run_quality_checks()

    print(
        checks.to_string(
            index=False
        )
    )

    failed = (
        checks["status"] == "FAIL"
    ).sum()

    print("\n" + "=" * 70)

    if failed == 0:
        print("RESULT: PASS")
        print("All data quality checks passed.")
    else:
        print(
            f"RESULT: FAIL — "
            f"{failed} checks failed."
        )

    print("=" * 70)


if __name__ == "__main__":
    main()