import streamlit as st
import pandas as pd
from datetime import datetime


def display_schedule_table(schedule, horarios, dias):
    # Extract the scheduled slots
    scheduled_slots = schedule['scheduled_slots'] 
    
    # Create a list of rows to display in the table
    rows = []
    
    # Iterate over the schedule and add each two entries as a row
    for i in range(0, len(scheduled_slots), 2):
        entry1 = scheduled_slots[i]
        entry2 = scheduled_slots[i + 1]
        
        # Get the assistant nicknames
        assistant1 = entry1['assistant_availability']["assistant"]["nickname"]
        assistant2 = entry2['assistant_availability']["assistant"]["nickname"]
        
        # Calculate the time slot and day
        time_slot = horarios[i // 2 % len(horarios)]
        day = dias[i // 2 % len(dias)]
        
        # Add the row to the list
        rows.append({
            'Day': day,
            'Time_Slot': time_slot,
            'Presencial': f'P: {assistant1}',
            'Remoto': f'R: {assistant2}',
            'Start_Time': entry1['assistant_availability']['time_slot']['start_hour']
        })
    
    # Create a DataFrame from the rows
    df = pd.DataFrame(rows)

    # Sort the DataFrame by 'Time Slot' and 'Day'
    df['Day'] = pd.Categorical(df['Day'], categories=['MONDAY', 'TUESDAY', 'WEDNESDAY','THURSDAY','FRIDAY','SATURDAY','SUNDAY'], ordered=True)
    df.sort_values(by=['Day', 'Time_Slot'], inplace=True)
    # Drop the intermediate 'Time Slot' column and keep the combined names
    df['Combined'] = df['Presencial'] + ' \n ' + df['Remoto']
    df.drop(columns=['Presencial', 'Remoto'], inplace=True)
    
    # Pivot the DataFrame to create a matrix with days as columns and time slots as rows
    pivot_df = df.pivot(index='Time_Slot', columns='Day', values='Combined')
    
    # Render the pivot table in Streamlit
    st.write("### Schedule Matrix")
    st.dataframe(pivot_df)

    # Optionally, convert it to HTML and return if needed
    return pivot_df.to_html()
