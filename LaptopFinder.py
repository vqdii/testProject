import re

import pandas as pd


class LaptopFinder:
    def __init__(self, games_file, laptops_file):
        self.games_data = pd.read_csv(games_file, sep=',')
        self.laptops = pd.read_csv(laptops_file)

    def parse_ram_all(self):
        for col in  self.games_data.select_dtypes(include=['object', 'string']):
            self.games_data[col] =  self.games_data[col].str.lower()
        for col in  self.laptops.select_dtypes(include=['object', 'string']):
            self.laptops[col] =  self.laptops[col].str.lower()

        self.games_data['parsed_memory'] = self.games_data['memory'].apply(self.parse_ram)
        self.laptops['parsed_memory'] = self.laptops['memory'].apply(self.parse_ram)
        self.laptops['parsed_ram'] = self.laptops['ram'].apply(self.parse_ram)


    def parse_ram(self, ram_str):
        try:
            if ram_str.upper().find('MB') != -1:
                return int(ram_str[:ram_str.upper().find('MB')])
                #return float(ram_str.replace('MB', ''))/1024
            if ram_str.upper().find('TB') != -1:
                return int(ram_str[:ram_str.upper().find('TB')])
                #return float(ram_str.replace(r'ТВ.*', ''))*1024
            return int(ram_str[:ram_str.upper().find('GB')])
        except ValueError:
            return None

    def get_game_specs(self, game_name):
        game_spec = self.games_data[self.games_data['name'].str.lower() == game_name.lower()]
        return game_spec.iloc[0] if not game_spec.empty else None

    def extract_info(self, cpu_str):
        match = re.match(r'(intel core [iI]\d)\s+(\d+)', cpu_str)
        if match:
            return match.group(1), int(match.group(2)[:1])
        return None, None

    def cpu_filter(self, row, game_cpu_series_list):
        laptop_series, laptop_gen = self.extract_info(row['cpu'].lower())
        for cpu_series, required_gen in game_cpu_series_list:
            if (
                    laptop_series == cpu_series
                    and laptop_gen is not None
                    and laptop_gen >= required_gen
                    #row['cpu_series'] == cpu_series
                    #and row['cpu_gen'] is not None
                    #and row['cpu_gen'] >= required_gen
            ):
                return True
        return False

    def find_suitable_laptops(self, game_name):
        print(self.games_data.head())
        print(self.games_data.columns)

        self.parse_ram_all()

        game_spec = self.get_game_specs(game_name)
        if game_spec.empty is None:
            print(f"Гру з назвою '{game_name}' не знайдено")
            return

        game_memory = game_spec['parsed_memory']
        game_gpu = game_spec['gpu']
        game_cpu = game_spec['cpu']

        #game_ram_gb = self.parse_ram(game_memory)
        #if game_ram_gb is None:
        #    print(f"Некоректно вказано обсяг оперативної пам’яті для гри '{game_name}'")
         #   return

        game_cpu_series_list = [
            self.extract_info(cpu.strip()) for cpu in game_cpu.split(' or ')
        ]
        game_cpu_series_list = [
            (series, gen) for series, gen in game_cpu_series_list if series is not None
        ]

        game_gpus = [gpu.strip().lower() for gpu in game_gpu.split(' or ')]

        filtered_df = self.laptops[self.laptops['parsed_ram'] >= game_memory]

        filtered_df = filtered_df[
            filtered_df['gpu'].apply(lambda gpu: any(gpu_name in gpu for gpu_name in game_gpus))
        ]

        filtered_df = filtered_df[
            filtered_df.apply(lambda row: self.cpu_filter(row, game_cpu_series_list), axis=1)
        ]


        if not filtered_df.empty:
            return filtered_df['product'].head(5).to_list()
        else:
            return []


