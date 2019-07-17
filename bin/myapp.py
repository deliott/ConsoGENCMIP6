from functools import partial
from random import random
from threading import Thread
import time

from bokeh.models import ColumnDataSource
from bokeh.plotting import curdoc, figure

from tornado import gen

# this must only be modified from a Bokeh session callback
source = ColumnDataSource(data=dict(x=[0], y=[0]))

# This is important! Save curdoc() to make sure all threads
# see the same document.
doc = curdoc()

@gen.coroutine
def update(x, y):
    source.stream(dict(x=[x], y=[y]))

def blocking_task():
    while True:
        # do some blocking computation
        time.sleep(0.1)
        x, y = random(), random()

        # but update the document from callback
        doc.add_next_tick_callback(partial(update, x=x, y=y))

p = figure(x_range=[0, 1], y_range=[0,1])
l = p.circle(x='x', y='y', source=source)

doc.add_root(p)

thread = Thread(target=blocking_task)
thread.start()



#
#
#
# # myapp.py
# # bokeh serve --show myapp.py
#
# from random import random
#
# from bokeh.layouts import column
# from bokeh.models import Button
# from bokeh.palettes import RdYlBu3
# from bokeh.plotting import figure, curdoc
#
# # create a plot and style its properties
# p = figure(x_range=(0, 100), y_range=(0, 100), toolbar_location=None)
# p.border_fill_color = 'black'
# p.background_fill_color = 'black'
# p.outline_line_color = None
# p.grid.grid_line_color = None
#
# # add a text renderer to our plot (no data yet)
# r = p.text(x=[], y=[], text=[], text_color=[], text_font_size="20pt",
#            text_baseline="middle", text_align="center")
#
# i = 0
#
# ds = r.data_source
#
# # create a callback that will add a number in a random location
# def callback():
#     global i
#
#     # BEST PRACTICE --- update .data in one step with a new dict
#     new_data = dict()
#     new_data['x'] = ds.data['x'] + [random()*70 + 15]
#     new_data['y'] = ds.data['y'] + [random()*70 + 15]
#     new_data['text_color'] = ds.data['text_color'] + [RdYlBu3[i%3]]
#     new_data['text'] = ds.data['text'] + [str(i)]
#     ds.data = new_data
#
#     i = i + 1
#
# # add a button widget and configure with the call back
# button = Button(label="Press Me")
# button.on_click(callback)
#
# # put the button and plot in a layout and add to the document
# curdoc().add_root(column(button, p))