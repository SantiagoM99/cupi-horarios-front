import streamlit as st

def display_availability_table(selected_tab, selected_times, dias, horarios, llaves_turno, asistentes):
    # Dropdown para seleccionar asistente
    selected_assistant = st.selectbox("Selecciona un asistente:", asistentes)
    
    # Convención para los checkboxes
    st.markdown(f"<p class='text'><strong>{llaves_turno[0]}:</strong> Presencial, <strong>{llaves_turno[1]}:</strong> Remoto</p>", unsafe_allow_html=True)
    
    # Encabezados de la grilla
    cols = st.columns(len(dias) + 1)
    cols[0].markdown("<div class='custom-table'><strong>Horario</strong></div>", unsafe_allow_html=True)
    for i, day in enumerate(dias):
        cols[i + 1].markdown(f"<div class='custom-table'><strong>{day}</strong></div>", unsafe_allow_html=True)

    # Construcción de la tabla de disponibilidad con dos checkboxes (P, S)
    for time in horarios:
        cols = st.columns(len(dias) + 1)
        cols[0].markdown(f"<div class='custom-table'>{time}</div>", unsafe_allow_html=True)
        for i, day in enumerate(dias):
            with cols[i + 1]:
                cols_inner = st.columns(2)
                checkbox_id_primary = f"{selected_tab}-{day}-{time}-{llaves_turno[0]}"
                checkbox_id_secondary = f"{selected_tab}-{day}-{time}-{llaves_turno[1]}"
                selected_primary = cols_inner[0].checkbox(llaves_turno[0], value=selected_times[selected_tab][day][time][llaves_turno[0]], key=checkbox_id_primary)
                selected_secondary = cols_inner[1].checkbox(llaves_turno[1], value=selected_times[selected_tab][day][time][llaves_turno[1]], key=checkbox_id_secondary)
                selected_times[selected_tab][day][time][llaves_turno[0]] = selected_primary
                selected_times[selected_tab][day][time][llaves_turno[1]] = selected_secondary
