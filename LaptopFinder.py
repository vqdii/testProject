import pandas as pd


class LaptopFinder:
    def __init__(self):
        self.games_data = 5
        self.lappsto = 6

    def parse_ram(self, ram_str):
        try:
            return int(ram_str.upper().replace('GB', '').strip())
        except ValueError:
            return None

    def extract_info(self, cpu_str):
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

    def cpu_filter(self, row, game_cpu_series_list):
        for cpu_series, required_gen in game_cpu_series_list:
            if (
                    row['cpu_series'] == cpu_series
                    and row['cpu_gen'] is not None
                    and row['cpu_gen'] >= required_gen
            ):
                return True
        return False

    def find_suitable_laptops(self, game_name):

        game_spec = self.get_game_specs(game_name)
        if not game_spec:
            print(f"Гру з назвою '{game_name}' не знайдено")
            return

        game_memory = game_spec['memory']
        game_gpu = game_spec['gpu']
        game_cpu = game_spec['cpu']

        game_ram_gb = self.parse_ram(game_memory)
        if game_ram_gb is None:
            print(f"Некоректно вказано обсяг оперативної пам’яті для гри '{game_name}'")
            return

        game_cpu_series_list = [
            self.extract_info(cpu.strip()) for cpu in game_cpu.split(' or ')
        ]
        game_cpu_series_list = [
            (series, gen) for series, gen in game_cpu_series_list if series is not None
        ]

        game_gpus = [gpu.strip().lower() for gpu in game_gpu.split(' or ')]

        laptops_df = self.get_all_laptops()
        laptops_df['ram_gb'] = laptops_df['ram'].apply(self.parse_ram)
        laptops_df['gpu'] = laptops_df['gpu'].str.lower()
        laptops_df[['cpu_series', 'cpu_gen']] = laptops_df['cpu'].apply(
            lambda x: pd.Series(self.extract_info(x))
        )

        filtered_df = laptops_df[laptops_df['ram_gb'] >= game_ram_gb]

        filtered_df = filtered_df[
            filtered_df['gpu'].apply(lambda gpu: any(gpu_name in gpu for gpu_name in game_gpus))
        ]

        filtered_df = filtered_df[
            filtered_df.apply(lambda row: self.cpu_filter(row, game_cpu_series_list), axis=1)
        ]

        if not filtered_df.empty:
            print(f"Підходящі ноутбуки для гри '{game_name}':")
            print(filtered_df)
        else:
            print(f"Не знайдено підходящих ноутбуків для гри '{game_name}'")


