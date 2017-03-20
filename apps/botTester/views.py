import numpy as np
import plotly.graph_objs as go
import plotly.offline as opy
from django.shortcuts import render


def example_graph(request):

    N=500
    random_x = np.linspace(0, 1, N)
    random_y = np.random.randn(N)

    trace = go.Scatter(
        x=random_x,
        y=random_y
    )

    data = go.Data([trace])
    layout = go.Layout(title='TestGraph', xaxis={'title':'x1'}, yaxis={'title':'x2'})
    figure = go.Figure(data=data, layout=layout)
    divLink = opy.plot(figure,auto_open=False, output_type='div', show_link=False)

    #L33t hacks for å fjerne mode-bar
    #with open(divLink, 'r') as file:
    #    tempHTML = file.read()
    # Replace the target strings
    #tempHTML = tempHTML.replace('displaylogo:!0', 'displaylogo:!1')
    #tempHTML = tempHTML.replace('modeBarButtonsToRemove:[]', 'modeBarButtonsToRemove:["sendDataToCloud"]')
    #with open(divLink, 'w') as file:
    #    file.write(tempHTML)
    #del tempHTML

    return render(request, 'graphTest.html', {'testGraph':divLink})

#example_graph('np')