import pandas as pd
df = pd.read_csv('laptops.csv', index_col='laptop_id', sep=',')

def extract_cpu_series(df, column_name):
    def extract_info(cpu_str):
        if "Intel Core i3" in cpu_str:
            series = "Intel Core i3"
        elif "Intel Core i5" in cpu_str:
            series = "Intel Core i5"
        elif "Intel Core i7" in cpu_str:
            series = "Intel Core i7"
        else:
            return None, None

        parts = cpu_str.split()
        for part in parts:
            if part.isdigit() and len(part) >= 4:
                generation = int(part[0])
                return series, generation

        return series, None

    extracted = df[column_name].apply(extract_info)
    df[['series', 'generation']] = pd.DataFrame(extracted.tolist(), index=df.index)
    return df

df = extract_cpu_series(df, 'cpu')

print(df.head())