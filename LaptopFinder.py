import pandas as pd

class LaptopFinder:
    def __init__(self):
        self.aaa = 5

    def parse_ram(ram_str):
        try:
            return int(ram_str.upper().replace('GB', '').strip())
        except ValueError:
            return None

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

    def extract_cpu_series(df, column_name):
        extracted = df[column_name].apply(extract_info)
        df[['series', 'generation']] = pd.DataFrame(extracted.tolist(), index=df.index)
        return df

    def get_game_specs(self, game_name):
        query = "SELECT memory, gpu, cpu FROM games_data WHERE name = %s"
        result = pd.read_sql_query(query, self.db.connection, params=(game_name,))
        return result.iloc[0] if not result.empty else None

    def get_all_laptops(self):
        query = '''
            SELECT laptop_id, company, product, type, inches, resolution, cpu, ram, memory, gpu, os, weight, price_in_euros
            FROM laptops
        '''
        df = pd.read_sql(query, self.db.connection)
        return df

    def find_suitable_laptops(self, game_name):

        game_spec = self.get_game_specs(game_name)

        if not game_spec:
            print(f"Гру з назвою '{game_name}' не знайдено")
            return

        game_memory, game_gpu, game_cpu = game_spec

        game_ram_gb = self.parse_ram(game_memory)
        if game_ram_gb is None:
            print(f"Некоректно вказано обсяг оперативної пам’яті для гри '{game_name}'")
            return

        game_gpus = [gpu.strip().lower() for gpu in game_gpu.split(' or ')]
        game_cpu_series_list = [self.extract_cpu_series(cpu.strip()) for cpu in game_cpu.split(' or ')]
        game_cpu_series_list = [(series, gen) for series, gen in game_cpu_series_list if series is not None]

        laptops_df = self.get_all_laptops()

        laptops_df['ram_gb'] = laptops_df['ram'].apply(self.parse_ram)
        laptops_df['gpu'] = laptops_df['gpu'].str.lower()
        laptops_df[['cpu_series', 'cpu_gen']] = laptops_df['cpu'].apply(self.extract_cpu_series).apply(pd.Series)

        # ram
        filtered_df = laptops_df[laptops_df['ram_gb'] >= game_ram_gb]

        # gpu
        filtered_df = filtered_df[
            filtered_df['gpu'].apply(lambda gpu: any(gpu_name in gpu for gpu_name in game_gpus))]

        # cpu

        filtered_df = filtered_df[filtered_df.apply(cpu_filter, axis=1)]

        # result
        if not filtered_df.empty:
            print(f"Підходящі ноутбуки для гри '{game_name}':")
            print(filtered_df)
        else:
            print(f"Не знайдено підходящих ноутбуків для гри '{game_name}'")

    def cpu_filter(row):
        for cpu_series, required_gen in game_cpu_series_list:
            if (
                    row['cpu_series'] == cpu_series and
                    row['cpu_gen'] is not None and
                    row['cpu_gen'] >= required_gen
            ):
                return True
        return False

