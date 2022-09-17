import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
    
plt.rcParams['font.size'] = 12

def _get_data(folder_path, time, index):
    files = list(Path(folder_path).glob('*.txt'))
    data = {
        'measures': [],
        'time': []
    }

    for filename in files:
        df = pd.read_csv(filename, header=0, skiprows=4, sep=" ", skipinitialspace=True)
        data['measures'].append(df['GROSS'][0])
        data['time'].append(time * index)

    data = pd.DataFrame(data)
    return data

def count_over_time(folder_path, xpos, zpos, time, index):
    data = _get_data(folder_path, time, index)

    sns.scatterplot(
        data = data,
        x = 'time',
        y = 'measures'
    )

    plt.title(f'x = {xpos} cm --- z = {zpos} cm')
    plt.savefig('imgs/count_over_time.png')