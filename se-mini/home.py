import streamlit as st

# Set page title and icon
st.set_page_config(
    page_title="Mini Project Management System",
    page_icon=":rocket:"
)

# Define the title and a brief introduction
st.title("Welcome to the Mini Project Management System")
st.markdown("This is a non-functional prototype for project management.")

# Create a sidebar with project options
st.sidebar.title("Project Options")
selected_project = st.sidebar.selectbox(
    "Select a Project",
    ["Project A", "Project B", "Project C"]
)

# Create a button to create a new project
if st.sidebar.button("Create New Project"):
    new_project_name = st.text_input("Enter Project Name:")
    if st.button("Create"):
        # Add logic here to create a new project
        st.success(f"Project '{new_project_name}' created successfully!")

# Display project information
st.header(f"Project: {selected_project}")
project_description = "This is a non-functional project description."
st.write(project_description)

# Create a button to view project details
if st.button("View Project Details"):
    # Add logic here to display project details
    st.info("Project details will be displayed here.")

# Create a button to view project tasks
if st.button("View Project Tasks"):
    # Add logic here to display project tasks
    st.info("Project tasks will be displayed here.")

# Create a button to view project timeline
if st.button("View Project Timeline"):
    # Add logic here to display project timeline
    st.info("Project timeline will be displayed here.")

# Add a footer with contact information or additional links
st.markdown(
    """
    ---
    Contact us at [email@example.com](mailto:email@example.com) or visit our website [example.com](http://example.com).
    """
)
