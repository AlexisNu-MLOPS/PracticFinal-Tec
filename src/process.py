"""
SageMaker Processing Job entrypoint.

Reads raw Titanic CSV from /opt/ml/processing/input/raw/
Saves processed train/validation/test CSV files to /opt/ml/processing/output/

SageMaker will automatically sync the output directory to the S3 path
configured in the ProcessingOutput of the ProcessingJob.
"""
import sys
import argparse
import logging
from pathlib import Path

import pandas as pd

# Add project root to path so src.preprocessing is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.preprocessing import preprocess_data  # noqa: E402

# ─── SageMaker standard paths ────────────────────────────────────────────────
INPUT_DIR = Path("/opt/ml/processing/input/raw")
OUTPUT_DIR = Path("/opt/ml/processing/output")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description="SageMaker Processing Job - Titanic")
    parser.add_argument(
        "--val-split", type=float, default=0.2,
        help="Fraction of training data to use as validation set (default: 0.2)"
    )
    parser.add_argument(
        "--random-state", type=int, default=42,
        help="Random seed for reproducibility (default: 42)"
    )
    parser.add_argument(
        "--input-dir", type=str, default=str(INPUT_DIR),
        help="Directory with raw CSV files (default: /opt/ml/processing/input/raw)"
    )
    parser.add_argument(
        "--output-dir", type=str, default=str(OUTPUT_DIR),
        help="Directory to write processed CSV files (default: /opt/ml/processing/output)"
    )
    return parser.parse_args()


def load_raw_data(input_dir: Path):
    """Load the primary CSV from input_dir.

    Looks for 'titanic_train.csv' first; if not found, takes the first
    CSV file in the directory (handles arbitrary filenames from S3).
    A second CSV (titanic_test.csv or the second file found) is used as
    the test set when available.
    """
    csv_files = sorted(input_dir.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            f"No CSV files found in {input_dir}. "
            "Make sure to mount the raw data to the input channel."
        )

    # Prefer explicit names, fall back to first file found
    train_path = input_dir / "titanic_train.csv"
    if not train_path.exists():
        train_path = csv_files[0]
        log.info("titanic_train.csv not found — using %s as training data.", train_path.name)

    log.info("Loading training data from %s", train_path)
    train_df = pd.read_csv(train_path)
    log.info("  → %d rows, %d columns", *train_df.shape)

    test_df = None
    test_path = input_dir / "titanic_test.csv"
    # Use second file as test set if explicit name not found
    if not test_path.exists() and len(csv_files) > 1:
        test_path = csv_files[1]
    if test_path.exists():
        log.info("Loading test data from %s", test_path)
        test_df = pd.read_csv(test_path)
        log.info("  → %d rows, %d columns", *test_df.shape)
    else:
        log.warning("No test CSV found in %s — skipping test set.", input_dir)

    return train_df, test_df


def save_processed_data(processed: dict, output_dir: Path):
    """Persist processed DataFrames as CSV files in output_dir."""
    output_dir.mkdir(parents=True, exist_ok=True)

    splits = {
        "train": (processed["X_train"], processed["y_train"]),
        "validation": (processed["X_val"], processed["y_val"]),
        "test": (processed["X_test"], processed["y_test"]),
    }

    for split_name, (X, y) in splits.items():
        if X is None:
            log.info("Skipping '%s' split — not available.", split_name)
            continue

        df = X.copy()
        if y is not None:
            df.insert(0, "Survived", y.values)

        out_path = output_dir / f"{split_name}.csv"
        df.to_csv(out_path, index=False)
        log.info("Saved %s split → %s  (%d rows, %d cols)", split_name, out_path, *df.shape)


def main():
    args = parse_args()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    log.info("=" * 55)
    log.info("TITANIC PROCESSING JOB")
    log.info("  input  : %s", input_dir)
    log.info("  output : %s", output_dir)
    log.info("  val_split   : %s", args.val_split)
    log.info("  random_state: %s", args.random_state)
    log.info("=" * 55)

    # 1. Load raw data
    train_df, test_df = load_raw_data(input_dir)

    # 2. Preprocess
    log.info("Running preprocessing pipeline …")
    processed = preprocess_data(
        train_df=train_df,
        test_df=test_df,
        val_split=args.val_split,
        random_state=args.random_state,
    )
    log.info(
        "  X_train: %s  |  X_val: %s  |  X_test: %s",
        processed["X_train"].shape if processed["X_train"] is not None else "—",
        processed["X_val"].shape if processed["X_val"] is not None else "—",
        processed["X_test"].shape if processed["X_test"] is not None else "—",
    )

    # 3. Save outputs
    log.info("Saving processed data …")
    save_processed_data(processed, output_dir)

    log.info("Processing complete. SageMaker will upload %s to S3.", output_dir)


if __name__ == "__main__":
    main()
