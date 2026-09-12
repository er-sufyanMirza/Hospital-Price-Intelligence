import duckdb
import pandas as pd 

DATABASE_PATH = 'data/processed/hospital_prices.duckdb'
BENCHMARK_PATH = 'data/raw/medicare_benchmark_sample.csv'

def main():
    benchmark_df = pd.read_csv(BENCHMARK_PATH)
    
    