import pandas as pd

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

    #ram
    filtered_df = laptops_df[laptops_df['ram_gb'] >= game_ram_gb]

    #gpu
    filtered_df = filtered_df[filtered_df['gpu'].apply(lambda gpu: any(gpu_name in gpu for gpu_name in game_gpus))]

    #cpu
    def cpu_filter(row):
        for cpu_series, required_gen in game_cpu_series_list:
            if (
                row['cpu_series'] == cpu_series and
                row['cpu_gen'] is not None and
                row['cpu_gen'] >= required_gen
            ):
                return True
        return False

    filtered_df = filtered_df[filtered_df.apply(cpu_filter, axis=1)]

    #result
    if not filtered_df.empty:
        print(f"Підходящі ноутбуки для гри '{game_name}':")
        print(filtered_df)
    else:
        print(f"Не знайдено підходящих ноутбуків для гри '{game_name}'")
