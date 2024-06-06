
import streamlit as st
from PIL import Image
import pandas as pd
import altair as alt
import requests
import io
import plotly.express as px



@st.cache_data
def load_data(filename, sheet_name=None):
    """Load data from a specific sheet within an Excel file or a CSV file."""
    path = f"data/{filename}"
    try:
        if filename.endswith('.xlsx'):
            if sheet_name:
                return pd.read_excel(path, sheet_name=sheet_name)
            else:
                return pd.read_excel(path)
        elif filename.endswith('.csv'):
            return pd.read_csv(path)
    except FileNotFoundError:
        st.error(f"Error: The file {filename} does not exist in the data directory.")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading the file: {e}")
        return None
    

def send_message(name, email, message):
    url = "https://formspree.io/f/xqkrogby"  # Replace 'YOUR_FORM_ID' with your actual Formspree endpoint
    data = {
        'name': name,
        'email': email,
        'message': message
    }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.post(url, json=data, headers=headers)
    return response

# Set page configuration
st.set_page_config(page_title="NHS Theatre Utilisation", layout="wide")

# Load and display the logo at the top of the sidebar
try:
    logo = Image.open("Images/navigation.png")
    st.sidebar.image(logo, use_column_width=True)
except Exception as e:
    st.sidebar.write("Error loading logo: ", e)







analysis_descriptions = {
    "Cases_by_Treatment_and_Case_Type": "This analysis shows how cases are distributed across different treatment types and case categories, providing insight into the focus areas of healthcare services.",
    "Cases_by_Procedure_and_Case_Type": "This analysis details the number of cases for each procedure, categorized by case type.",
    "Top_20_Elective_Procedures_by_Cases": "List of the top 20 elective procedures ranked by the number of cases, highlighting the most frequently performed elective surgeries.",
    "Average_Surgery_Duration_by_Procedure": "Analyzes the average duration of surgeries across different procedures, focusing on elective surgeries.",
    "Top_10_Procedures_Longest_Duration": "Identifies the top 10 procedures with the longest average surgery times.",
    "Top_10_Procedures_Shortest_Duration": "Shows the procedures that have the shortest average surgery times, allowing for quick patient turnover.",
    "Top_10_Consultants_Most_Late_Starts": "Highlights the top 10 consultants with the most frequent late starts, indicating potential areas for efficiency improvement.",
    "Top_5_Theatres_Most_Late_Starts": "Details which 5 theatres have the most late starts, which may indicate logistical or operational challenges.",
    "Theatre_Most_Early_Finishes": "Identifies the theatre with the most early finishes, potentially indicating better than expected operational efficiency.",
    "Potential_Income_Top_10_Efficient_Ophthalmology_Procedures": "Estimates potential income increases if the top 3 most efficient ophthalmology procedures were performed more frequently."
}


