import streamlit as st

from utils import fetch_availability, fetch_time_slots, format_schedule_start_time

def display_availability_table(asistentes, selected_times, dias, horarios, llaves_turno, selected_tab):
    # Track selected assistant in session state
    if 'selected_assistant' not in st.session_state:
        st.session_state.selected_assistant = None

    # Dropdown para seleccionar asistente
    nombres_asistentes = [f"{assistant['first_names']} {assistant['last_names']}" for assistant in asistentes]
    selected_assistant_name = st.selectbox("Selecciona un asistente:", nombres_asistentes)
    
    # Find the selected assistant
    selected_assistant = next((asistente for asistente in asistentes if f"{asistente['first_names']} {asistente['last_names']}" == selected_assistant_name), None)
    
    # Update session state if the selected assistant has changed
    if selected_assistant and st.session_state.selected_assistant != selected_assistant['code']:
        st.session_state.selected_assistant = selected_assistant['code']
        st.session_state.availability_matrix = None  # Force refresh

    # Initialize the matrix if it's not in session state
    if 'availability_matrix' not in st.session_state or st.session_state.availability_matrix is None:
        st.session_state.availability_matrix = {day: {hour: [False, False] for hour in horarios} for day in dias}
    
    # Fetch availability and time slots if the assistant is selected
    if selected_assistant:
        # Fetch de disponibilidad del asistente seleccionado
        availability = fetch_availability(selected_assistant['code'])
        time_slots = fetch_time_slots()

        # Mapeo de ID de time slots a sus detalles
        time_slot_map = {slot['id']: slot for slot in time_slots}
        # Formateo de horas
        start_times = [format_schedule_start_time(horario) for horario in horarios]
        
        # Actualizar la matriz de disponibilidad
        availability_matrix = {day: {hour: [False, False] for hour in start_times} for day in dias}
        for entry in availability:
            time_slot_id = entry['time_slot']['id']
            day = entry['time_slot']['day']
            start_hour = entry['time_slot']['start_hour']
            is_remote = entry['remote_only']
            slot = time_slot_map.get(time_slot_id, None)
            if slot:
                if not is_remote:
                    availability_matrix[day][str(start_hour)][0] = True
                else:
                    availability_matrix[day][str(start_hour)][1] = True

        # Update session state with the new matrix
        st.session_state.availability_matrix = availability_matrix

    # Convención para los checkboxes
    st.markdown(f"<p class='text'><strong>{llaves_turno[0]}:</strong> Presencial, <strong>{llaves_turno[1]}:</strong> Remoto</p>", unsafe_allow_html=True)
    
    # Encabezados de la grilla
    cols = st.columns(len(dias) + 1)
    cols[0].markdown("<div class='custom-table'><strong>Horario</strong></div>", unsafe_allow_html=True)
    for i, day in enumerate(dias):
        cols[i + 1].markdown(f"<div class='custom-table'><strong>{day}</strong></div>", unsafe_allow_html=True)

    # Construcción de la tabla de disponibilidad con dos checkboxes (Presencial, Remoto)
    for index in range(len(horarios)):
        cols = st.columns(len(dias) + 1)
        cols[0].markdown(f"<div class='custom-table'>{horarios[index]}</div>", unsafe_allow_html=True)
        time = start_times[index]
        for i, day in enumerate(dias):
            with cols[i + 1]:
                cols_inner = st.columns(2)
                selected_primary = cols_inner[0].checkbox(llaves_turno[0], value=st.session_state.availability_matrix[day][time][0], key=f"{day}-{time}-{llaves_turno[0]}")
                selected_secondary = cols_inner[1].checkbox(llaves_turno[1], value=st.session_state.availability_matrix[day][time][1], key=f"{day}-{time}-{llaves_turno[1]}")
                selected_times[selected_tab][day][time][llaves_turno[0]] = selected_primary
                selected_times[selected_tab][day][time][llaves_turno[1]] = selected_secondary
