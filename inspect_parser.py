from ingestion.json_parser import MRFParser

parser = MRFParser('data/raw/west_mercy_v3.json')

tables = parser.parse()

for name,df in tables.items():
    print("\n" + "=" *70)
    print(name.upper())
    print("="*70)
    print("Row:",len(df))
    print("Column:" ,df.columns)
    print()
    
    print(df.to_string(index= False))
    