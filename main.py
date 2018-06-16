import numpy as np
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.io import output_notebook,push_notebook,show
from os.path import dirname, join
from ipywidgets import interact
import numpy as np

from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, Div,BoxSelectTool
from bokeh.models.widgets import Slider, Select, TextInput
from bokeh.io import curdoc

from bokeh.models import HoverTool

output_notebook()
# prepare some data
fifa_data = pd.read_csv("FifaData.csv")



axis_map = {



	'Rating':'Rating',
	'Height':'Height',
	'Weight':'Weight',

	
	'Age':'Age',

	'Weak_foot':'Weak_foot',
	'Skill_Moves':'Skill_Moves',
	'Ball_Control':'Ball_Control',
	'Dribbling':'Dribbling',
	'Marking':'Marking',
	'Sliding_Tackle':'Sliding_Tackle',
	'Standing_Tackle':'Standing_Tackle',
	'Aggression':'Aggression',
	'Reactions':'Reactions',
	'Attacking_Position':'Attacking_Position',
	'Interceptions':'Interceptions',
	'Vision':'Vision',
	'Composure':'Composure',
	'Crossing':'Crossing',
	'Short_Pass':'Short_Pass',
	'Long_Pass':'Long_Pass',
	'Acceleration':'Acceleration',
	'Speed':'Speed',
	'Stamina':'Stamina',
	'Strength':'Strength',
	'Balance':'Balance',
	'Agility':'Agility',
	'Jumping':'Jumping',
	'Heading':'Heading',
	'Shot_Power':'Shot_Power',
	'Finishing':'Finishing',
	'Long_Shots':'Long_Shots',
	'Curve':'Curve',
	'Freekick_Accuracy':'Freekick_Accuracy',
	'Penalties':'Penalties',
	'Volleys':'Volleys',
	'GK_Positioning':'GK_Positioning',
	'GK_Diving':'GK_Diving',
	'GK_Kicking':'GK_Kicking',
	'GK_Handling':'GK_Handling',
	'GK_Reflexes':'GK_Reflexes'


}

desc = Div(text=open(join(dirname(__file__), "description.html")).read(), width=800)
# Create Input controls

# Club_Joining = Slider(title="Club_Joining", start=2000, end=2016, value=1970, step=1)
# Contract_Expiry = Slider(title="Contract_Expiry", start=2000 end=2025, value=2014, step=1)
Club = TextInput(title="Club")
Nationality = TextInput(title="Nationality")
x_axis = Select(title="x_axis:", value="Curve", options=sorted(axis_map.keys()))
y_axis = Select(title="y_axix:", value="Rating", options=sorted(axis_map.keys()))



# Create Column Data Source that will be used by the plot
source = ColumnDataSource(data=dict(x=[], y=[], Name=[],Nationality=[],Club=[],Preffered_Position=[]))


hover = HoverTool(tooltips=[
	("Name", "@Name"),
	("Nationality", "@Nationality"),
	("Club", "@Club"),
	# ("Preffered_Position", "$Preffered_Position"),
])



p = figure(plot_height=600, plot_width=700,tools=[hover,"box_select"])
p.circle(x="x", y="y", source=source, size=7)


def select_player():
	selected = fifa_data
	Club_val = Club.value.strip()
	Nationality_val = Nationality.value.strip()

	if (Club_val != ""):
		selected = selected[selected.Club.str.contains(Club_val)==True]
	if (Nationality_val != ""):
		selected = selected[selected.Nationality.str.contains(Nationality_val)==True]


	return selected


def update():
    df = select_player()
    x_name = axis_map[x_axis.value]
    y_name = axis_map[y_axis.value]
    
    p.xaxis.axis_label = x_axis.value
    p.yaxis.axis_label = y_axis.value

    p.title.text = "%d players selected" % len(df)


    source.data = dict(
        x=df[x_name],
        y=df[y_name],
        Name=df["Name"],
        Nationality =df["Nationality"],
        Club =df["Club"],
        # Preffered_Position =["Preffered_Position"]

    )


controls = [ x_axis, y_axis, Club,Nationality]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())


sizing_mode = 'fixed'  # 'scale_width' also looks nice with this example

inputs = widgetbox(*controls, sizing_mode=sizing_mode)
l = layout([
	[desc],
    [inputs, p],
], sizing_mode=sizing_mode)

update()  # initial load of the data


curdoc().add_root(l)
curdoc().title = "Fifa_2016"
