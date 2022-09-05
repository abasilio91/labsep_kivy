import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
    
plt.rcParams['font.size'] = 12

def zcount(filename):
    data = pd.read_csv(f'resultados/{filename}.csv')
    plot_data = {
        'z (cm)': data.z.unique(),
        'count': []
    }


    for item_z in plot_data['z (cm)']:
        val = data.query('z == @item_z').contagem.mean()
        plot_data['count'].append(val)

    plot_data = pd.DataFrame(plot_data)

    sns.scatterplot(
        data = plot_data,
        x = 'z (cm)',
        y = 'count'
    )
    plt.xticks(plot_data['z (cm)'])
    # plt.legend(title = 'x (cm)', bbox_to_anchor=(1,1))
    plt.savefig('imgs/z-contagem.png')