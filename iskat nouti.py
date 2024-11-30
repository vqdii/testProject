import pandas as pd

def get_all_laptops(self):
    query = '''
        SELECT laptop_id, company, product, type, inches, resolution, cpu, ram, memory, gpu, os, weight, price_in_euros
        FROM laptops
    '''
    df = pd.read_sql(query, self.db.connection)
    return df