import matplotlib
from matplotlib import pyplot as plt
import pandas as pd
import scienceplots
assert scienceplots, 'scienceplots needed'
plt.style.use(['science', 'no-latex'])

df = pd.read_csv('results.csv')
colors = matplotlib.colormaps['tab10'](range(len(df)))

ax = df.plot.bar(x='language', y='percentage', legend=False, title='Language Popularity', color=colors) 
ax.yaxis.set_label_text('Percentage (%)')
ax.xaxis.set_label_text('')

plt.savefig('results.svg')