import plotly.express as px
import pandas as pd

data = {
    "1": [
        "Task 1",
        "2023-01-01",
        "2023-02-01",
        31,
        ["emp1", "emp2"],
        "high"
    ],
    "2": [
        "Task 2",
        "2023-02-02",
        "2023-03-01",
        28,
        ["emp3", "emp4"],
        "medium"
    ],
    "3": [
        "t3",
        "2023-10-27",
        "2023-10-31",
        4,
        ["a", "n"],
        "high"
    ]
}

# Convert the data dictionary to a DataFrame for easier manipulation
df = pd.DataFrame.from_dict(data, orient='index',
                            columns=['Task', 'Start', 'End', 'Duration', 'Employees', 'Precedence'])

# Create the Gantt chart
fig = px.timeline(df, x_start='Start', x_end='End', y='Task')

# Customize the appearance of the Gantt chart
fig.update_yaxes(categoryorder="total ascending")
fig.update_layout(
    title="Gantt Chart with Task Details",
    xaxis_title="Timeline",
    yaxis_title="Tasks",
)

# Add custom hover text with all details from the dictionary
fig.update_traces(
    customdata=df[['Task', 'Start', 'End', 'Duration', 'Employees', 'Precedence']].values,
    hovertemplate="Task: %{customdata[0]}<br>Start Date: %{customdata[1]}<br>End Date: %{customdata[2]}<br>Duration: %{customdata[3]} days<br>Employees: %{customdata[4]}<br>Precedence: %{customdata[5]}",
)

# Show the Gantt chart
fig.show()
