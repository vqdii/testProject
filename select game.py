import pandas as pd

def get_game_specs(self, game_name):
    query = "SELECT memory, gpu, cpu FROM games_data WHERE name = %s"
    result = pd.read_sql_query(query, self.db.connection, params=(game_name,))
    return result.iloc[0] if not result.empty else None