# Dictionary for SQL queries
sql_queries = {
    "Cases_by_Treatment_and_Case_Type": """
        -----   calculating the number of cases by Treatment Function and Case Type ----
        SELECT 
            TreatmentFunction,  
            CaseType,           
            COUNT(*) AS NumberOfCases  
        FROM 
            Business_Analyst_Test_Theatre_Cases  
        GROUP BY 
            TreatmentFunction, 
            CaseType
        ORDER BY 
            TreatmentFunction, 
            CaseType;
    """,
    "Cases_by_Procedure_and_Case_Type": """
        --  calculating the number of cases by Procedure Name and Case Type  --
        SELECT 
            ProcedureName,  
            CaseType,       
            COUNT(*) AS NumberOfCases  
        FROM 
            Business_Analyst_Test_Theatre_Cases 
        GROUP BY 
            ProcedureName, 
            CaseType
        ORDER BY 
            ProcedureName, 
            CaseType;

    """,
    "Top_20_Elective_Procedures_by_Cases": """
        ---   finding the top 20 elective procedures by number of cases   ---

        SELECT TOP 20
            ProcedureName,
            COUNT(*) AS NumberOfCases
        FROM 
            Business_Analyst_Test_Theatre_Cases
        WHERE 
            CaseType = 'Elective'
        GROUP BY 
            ProcedureName
        ORDER BY 
            NumberOfCases DESC;
    """,
    "Average_Surgery_Duration_by_Procedure": """
        -- calculating the average duration of surgery for elective procedures

        SELECT 
            ProcedureName,
            AVG(DurationOfSurgeryMinutes) AS AverageDuration  
        FROM 
            Business_Analyst_Test_Theatre_Cases
        WHERE 
            CaseType = 'Elective' 
        GROUP BY 
            ProcedureName
        ORDER BY 
            AverageDuration DESC;
    """,
    "Top_10_Procedures_Longest_Duration": """
        ---   finding the top 10 procedures with the longest average duration ----

        SELECT TOP 10
            ProcedureName,
            AVG(DurationOfSurgeryMinutes) AS AverageDuration
        FROM 
            Business_Analyst_Test_Theatre_Cases
        WHERE 
            CaseType = 'Elective'
        GROUP BY 
            ProcedureName
        ORDER BY 
            AverageDuration DESC;
    """,
    "Top_10_Procedures_Shortest_Duration": """
            ---- finding the top 10 procedures with the shortest average duration  ---

            SELECT TOP 10
                ProcedureName,
                AVG(DurationOfSurgeryMinutes) AS AverageDuration
            FROM 
                Business_Analyst_Test_Theatre_Cases
            WHERE 
                CaseType = 'Elective'
            GROUP BY 
                ProcedureName
            ORDER BY 
                AverageDuration ASC;
    """,
    "Top_10_Consultants_Most_Late_Starts": """
        -- finding the top 10 consultants with the most late starts --

        SELECT TOP 10
            Consultant,
            COUNT(*) AS LateStarts
        FROM Business_Analyst_Test_Theatre_Cases
        WHERE CaseType = 'Elective' AND TreatmentFunction = 'Ophthalmology' AND LateStart = 1
        GROUP BY Consultant
        ORDER BY LateStarts DESC;
    """,
    "Top_5_Theatres_Most_Late_Starts": """
        ---  theatres with the most late starts   ----
        SELECT TOP 5
            TheatreName,
            COUNT(*) AS LateStarts
        FROM Business_Analyst_Test_Theatre_Cases
        WHERE CaseType = 'Elective' AND TreatmentFunction = 'Ophthalmology' AND LateStart = 1
        GROUP BY TheatreName
        ORDER BY LateStarts DESC;
    """,
    "Theatre_Most_Early_Finishes": """
        ---  the theatre with the most early finishes   ---

        SELECT TOP 4
            TheatreName,
            COUNT(*) AS EarlyFinishes
        FROM Business_Analyst_Test_Theatre_Cases
        WHERE CaseType = 'Elective' AND TreatmentFunction = 'Ophthalmology' AND EarlyFinish = 1
        GROUP BY TheatreName
        ORDER BY EarlyFinishes DESC;
    """,
    "Potential_Income_Top_10_Efficient_Ophthalmology_Procedures": """
         ---   calculate potential income for the top five efficient Ophthalmology procedures ---
        SELECT
            a.ProcedureName,
            b.Income,
            a.AverageDuration
        FROM
            (SELECT TOP 10
                ProcedureName,
                AVG(DurationOfSurgeryMinutes) AS AverageDuration
            FROM
                Business_Analyst_Test_Theatre_Cases
            WHERE
                CaseType = 'Elective' AND TreatmentFunction = 'Ophthalmology'
            GROUP BY
                ProcedureName
            ORDER BY
                AverageDuration ASC) a
        JOIN
            NHS_Biz_Ophthalmology_Income b ON a.ProcedureName = b.Procedure_Name;
    """,
    # Add more queries here
}



# Main navigation with expanders
# Persistent state setup
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'Home'

# Navigation setup with session state
with st.sidebar:
    st.title('Navigation')
    if st.button('Home'):
        st.session_state.current_page = "Home"
    if st.button('Dashboard'):
        st.session_state.current_page = "Dashboard"
    with st.expander("SQL Analysis"):
        analysis_options = list(analysis_descriptions.keys())
        st.session_state.selected_analysis = st.selectbox(
            "Choose an analysis to view", 
            analysis_options, 
            key='analysis_select'
        )
        if st.button('Analyze'):
            st.session_state.current_page = "SQL Analysis"
    with st.expander("Data"):
        data_page_options = ["Raw Data", "Ophthalmology Income"]
        st.session_state.selected_data = st.radio("Data Sheets", data_page_options, key='data_select')
        if st.button('Show Data'):
            st.session_state.current_page = "Data"
    
    if st.button('Contact'):
        st.session_state.current_page = "Contact"

