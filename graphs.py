import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
    
plt.rcParams['font.size'] = 12

def __get_data(filename):
    data = pd.read_csv(f'resultados/{filename}.csv')
    z_pos = data.z.unique()
    x_pos = data.x.unique()

    plot_data = {
        'z': [],
        'x': [],
        'count': []
    }

    for item_x in x_pos:
        for item_z in z_pos:
            val = data.query('z == @item_z and x == @item_x').contagem.mean()
            plot_data['count'].append(val)
            plot_data['x'].append(item_x)
            plot_data['z'].append(item_z)

    plot_data = pd.DataFrame(plot_data)
    return plot_data

def zcount(filename):
    plot_data = __get_data(filename)

    sns.scatterplot(
        data = plot_data,
        x = 'z',
        y = 'count',
        hue = 'x',
        style = 'x'
    )

    plt.xticks(plot_data['z'])
    plt.xlabel('z (cm)')
    plt.legend(title = 'x (cm)', bbox_to_anchor=(1,1))
    plt.savefig('imgs/z-contagem.png')

def xcount(filename):
    plot_data = __get_data(filename)

    sns.scatterplot(
        data = plot_data,
        x = 'x',
        y = 'count',
        hue = 'z',
        style = 'z'
    )

    plt.xticks(plot_data['x'])
    plt.xlabel('x (cm)')
    plt.legend(title = 'z (cm)', bbox_to_anchor=(1,1))
    plt.savefig('imgs/x-contagem.png')

def count_over_time(filename, x_pos, z_pos):
    data = pd.read_csv(f'resultados/{filename}.csv')
    plot_data = data.query('z == @z_pos and x == @x_pos')

    sns.scatterplot(
        data = plot_data,
        x = 'tempo(s)',
        y = 'contagem'
    )

    plt.title(f'x = {x_pos} cm ---- z = {z_pos} cm')
    plt.savefig('imgs/count_over_time.png')