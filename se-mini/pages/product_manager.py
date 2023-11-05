import streamlit as st
import plotly.figure_factory as ff
import plotly.express as px
import pandas as pd
import json
from datetime import datetime





#reading from 
with open('project_schedule.json', 'r+') as file:
    project_schedule = json.load(file)






# Set page title and icon
st.set_page_config(
    page_title="Product Manager Login",
    page_icon="🛒",
    # layout="wide"
)








if "redirect" not in st.session_state:
   st.session_state["redirect"] = False

if "user_email" not in st.session_state:
   st.session_state["user_email"] = ""





def add_task_expander(expander, project):
    form_data = []

    task_input_form = expander.form('Task input form')
    task_input_form.write("Enter Task Details:")

        # Task ID input
    form_data.append(task_input_form.text_input("Task ID"))
        
        # Task Name input
    form_data.append(task_input_form.text_input("Task Name"))
        
        # Start Date input
    form_data.append(str(task_input_form.date_input("Start Date")))
        
        # End Date input
    form_data.append(str(task_input_form.date_input("End Date")))
        
        # Duration input
    form_data.append(task_input_form.number_input("Duration", min_value=0, step=1))
        
        # Employees input
    employees = task_input_form.text_input("Employees (comma-separated)")
    form_data.append(employees.split(",") if employees else [])
        
        # Precedence input
    form_data.append(task_input_form.selectbox("Precedence", ["high", "medium", "low"]))
        
        # Submit button
    submitted = task_input_form.form_submit_button("Add Task")


    if submitted:
        # st.session_state['selected_project_details'][form_data[0]] = form_data[1:]
        form_data.append(0)
        project_schedule[st.session_state['user_email']][project][form_data[0]] = form_data[1:]
        with open("project_schedule.json", "w") as outfile:
            json.dump(project_schedule, outfile, indent=4)

    st.button("press")






def login():
    # Create a simple title
    st.title("Product Manager Login")

    # Add input fields for username and password
    user_email = st.text_input("E-mail")
    password = st.text_input("Password", type="password")


    if st.button("Login"):
        if user_email in project_schedule:
            if project_schedule[user_email]["password"] == password: 
                st.session_state["user_email"] = user_email
                st.session_state['redirect'] = True
                st.success("Login successful! Redirecting...")
        else:
            st.error('Wrong credentials', icon="🚨")

    # Add a link to a registration or forgot password page
    st.markdown("[Forgot Password?](#) | [Register](#)")

    # Add a footer with contact information or additional links
    st.markdown(
        """
        ---
        Contact us at [email@example.com](mailto:email@example.com) or visit our website [example.com](http://example.com).
        """
    )





def dashboard():
    if "tasks" not in st.session_state:
        st.session_state.tasks = []

    if "added" not in st.session_state:
        st.session_state.added = 0

    # new_project_name = None
    # st.sidebar.title("Project Options")
    # if st.sidebar.button("Create New Project"):
    #     new_project = st.sidebar.text_input("Enter project name")
    #     if st.sidebar.button("create"):
    #         new_project_name = new_project
    #         project_schedule[st.session_state["user_email"]][new_project_name] = {"o":"p"}

    # if st.sidebar.button("lll"):
    #     # project_schedule[st.session_state["user_email"]][new_project_name] = {"o":"p"}
    #     st.sidebar.write(new_project_name)
        # st.sidebar.write(project_schedule[st.session_state['user_email']])


    st.sidebar.title("Project Options")
    st.sidebar.write("---")
    new_project = st.sidebar.text_input("Create a new project", placeholder="Enter project name")
    create = st.sidebar.button("Create")
    if create:
        project_schedule[st.session_state["user_email"]][new_project] = {}
        with open("project_schedule.json", "w") as outfile:
            json.dump(project_schedule, outfile, indent=4)
        # file.seek(0)
        # json.dumps(project_schedule, file, indent=4)

    projects_list = list(project_schedule[st.session_state["user_email"]].keys())
    projects_list[0] = "choose a project..."
    selected_project = st.sidebar.selectbox("Select a Project",projects_list)


    if selected_project != "choose a project...":
        st.header(f"Project: {selected_project}")
        st.session_state['selected_project_details'] = project_schedule[st.session_state["user_email"]][selected_project]
        add_task = st.expander("Add Task")
        add_task_expander(add_task, selected_project)

        if st.session_state['selected_project_details'] != {}:
            table_data = [{"Task ID": task_id, "Task Name": task[0], "Start Date": task[1], "End Date": task[2], "Duration": task[3], "Employees": ", ".join(task[4]), "Precedence": task[5], "completed %":task[6]} for task_id, task in st.session_state['selected_project_details'].items()]
            st.table(table_data)


        gantt_data = project_schedule[st.session_state['user_email']][selected_project]

        df = pd.DataFrame.from_dict(gantt_data, orient='index',
                            columns=['Task', 'Start', 'Finish', 'Duration', 'Employees', 'Precedence', 'completed %'])


        # fig = px.timeline(df, x_start='Start', x_end='End', y='Task')
        fig = ff.create_gantt(df, index_col='completed %', show_colorbar=True, group_tasks=True, show_hover_fill=True, bar_width=0.4, showgrid_x=True, showgrid_y=True)


        category_order = df['Task'].tolist()
        category_order.reverse()
        fig.update_yaxes(categoryorder="array", categoryarray=category_order)
        fig.update_layout(
            title="Gantt Chart with Task Details",
            xaxis_title="Timeline",
            yaxis_title="Tasks",
        )

        # fig.update_traces(
        #     customdata=df[['Task', 'Start', 'Finish', 'Duration', 'Employees', 'Precedence', 'completed %']].values,
        #     hovertemplate="Task: %{customdata[0]}<br>Start Date: %{customdata[1]}<br>End Date: %{customdata[2]}<br>Duration: %{customdata[3]} days<br>Employees: %{customdata[4]}<br>Precedence: %{customdata[5]}",
        # )
        fig.add_vline(x=datetime.now(), line_width=3, line_color="red")


        st.plotly_chart(fig)




    
































if st.session_state["redirect"] == False:
    login()
else:
    dashboard()