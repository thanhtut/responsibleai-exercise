import csv
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
from tiny_pii.pii_pipeline import PIIPipeline  # Assuming this is your processor class


class CSVProcessor:
    def __init__(self, input_file: str, output_file: str = None):
        """
        Initialize the CSV processor.

        Args:
            input_file: Path to input CSV file
            output_file: Path to output CSV file (if None, will create based on input filename)
        """
        self.input_file = Path(input_file)
        if output_file is None:
            # Create output filename by adding '_processed' before extension
            self.output_file = (
                self.input_file.parent / f"{self.input_file.stem}_redacted{self.input_file.suffix}"
            )
        else:
            self.output_file = Path(output_file)

        self.processor = PIIPipeline()

    def _process_row(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single row and add new fields based on PII detection.

        Args:
            row: Dictionary containing row data

        Returns:
            Dictionary with additional fields based on processing results
        """
        result = self.processor.process(row["text"])

        # Add new fields to the row
        new_row = row.copy()
        new_row["name"] = result.name
        new_row["email"] = result.email
        new_row["phone"] = result.phone
        new_row["nric"] = result.nric
        new_row["address"] = result.address
        new_row["redacted_text"] = result.redacted_text

        return new_row

    def process_file(self) -> None:
        """
        Process the entire CSV file and create a new one with additional columns.
        """
        try:
            # Read input CSV file
            print(f"Reading file: {self.input_file}")
            df = pd.read_csv(self.input_file)

            # Process each row
            print("Processing rows...")
            processed_rows = []
            total_rows = len(df)

            for index, row in df.iterrows():
                # Show progress
                if (index + 1) % 100 == 0:
                    print(f"Processed {index + 1}/{total_rows} rows")

                processed_row = self._process_row(row.to_dict())
                processed_rows.append(processed_row)

            # Create new DataFrame with processed results
            result_df = pd.DataFrame(processed_rows)

            # Save to new CSV file
            print(f"Saving results to: {self.output_file}")
            result_df.to_csv(self.output_file, index=False)
            print("Processing completed successfully!")

        except Exception as e:
            print(f"Error processing file: {str(e)}")
            raise


def main():
    """
    Main function to run the CSV processor.
    """
    import argparse

    parser = argparse.ArgumentParser(description="Process CSV file for PII detection")
    parser.add_argument("input_file", help="Path to input CSV file")
    parser.add_argument("--output_file", help="Path to output CSV file (optional)")

    args = parser.parse_args()

    processor = CSVProcessor(args.input_file, args.output_file)
    processor.process_file()


if __name__ == "__main__":
    main()
