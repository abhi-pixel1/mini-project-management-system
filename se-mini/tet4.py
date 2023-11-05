import streamlit as st
import plotly.figure_factory as ff
import pandas as pd

# Create a Streamlit app
st.title("Project Management Software with Gantt Chart")


if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "added" not in st.session_state:
    st.session_state.added = 0





# Project name and description
with st.form("new task"):
    project_name = st.text_input("Project Name")
    project_description = st.text_area("Project Description")

    # Task input
    task_name = st.text_input("Task Name")
    task_start = st.date_input("Task Start Date")
    task_end = st.date_input("Task End Date")

    submit = st.form_submit_button('Add Task')



if submit:
    if task_name and task_start and task_end:
        st.session_state.tasks.append({"Task Name": task_name, "Start Date": str(task_start), "End Date": str(task_end)})







uploaded_file = st.file_uploader("Choose a file")
if st.session_state["added"] == 0 and uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    # st.write(dataframe)
    dict_list = df.to_dict('records')
    for i in dict_list:
        st.session_state.tasks.append(i)
    st.session_state["added"] = 1






# Initialize task list if not already defined
# if "tasks" not in st.session_state:
    # st.session_state.tasks = []

# Display tasks in a table
st.subheader("Task List")
st.dataframe(st.session_state.tasks)

# Create Gantt chart
if st.session_state.tasks:
    gantt_chart_data = []
    for task in st.session_state.tasks:
        gantt_chart_data.append(
            dict(Task=task["Task Name"], Start=task["Start Date"], Finish=task["End Date"])
        )

    fig = ff.create_gantt(gantt_chart_data, index_col="Task", title=project_name)
    st.plotly_chart(fig, theme=None)

# Reset tasks
if st.button("Clear Tasks"):
    st.session_state.tasks = []

# Export as CSV
if st.button("Export as CSV"):
    import pandas as pd

    df = pd.DataFrame(st.session_state.tasks)
    csv = df.to_csv(index=False)
    st.download_button("Download CSV", csv, key="csv")

# You can also add more features like editing tasks, setting dependencies, etc.