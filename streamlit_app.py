import datetime
import random

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st



# Show app title and description.
st.set_page_config(page_title="IRIS", page_icon="🎫", layout='wide',
                #    initial_sidebar_state=st.session_state.get('sidebar_state', '')
)

st.snow()

# Create a random Pandas dataframe with existing tickets.
if "df" not in st.session_state:

    # Set seed for reproducibility.
    np.random.seed(42)

    # Make up some fake issue descriptions.
    issue_descriptions = [
        "Network connectivity issues in the office",
        "Software application crashing on startup",
        "Printer not responding to print commands",
        "Email server downtime",
        "Data backup failure",
        "Login authentication problems",
        "Website performance degradation",
        "Security vulnerability identified",
        "Hardware malfunction in the server room",
        "Employee unable to access shared files",
        "Database connection failure",
        "Mobile application not syncing data",
        "VoIP phone system issues",
        "VPN connection problems for remote employees",
        "System updates causing compatibility issues",
        "File server running out of storage space",
        "Intrusion detection system alerts",
        "Inventory management system errors",
        "Customer data not loading in CRM",
        "Collaboration tool not sending notifications",
    ]

    # Generate the dataframe with 100 rows/tickets.
    data = {
        "Seller address": np.random.choice(["700", "150", "20"], size=100),
        "Buy amount": np.random.choice(["700", "150", "20"], size=100),      
        "address": [f"email-{i}" for i in range(1100, 1000, -1)],
        "password": [f"password-{i}" for i in range(1100, 1000, -1)],
        "ID": [f"TICKET-{i}" for i in range(1100, 1000, -1)],
        "Issue": np.random.choice(issue_descriptions, size=100),
        "Status": np.random.choice(["Open", "In Progress", "Closed"], size=100),
        "Amount": np.random.choice(["700", "150", "20"], size=100),
        "Date Submitted": [
            datetime.date(2024, 6, 1) + datetime.timedelta(days=random.randint(0, 182))
            for _ in range(100)
        ],
    }
    df = pd.DataFrame(data)

    # Save the dataframe in session state (a dictionary-like object that persists across
    # page runs). This ensures our data is persisted when the app updates.
    st.session_state.df = df

nodes_tab, iristk_tab, accountbal_tab, discussion_tab, tips_tab = \
        st.tabs(["NODES", "IRIS TOKENS", "ACC_BALANCE", "DISCUSSIONS", "TIPS ❄️"])

with nodes_tab:
    node01_tab, node02_tab, node03_tab, nodeo4_tab, node05_tab, node06_tab, node07_tab, node08_tab, node09_tab, node10_tab = st.tabs(["NODE 01", "NODE 02", "NODE 03", "NODE 04", "NODE 05", "NODE 06", "NODE 07", "NODE 08", "NODE 09", "NODE 10"])
with iristk_tab:
    # Show section to view and edit existing tickets in a table.
    st.header("Existing tickets")

    st.info(
    "You can edit the tickets by double clicking on a cell. Note how the plots below "
    "update automatically! You can also sort the table by clicking on the column headers.",
    icon="✍️",
    )

    # Show the tickets dataframe with `st.data_editor`. This lets the user edit the table
    # cells. The edited data is returned as a new dataframe.
    edited_df = st.data_editor(
    st.session_state.df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Status": st.column_config.SelectboxColumn(
            "Status",
            help="Ticket status",
            options=["Open", "In Progress", "Closed"],
            required=True,
        ),
        "Priority": st.column_config.SelectboxColumn(
            "Priority",
            help="Priority",
            options=["High", "Medium", "Low"],
            required=True,
        ),
    },
    # Disable editing the ID and Date Submitted columns.
    disabled=["ID", "Date Submitted"],
)
        
     
with accountbal_tab:

    # Show some metrics and charts about the ticket.
    st.header("Statistics")

    # Show metrics side by side using `st.columns` and `st.metric`.
    col1, col2, col3 = st.columns(3)
    num_open_tickets = len(st.session_state.df[st.session_state.df.Status == "Open"])
    col1.metric(label="Number of open tickets", value=num_open_tickets, delta=10)
    col2.metric(label="First response time (hours)", value=5.2, delta=-1.5)
    col3.metric(label="Average resolution time (hours)", value=16, delta=2)

    # Show two Altair charts using `st.altair_chart`.

    status_plot = (
    alt.Chart(edited_df)
    .mark_bar()
    .encode(
        x="month(Date Submitted):O",
        y="count():Q",
        xOffset="Status:N",
        color="Status:N",
    )
    .configure_legend(
        orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
    )
    )
    st.altair_chart(status_plot, use_container_width=True, theme="streamlit")


    priority_plot = (
        alt.Chart(edited_df)
        .mark_arc()
        .encode(theta="count():Q", color="Priority:N")
        .properties(height=300)
        .configure_legend(
            orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
        )
    )
    st.altair_chart(priority_plot, use_container_width=True, theme="streamlit")

with iristk_tab:

    # Show a section to add a new ticket.
    st.header("Add an offer")

    # We're adding tickets via an `st.form` and some input widgets. If widgets are used
    # in a form, the app will only rerun once the submit button is pressed.
    with st.form("add_offer_form"):
        issue = st.text_area("Offer ID")
        offerType = st.selectbox("Transaction type", ["Buy iris", "Sell iris", "Buy node", "Sell node"])
        amount = st.text_input("Amount of iris tokens")
        submitted = st.form_submit_button("Submit")

    if submitted:
        # Make a dataframe for the new ticket and append it to the dataframe in session
        # state.
        recent_ticket_number = int(max(st.session_state.df.ID).split("-")[1])
        today = datetime.datetime.now().strftime("%m-%d-%Y")
        df_new = pd.DataFrame(
            [
                {
                    "ID": f"TICKET-{recent_ticket_number+1}",
                    "Issue": issue,
                    "Status": "Open",
                    "Amount": amount,
                    "Date Submitted": today,
                }
            ]
        )

        # Show a little success message.
        st.write("Ticket submitted! Here are the ticket details:")
        st.dataframe(df_new, use_container_width=True, hide_index=True)
        st.session_state.df = pd.concat([df_new, st.session_state.df], axis=0)




st.sidebar.title("❄️ Iris ")


with st.sidebar.expander("Log in"):
    form = st.form(key="log_in")
    col1, col2 = form.columns([3,3])
    st.write =('Login')
    address = col1.text_input("Email address",key="address",
    )

    password = col2.text_input("Password",key="password",
    )
    
    form.form_submit_button(label="Submit")
    if submitted:
        df_newlog = pd.DataFrame(
        [
            {
                "address": address,
                "password": password,
                "Date Submitted": datetime.time,
            }
        ]
    )

        # Show a little success message.
        #st.write("Log in successful")
        st.dataframe(df_newlog, use_container_width=True, hide_index=True)
        st.session_state.df = pd.concat([df_newlog, st.session_state.df], axis=0)

