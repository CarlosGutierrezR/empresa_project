from pathlib import Path
from datetime import datetime, timezone
from io import BytesIO
import zipfile

import pandas as pd
import requests


ECB_ZIP_URL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_CSV_PATH = DATA_DIR / "ecb_rates_raw.csv"
TRANSFORMED_CSV_PATH = DATA_DIR / "ecb_fx_rates_transformed.csv"


def download_ecb_csv_from_zip(url: str, output_path: Path) -> None:
    response = requests.get(url, timeout=60)
    response.raise_for_status()

    with zipfile.ZipFile(BytesIO(response.content)) as zf:
        csv_names = [name for name in zf.namelist() if name.endswith(".csv")]
        if not csv_names:
            raise ValueError("El ZIP del ECB no contiene ningún archivo CSV.")

        csv_bytes = zf.read(csv_names[0])
        output_path.write_bytes(csv_bytes)

def download_ecb_csv(url: str, output_path: Path) -> None:
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    output_path.write_bytes(response.content)


def transform_ecb_csv(input_path: Path, output_path: Path) -> pd.DataFrame:
    df = pd.read_csv(input_path)

    if "Date" not in df.columns:
        raise ValueError("El archivo del ECB no contiene la columna 'Date'.")

    df_long = df.melt(
        id_vars=["Date"],
        var_name="target_currency",
        value_name="exchange_rate",
    )

    df_long = df_long.dropna(subset=["exchange_rate"]).copy()

    df_long["rate_date"] = pd.to_datetime(df_long["Date"]).dt.date
    df_long["base_currency"] = "EUR"
    df_long["exchange_rate"] = pd.to_numeric(df_long["exchange_rate"], errors="coerce")
    df_long["ingestion_timestamp"] = datetime.now(timezone.utc).isoformat()
    df_long["source"] = "ECB"

    df_long = df_long.dropna(subset=["exchange_rate"])

    df_final = df_long[
        [
            "rate_date",
            "base_currency",
            "target_currency",
            "exchange_rate",
            "ingestion_timestamp",
            "source",
        ]
    ].copy()

    df_final.to_csv(output_path, index=False)
    return df_final


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("Descargando archivo oficial del ECB...")
    download_ecb_csv_from_zip(ECB_ZIP_URL, RAW_CSV_PATH)
    print(f"Archivo raw guardado en: {RAW_CSV_PATH}")

    print("Transformando datos al esquema objetivo...")
    df_final = transform_ecb_csv(RAW_CSV_PATH, TRANSFORMED_CSV_PATH)
    print(f"Archivo transformado guardado en: {TRANSFORMED_CSV_PATH}")
    print(f"Filas generadas: {len(df_final)}")
    print("Columnas finales:")
    print(list(df_final.columns))
    print(df_final.head(5).to_string(index=False))


if __name__ == "__main__":
    main()