# Loading data from specific sheets
raw_data = load_data('NHS_Trust_Theatre_Utilisation_Efficiency_Dashboard.xlsx', 'Raw Data')
ophthalmology_income = load_data('NHS_Trust_Theatre_Utilisation_Efficiency_Dashboard.xlsx', 'Ophthalmology Income')




# Conditional rendering based on navigation selection
if st.session_state.current_page == "Home":
    st.title('Theatre Utilisation Dashboard')
    st.image("Images/Homebanner1.png", use_column_width=True)
    st.markdown('''
#### Overview
Welcome to the Theatre Utilisation Dashboard, a sophisticated tool designed to enhance operational efficiency in surgical environments. This system leverages advanced data processing technologies to provide deep insights into theatre operations, supporting strategic planning and resource management.

#### Project Genesis
This initiative transforms complex healthcare data into actionable insights through a fully automated data pipeline. Utilizing cutting-edge technologies such as Azure Data Factory, Azure Databricks, and SQL Server, the data—sourced from the National Health Service (NHS) via public health databases—undergoes thorough processing to ensure its accuracy and relevance.

#### Features
- **Dynamic Data Visualizations**: Engage with interactive charts and graphs to explore operational metrics including case types, procedure efficiencies, and consultant performance.
- **Advanced SQL Analysis**: Delve into underlying patterns and trends with detailed SQL queries.
- **Real-Time Data Integration**: Automated updates ensure the dashboard remains current, reflecting the latest operational metrics.

#### Data Transparency
Data for this dashboard is derived from publicly available sources provided by the NHS, ensuring transparency and ethical usage. The handling and processing of this data are carried out with the utmost care to preserve its integrity and confidentiality.

#### Usage
Use the sidebar to navigate through various sections of the dashboard, from dynamic views to in-depth SQL analyses and raw data sheets. Each component is designed to provide tailored information that supports informed decision-making.

#### Aim
The aim of this project is to establish an automated system that equips healthcare administrators and operational managers with robust, data-driven tools that improve decision-making, enhance resource allocation, and boost operational outcomes in healthcare settings.

#### Note
This project is an independent initiative that uses publicly available NHS data. It is not developed by, nor affiliated with, the NHS or any related government body.
''', unsafe_allow_html=True)


