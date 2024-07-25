import streamlit as st

def display_schedule_table(schedule, dias, horarios):
    # Encabezados de la grilla
    cols = st.columns(len(dias) + 1)
    cols[0].markdown("<div class='custom-table'><strong>Horario</strong></div>", unsafe_allow_html=True)
    for i, day in enumerate(dias):
        cols[i + 1].markdown(f"<div class='custom-table'><strong>{day}</strong></div>", unsafe_allow_html=True)

    # Construcción de la tabla de horarios
    for time in horarios:
        cols = st.columns(len(dias) + 1)
        cols[0].markdown(f"<div class='custom-table'>{time}</div>", unsafe_allow_html=True)
        for i, day in enumerate(dias):
            cell_content = schedule[day][time]
            presenciales = cell_content["Presencial"]
            remotos = cell_content["Remoto"]
            content = ""
            if presenciales:
                content += f"Presencial: {presenciales}<br>"
            if remotos:
                content += f"Remoto: {remotos}"
            st.markdown(f"<div class='custom-table'>{content}</div>", unsafe_allow_html=True)
