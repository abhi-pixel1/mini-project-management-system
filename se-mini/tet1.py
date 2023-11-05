import plotly.figure_factory as ff
import pandas as pd

data = {
    "1": [
        "Task 1",
        "2023-01-01",
        "2023-02-01",
        31,
        ["emp1", "emp2"],
        "high",
    ],
    "2": [
        "Task 2",
        "2023-02-02",
        "2023-03-01",
        28,
        ["emp3", "emp4"],
        "medium",
    ],
    "3": [
        "t3",
        "2023-10-27",
        "2023-10-31",
        4,
        ["a", "n"],
        "high",
    ],
}

# Create a DataFrame from the data dictionary
df = pd.DataFrame.from_dict(data, orient="index", columns=["Task Name", "Start Date", "End Date", "Duration", "Employees", "Precedence"])

# Convert date columns to datetime
df["Start Date"] = pd.to_datetime(df["Start Date"])
df["End Date"] = pd.to_datetime(df["End Date"])

df = df.rename(columns={"Start Date": "Start"})
df = df.rename(columns={"End Date": "Finish"})
df = df.rename(columns={"Task Name": "Task"})
# Calculate Task ID for Gantt chart
df["Task ID"] = df.index
print(df)



hover_text = [["t1"], ["t2"], ["t3"]]

# for index, row in df.iterrows():
#     print(index, row['Task'], type(row))
#     details = f"Task: {row['Task']}<br>Start Date: {row['Start']}<br>End Date: {row['Finish']}<br>Duration: {row['Duration']} days<br>Employees: {', '.join(row['Employees'])}<br>Precedence: {row['Precedence']}"
#     hover_text.append(details)




# Create a Gantt chart
fig = ff.create_gantt(
    df,
    index_col="Task ID",
    show_colorbar=True,
    group_tasks=True
)



fig.update_traces(text=hover_text, hoverinfo="text")

# Customize Gantt chart layout
fig.update_layout(
    title="Gantt Chart with Task Details",
    xaxis_title="Timeline",
    yaxis_title="Tasks",
)

# Show the Gantt chart
fig.show()