elif st.session_state.current_page == "Dashboard":
    st.title('Theatre Utilisation Efficiency Dashboard')

    # Ensuring 'Income' column is cleaned and converted to numeric
    ophthalmology_income['Income'] = ophthalmology_income['Income'].replace('[£,]', '', regex=True).astype(float)

    # Slicers for Case Type and Treatment Function
    case_types = raw_data['CaseType'].unique()
    treatment_functions = raw_data['TreatmentFunction'].unique()

    selected_case_types = st.multiselect('Filter by Case Type:', options=case_types, default=case_types)
    selected_treatment_functions = st.multiselect('Filter by Treatment Function:', options=treatment_functions, default=treatment_functions)

    # Applying filters
    filtered_data = raw_data[(raw_data['CaseType'].isin(selected_case_types)) &
                             (raw_data['TreatmentFunction'].isin(selected_treatment_functions))]

    if filtered_data.empty:
        st.error("No data matches your filters.")
    else:
        # Calculate metrics
        total_cases = filtered_data['BKCaseNo'].nunique()
        total_surgery_minutes = filtered_data['DurationOfSurgeryMinutes'].sum()
        total_procedures_income = ophthalmology_income[ophthalmology_income['Procedure_Name'].isin(filtered_data['ProcedureName'].unique())]['Income'].sum()
        top_10_procedures_income = ophthalmology_income[ophthalmology_income['Procedure_Name'].isin(filtered_data['ProcedureName'].unique())].nlargest(10, 'Income')['Income'].sum()

        # Format numbers with thousand separators
        formatted_total_cases = f"{total_cases:,}"
        formatted_total_surgery_minutes = f"{total_surgery_minutes:,}" 

        # Display metrics using columns
        metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
        metrics_col1.metric("Total Cases", formatted_total_cases)
        metrics_col2.metric("Total Surgery Minutes", formatted_total_surgery_minutes)
        metrics_col3.metric("Total Procedures Income", f"£{total_procedures_income:,.2f}")
        metrics_col4.metric("Top 10 Procedures Income", f"£{top_10_procedures_income:,.2f}")

        # Creating two columns for more detailed analytics and data presentation
        metrics_col1, metrics_col2 = st.columns(2)

        with metrics_col1:
            st.subheader('Case Distribution by Treatment Function and Case Type')
            pivot_data = filtered_data.groupby(['TreatmentFunction', 'CaseType'])['BKCaseNo'].nunique().unstack().fillna(0)
            pivot_data = pivot_data.astype(int)  # Convert to integer to remove decimal places
            st.dataframe(pivot_data.style.format("{:.0f}").background_gradient(cmap='viridis'))

            st.subheader("Top 10 Longest Average Procedure Times (Elective)")
            elective_data = filtered_data[filtered_data['CaseType'] == 'Elective']
            avg_times_longest = elective_data.groupby('ProcedureName')['DurationOfSurgeryMinutes'].mean().nlargest(10).reset_index()
            avg_times_longest['DurationOfSurgeryMinutes'] = avg_times_longest['DurationOfSurgeryMinutes'].round(2)
            st.dataframe(avg_times_longest.style.format({"DurationOfSurgeryMinutes": "{:.2f}"}).background_gradient(cmap='coolwarm'))

        with metrics_col2:
            st.subheader('Number of Cases by Procedure')
            procedure_pivot_data = filtered_data.groupby('ProcedureName')['BKCaseNo'].nunique().reset_index(name='CaseCount').sort_values('CaseCount', ascending=False)
            st.dataframe(procedure_pivot_data.style.background_gradient(cmap='magma'))

            st.subheader("Top 10 Shortest Average Procedure Times (Elective)")
            avg_times_shortest = elective_data.groupby('ProcedureName')['DurationOfSurgeryMinutes'].mean().nsmallest(10).reset_index()
            avg_times_shortest['DurationOfSurgeryMinutes'] = avg_times_shortest['DurationOfSurgeryMinutes'].round(2)
            st.dataframe(avg_times_shortest.style.format({"DurationOfSurgeryMinutes": "{:.2f}"}).background_gradient(cmap='coolwarm'))

        
        metrics_col1, metrics_col2 = st.columns(2)
        with metrics_col1:
            st.subheader('Top 5 Ophthalmology Consultants That Could Be Doing More')
            oph_data = filtered_data[filtered_data['TreatmentFunction'] == 'Ophthalmology']
            consultant_performance = oph_data.groupby('Consultant')['DurationOfSurgeryMinutes'].mean().reset_index()
            top_consultants = consultant_performance.nsmallest(5, 'DurationOfSurgeryMinutes')
            consultant_chart = alt.Chart(top_consultants).mark_bar(color='indigo').encode(
                x=alt.X('Consultant:N', sort='-y', title='Consultant', axis=alt.Axis(titleFontWeight='bold')),
                y=alt.Y('DurationOfSurgeryMinutes:Q', title='Average Surgery Duration (minutes)', axis=alt.Axis(titleFontWeight='bold')),
                tooltip=[alt.Tooltip('Consultant:N'), alt.Tooltip('DurationOfSurgeryMinutes:Q', title='Avg Duration')]
            ).properties(
                title='Top 5 Efficient Ophthalmology Consultants by Surgery Time'
            )
            text = consultant_chart.mark_text(
                align='center',
                baseline='bottom',
                dy=-5,  # Adjusting dy to position labels above bars
                color='white',
                fontWeight='bold',
                fontSize=12
            ).encode(
                text=alt.Text('DurationOfSurgeryMinutes:Q', format='.1f')
            )
            st.altair_chart(consultant_chart + text, use_container_width=True)

        with metrics_col2:
            st.subheader('Top 5 Best General Performing Consultants by Lowest Average Surgery Duration')

            # Group by 'Consultant', calculating the mean surgery duration, and reset the index for plotting
            consultant_performance = filtered_data.groupby('Consultant')['DurationOfSurgeryMinutes'].mean().reset_index()

            # Select the top 5 consultants with the smallest average surgery duration
            top_consultants = consultant_performance.nsmallest(5, 'DurationOfSurgeryMinutes')

            # Create a bar chart using Altair
            consultant_chart = alt.Chart(top_consultants).mark_bar(color='lightblue').encode(
                x=alt.X('Consultant:N', title='Consultant', axis=alt.Axis(titleFontWeight='bold')),
                y=alt.Y('DurationOfSurgeryMinutes:Q', title='Average Surgery Duration (minutes)', axis=alt.Axis(titleFontWeight='bold'),
                        sort=alt.EncodingSortField(field='DurationOfSurgeryMinutes', order='ascending')),  # Ensure ascending sort
                tooltip=[alt.Tooltip('Consultant:N'), alt.Tooltip('DurationOfSurgeryMinutes:Q', title='Avg Duration')]
            ).properties(
                title='Top 5 Best Performing Consultants by Surgery Time'
            )

            # Add text labels on top of the bars for better visibility of values
            text = consultant_chart.mark_text(
                align='center',
                baseline='bottom',
                dy=-5,  # Adjust position to display above the bars
                color='white',
                fontWeight='bold',
                fontSize=12
            ).encode(
                text=alt.Text('DurationOfSurgeryMinutes:Q', format='.1f')  # Formating with one decimal place
            )

            # Display the combined chart and text in Streamlit
            st.altair_chart(consultant_chart + text, use_container_width=True)


        # Dynamic DataFrames and Charts
        left_col, center_col, right_col = st.columns(3)

        with left_col:
            st.subheader('Consultant Efficiency Analysis')
            consultant_efficiency = filtered_data.groupby('Consultant').agg({'DurationOfSurgeryMinutes': ['mean', 'count']}).reset_index()
            consultant_efficiency.columns = ['Consultant', 'Average Surgery Duration', 'Number of Cases']
            consultant_chart = alt.Chart(consultant_efficiency).mark_bar().encode(
                x=alt.X('Number of Cases:Q'),
                y=alt.Y('Consultant:N', sort='-x'),
                color=alt.Color('Average Surgery Duration:Q', scale=alt.Scale(scheme='redblue')),
                tooltip=['Consultant', 'Number of Cases', 'Average Surgery Duration']
            ).properties(height=300)
            st.altair_chart(consultant_chart, use_container_width=True)

            st.subheader('Top 10 Procedures with Highest Average of DurationOfSurgeryMinutes')
            top_procedures = filtered_data.groupby('ProcedureName')['DurationOfSurgeryMinutes'].mean().nlargest(10).reset_index()
            st.dataframe(top_procedures)

        with center_col:
            st.subheader('Consultant Performance Analysis')
            consultant_performance = filtered_data.groupby('Consultant').agg({'DurationOfSurgeryMinutes': ['mean', 'count']}).nlargest(20, ('DurationOfSurgeryMinutes', 'mean'))
            st.dataframe(consultant_performance.style.format({"mean": "{:.2f}"}).background_gradient(cmap='magma'))

            st.subheader('Procedure Count')
            procedure_counts = filtered_data['ProcedureName'].value_counts().head(5).reset_index()
            procedure_counts.columns = ['ProcedureName', 'Count']

            # Create bar chart
            procedure_chart = alt.Chart(procedure_counts).mark_bar(color='steelblue').encode(
                x=alt.X('ProcedureName:N', sort='-y', title='Procedure Name'),
                y=alt.Y('Count:Q', title='Count'),
                tooltip=[alt.Tooltip('ProcedureName:N'), alt.Tooltip('Count:Q')]
            ).properties(
                height=400,
                width=alt.Step(80)  # Controls the width of the bars
            )

            # Add text labels on top of the bars
            text = procedure_chart.mark_text(
                align='center',
                baseline='bottom',
                dy=-5,  # Adjust dy to position labels above bars
                color='white',
                fontWeight='bold',
                fontSize=12
            ).encode(
                text=alt.Text('Count:Q', format=',')  # Using ',' as a thousand separator
            )

            # Combine the chart and the text
            st.altair_chart(procedure_chart + text, use_container_width=True)

        with right_col:
            st.subheader('Top 20 Income by Procedure')
            procedure_income = ophthalmology_income[ophthalmology_income['Procedure_Name'].isin(filtered_data['ProcedureName'].unique())]
            top_income = procedure_income.nlargest(20, 'Income')[['Procedure_Name', 'Income']]

            # Format the Income column to include a pound sign and limit to one decimal place
            formatted_income = top_income.style.format({
                'Income': '£{:.1f}'
            })
            st.dataframe(formatted_income)


            st.subheader('Top 5 Best performing Procedures by Lowest DurationOfSurgeryMinutes average')
            top_procedures = filtered_data.groupby('ProcedureName')['DurationOfSurgeryMinutes'].mean().nsmallest(5).reset_index()
            #st.dataframe(top_procedures)
            # Create an Altair chart object
            top_procedures_chart = alt.Chart(top_procedures).mark_bar(color='cadetblue').encode(
                x=alt.X('ProcedureName:N', title='Procedure Name', sort=alt.EncodingSortField(field='DurationOfSurgeryMinutes', order='ascending')),  # Sorting based on Duration
                y=alt.Y('DurationOfSurgeryMinutes:Q', title='Average Duration (minutes)'),
                tooltip=[alt.Tooltip('ProcedureName:N'), alt.Tooltip('DurationOfSurgeryMinutes:Q', title='Avg Duration', format='.2f')]
            ).properties(
                height=400
            )

            # Add text labels on top of the bars
            text = top_procedures_chart.mark_text(
                align='center',
                baseline='bottom',
                dy=-5,  # Adjust dy to position labels above bars
                color='white',
                fontWeight='bold',
                fontSize=12
            ).encode(
                text=alt.Text('DurationOfSurgeryMinutes:Q', format='.1f')
            )

            # Display the chart
            st.altair_chart(top_procedures_chart + text, use_container_width=True)


        # Clear Filters button
        if st.button('Clear Filters'):
            st.experimental_rerun()

     

