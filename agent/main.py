import os
import pandas as pd
import msal

AZURE_CLIENT_ID = os.environ.get("AZURE_CLIENT_ID")
AZURE_TENANT_ID = os.environ.get("AZURE_TENANT_ID")
AZURE_CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET")


def get_azure_token():
    """Get Azure access token using MSAL client credentials flow."""
    if not all([AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET]):
        print("Azure credentials not configured, skipping authentication.")
        return None

    authority = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
    app = msal.ConfidentialClientApplication(
        AZURE_CLIENT_ID,
        authority=authority,
        client_credential=AZURE_CLIENT_SECRET,
    )

    result = app.acquire_token_for_client(
        scopes=["https://graph.microsoft.com/.default"]
    )

    if "access_token" in result:
        print("Azure authentication successful.")
        return result["access_token"]
    else:
        print(
            f"Azure authentication failed: "
            f"{result.get('error_description', 'Unknown error')}"
        )
        return None


def fetch_french_wh_rates():
    """Fetch French withholding tax rates.

    Rates sourced from the French General Tax Code (CGI) and official
    Direction Générale des Finances Publiques (DGFiP) guidance.
    """
    rates_data = [
        {
            "Category": "Dividends - Standard rate",
            "Rate (%)": 26.5,
            "Notes": "Non-residents, default rate (Art. 119 bis CGI)",
        },
        {
            "Category": "Dividends - EU/EEA individual",
            "Rate (%)": 12.8,
            "Notes": "EU/EEA resident individual shareholders",
        },
        {
            "Category": "Interest",
            "Rate (%)": 0.0,
            "Notes": "Generally exempt for non-residents (Art. 131 quater CGI)",
        },
        {
            "Category": "Royalties",
            "Rate (%)": 26.5,
            "Notes": "Standard rate for non-residents (Art. 182 B CGI)",
        },
        {
            "Category": "Capital gains - Real estate (EU/EEA)",
            "Rate (%)": 19.0,
            "Notes": "EU/EEA resident individuals",
        },
        {
            "Category": "Capital gains - Real estate (non-EU)",
            "Rate (%)": 26.5,
            "Notes": "Non-EU/EEA residents",
        },
        {
            "Category": "Service / management fees",
            "Rate (%)": 26.5,
            "Notes": "Paid to non-residents (Art. 182 B CGI)",
        },
        {
            "Category": "Directors fees",
            "Rate (%)": 26.5,
            "Notes": "Paid to non-resident directors (Art. 182 B CGI)",
        },
        {
            "Category": "Salaries - Band 1",
            "Rate (%)": 0.0,
            "Notes": "Art. 182 A CGI - up to 16,015 EUR/year",
        },
        {
            "Category": "Salaries - Band 2",
            "Rate (%)": 12.0,
            "Notes": "Art. 182 A CGI - 16,015 to 46,762 EUR/year",
        },
        {
            "Category": "Salaries - Band 3",
            "Rate (%)": 20.0,
            "Notes": "Art. 182 A CGI - above 46,762 EUR/year",
        },
    ]

    df = pd.DataFrame(rates_data)
    return df


def main():
    print("Starting French Tax Withholding Rate Agent...")

    token = get_azure_token()
    _ = token  # token available for future Azure API calls

    print("Fetching French withholding tax rates...")
    df = fetch_french_wh_rates()

    print("\nFrench Withholding Tax Rates:")
    print(df.to_string(index=False))

    output_file = "french_wh_rates.csv"
    df.to_csv(output_file, index=False)
    print(f"\nRates saved to {output_file}")

    print("\nAgent completed successfully.")


if __name__ == "__main__":
    main()
