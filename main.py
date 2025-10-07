from src.derived_processor import DerivedDataProcessor
from sqlalchemy import create_engine

if __name__ == "__main__":
    database_url = "sqlite:///db/database.db"
    processor = DerivedDataProcessor("train_data", "ideal_data", "test_data", database_url)
    final_result = processor.main()
    print(final_result)

    engine = create_engine(database_url)
    final_result.to_sql("result", engine, index=False, if_exists="replace")
    print("✔️ Results saved to database.db (table: result)")