elif st.session_state.current_page == "SQL Analysis":
    st.title('Detailed SQL Analysis')
    if st.session_state.selected_analysis:
        description = analysis_descriptions.get(st.session_state.selected_analysis, "No description available for this analysis.")
        sql_query = sql_queries.get(st.session_state.selected_analysis, "No SQL query available for this analysis.")
        
        st.subheader(st.session_state.selected_analysis)
        st.markdown(f"**Description**: {description}")
        st.code(sql_query, language='sql')  # Display the SQL query
        
        if st.button('Run Analysis'):
            data_filename = st.session_state.selected_analysis.replace(" ", "_") + '.csv'
            data = load_data(data_filename)
            if data is not None:
                st.dataframe(data)
            else:
                st.error("Failed to load data for the selected analysis.")
    else:
        st.info("Please select an analysis from the dropdown above and click 'Run Analysis' to view results.")




elif st.session_state.current_page == "Data":
    data_page = st.session_state.selected_data
    if data_page == "Raw Data":
        st.title("Raw Data")
        data = load_data('NHS_Trust_Theatre_Utilisation_Efficiency_Dashboard.xlsx', 'Raw Data')
    elif data_page == "Ophthalmology Income":
        st.title("Ophthalmology Income")
        data = load_data('NHS_Trust_Theatre_Utilisation_Efficiency_Dashboard.xlsx', 'Ophthalmology Income')

    if data is not None:
        st.dataframe(data)
    else:
        st.error("Failed to load the selected dataset.")



# Main content based on navigation
elif st.session_state.current_page == "Contact":
    st.title("Contact Me")
    with st.form("contact_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        message = st.text_area("Message")
        submit_button = st.form_submit_button("Send Message")

        if submit_button:
            response = send_message(name, email, message)
            if response.status_code == 200:
                st.success("Thank you for your message! I will get back to you soon.")
            else:
                st.error("An error occurred while sending your message.")



# Add any additional styling directly related to the app-wide
