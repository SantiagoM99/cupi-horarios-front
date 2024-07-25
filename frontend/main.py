import streamlit as st
from streamlit_option_menu import option_menu
from frontend.components.option_menu import show_navbar
from frontend.components.schedule_table import show_horario_table
from frontend.components.availability_table import show_disponibilidad_table
from utils.fetch_data import fetch_availabilities
import json

# Configuración inicial
st.markdown("<style>{}</style>".format(open('style/style.css').read()), unsafe_allow_html=True)
# Cargar el CSS
st.markdown('<link rel="stylesheet" href="style/style.css">', unsafe_allow_html=True)
# Mostrar la barra de navegación
show_navbar()

# Función para mostrar el título principal
def show_title():
    st.markdown("<h1 class='title'>Cupi-horarios</h1>", unsafe_allow_html=True)

# Datos
availabilities = fetch_availabilities()
# Procesar los datos para la tabla de horarios
schedule = {}
for entry in availabilities:
    assistant_code = entry["assistant_code"]
    remote_only = entry["remote_only"]
    time_slot_id = entry["time_slot_id"]
    day_index = int(time_slot_id[-1]) % len(dias)  # Asignación simulada para los días
    time_index = int(time_slot_id[-2]) % len(horarios)  # Asignación simulada para los horarios
    day = dias[day_index]
    time = horarios[time_index]
    tipo = "Remoto" if remote_only else "Presencial"
    schedule.setdefault(day, {}).setdefault(time, {"Presencial": None, "Remoto": None})
    schedule[day][time][tipo] = asistentes[assistant_code % len(asistentes)]

# Interfaz de usuario
def main():
    show_title()
    
    selected_tab = option_menu(
        menu_title=None,
        options=["Horario", "Disponibilidad"],
        icons=["calendar", "check-circle"],
        orientation="horizontal",
        styles={
            "nav-link-selected": {"background-color": "#3B41C9", "color": "#f8f7ff"},
            "nav-link": {"color": "#465157"}
        }
    )

    if selected_tab == "Horario":
        show_horario_table(schedule)
    elif selected_tab == "Disponibilidad":
        show_disponibilidad_table()

    # Botón para guardar la selección
    st.markdown("<div style='text-align: center; margin-top: 20px;'>", unsafe_allow_html=True)
    if st.button("Guardar"):
        st.markdown(f"<h2 class='subtitle'>Seleccionaste las siguientes franjas horarias para {selected_tab}:</h2>", unsafe_allow_html=True)
        if selected_tab == "Horario":
            for day, times in selected_times[selected_tab].items():
                selected_slots = [f"{time}: {', '.join(t)}" for time, t in times.items() if any(x != 'N' for x in t)]
                if selected_slots:
                    st.markdown(f"<p class='text'><strong>{day}:</strong> {', '.join(selected_slots)}</p>", unsafe_allow_html=True)
        elif selected_tab == "Disponibilidad":
            for day, times in selected_times[selected_tab].items():
                for time, modes in times.items():
                    selected_modes = [mode for mode, selected in modes.items() if selected]
                    if selected_modes:
                        st.markdown(f"<p class='text'><strong>{day} - {time}:</strong> {', '.join(selected_modes)}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
