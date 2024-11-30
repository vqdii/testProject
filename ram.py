import pandas as pd

data = {'ram': ['16GB', '8 gb', 'four GB', '32GB', '4 GB']}
df = pd.DataFrame(data)

def parse_ram(ram_str):
    try:
        return int(ram_str.upper().replace('GB', '').strip())
    except ValueError:
        return None

df['ram_gb'] = df['ram'].apply(parse_ram)

print(df)