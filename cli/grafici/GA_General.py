import plotly.express as px
import os

dir_list = next(os.walk('out'))[1]
dir_list.sort()

ga_count = []

for dir in dir_list:
    count = 0
    with open(f'out/{dir}/google_analytics/point3/enti.tsv', 'r', encoding='utf-8-sig') as f:       
        next(f) #Salta la prima riga
        for line in f:
            line_values = line.split('\t')

            if int(line_values[35]) == 1:
                count += 1    
    
    ga_count.append(count)

fig = px.line(x=dir_list, y=ga_count, labels={'x':'Data', 'y':'PA contagiate da Google Analytics (fra le contattate da MonitoraPA)'}, title='MonitoraPA') 
fig.update_layout(yaxis_range=[0,8000])

fig.write_html("web/grafici/GA_General.html")