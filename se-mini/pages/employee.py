import streamlit as st
import plotly.figure_factory as ff
import plotly.express as px
import pandas as pd
import json
from datetime import datetime


#reading from 
with open('employee.json', 'r+') as file:
    employee = json.load(file)



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









def progress_update_expander(expander, df):
    task_list = df['Task'].tolist()
    # st.write(column1_list)
    progress_update_form = expander.form('progress update form')
    progress_update_form.write("Select task:")
    task_name = progress_update_form.selectbox("Select a task...", task_list)
    progress_val = progress_update_form.number_input("Progress %", min_value=0, max_value=100, step=1)
    submitted = progress_update_form.form_submit_button("Update Task")

    if submitted:
        l = task_name.split(" : ")
        # expander.write(l)
        # project_schedule[]
        with open("project_schedule.json", "w") as outfile:
            json.dump(project_schedule, outfile, indent=4)


















def login():
    # Create a simple title
    st.title("Employee Login")

    # Add input fields for username and password
    user_email = st.text_input("E-mail")
    password = st.text_input("Password", type="password")


    if st.button("Login"):
        if user_email in employee:
            if employee[user_email]["password"] == password: 
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
    st.session_state['emp_details'] = employee[st.session_state['user_email']]
    assigned_tasks = [st.session_state['emp_details'][key] for key in st.session_state['emp_details'] if key.isdigit()]
    # st.write(project_details)

    overdue = []
    current = []
    future = []

    current_date = datetime.now()
    for i in assigned_tasks:
        start_date = datetime.strptime(project_schedule[i[0]][i[1]][i[2]][1], "%Y-%m-%d")
        end_date = datetime.strptime(project_schedule[i[0]][i[1]][i[2]][2], "%Y-%m-%d")

        task_details = project_schedule[i[0]][i[1]][i[2]]
        task_details.insert(0, project_schedule[i[0]]['name'])
        task_details.insert(1, i[1])
        if end_date < current_date:
            overdue.append(task_details)
        elif start_date > current_date:
            future.append(task_details)
        else:
            current.append(task_details)
    

    overdue_df = None
    current_df = None
    future_df = None
    if len(overdue)>0:
        overdue_df = pd.DataFrame(overdue, columns=['Project Manager', 'Project', 'Task', 'Start', 'Finish', 'Duration', 'Employees', 'Precidence', 'Completed %'])
        st.header("Overdue")
        st.dataframe(overdue_df, width=10000)
    if len(current)>0:
        current_df = pd.DataFrame(current, columns=['Project Manager', 'Project', 'Task', 'Start', 'Finish', 'Duration', 'Employees', 'Precidence', 'Completed %'])
        st.header("Current")
        st._arrow_table(current_df)
    if len(future):
        future_df = pd.DataFrame(future, columns=['Project Manager', 'Project', 'Task', 'Start', 'Finish', 'Duration', 'Employees', 'Precidence', 'Completed %'])
        st.header("Future")
        st.dataframe(future_df)







    gantt_data = pd.concat([overdue_df, current_df, future_df], ignore_index=True)
    gantt_data['Task'] = gantt_data.iloc[:, 0:3].apply(lambda row: ' : '.join(row), axis=1)
    gantt_data = gantt_data.drop(columns=['Project Manager', 'Project'])
    gantt_data['DateColumn'] = pd.to_datetime(gantt_data['Start'])
    gantt_data = gantt_data.sort_values(by='DateColumn')
    st.dataframe(gantt_data)




    progress_update = st.expander("Add Task")    
    progress_update_expander(progress_update, gantt_data)







    # fig = px.timeline(df, x_start='Start', x_end='End', y='Task')
    fig = ff.create_gantt(gantt_data, index_col='Completed %', show_colorbar=True, group_tasks=True, show_hover_fill=True, bar_width=0.4, showgrid_x=True, showgrid_y=True)


    category_order = gantt_data['Task'].tolist()
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