import streamlit as st
from utils.fetch_data import load_local_data, fetch_chosen_schedule
from components.option_menu import display_option_menu
from components.schedule_table import display_schedule_table
from components.availability_table import display_availability_table

data = load_local_data('data/data.json')
mock_data = load_local_data('data/mock_data.json')

tipo_turno = data["tipo_turno"]
llaves_turno = data["llaves_turno"]
dias = data["dias"]
horarios = data["horarios"]
asistentes = data["asistentes"]

selected_times = {
    "Horario": {day: {time: ["N", "N"] for time in horarios} for day in dias},
    "Disponibilidad": {day: {time: {llaves_turno[0]: False, llaves_turno[1]: False} for time in horarios} for day in dias}
}

st.markdown("<style>{}</style>".format(open('style/style.css').read()), unsafe_allow_html=True)

final_schedule = fetch_chosen_schedule(mock_data)

schedule = {day: {time: {"Presencial": None, "Remoto": None} for time in horarios} for day in dias}
for entry in final_schedule:
    assistant_code = int(entry["assistant_code"])
    remote_only = entry["remote_only"]
    time_slot_id = entry["time_slot_id"]
    day_index = int(time_slot_id[-1]) % len(dias)
    time_index = int(time_slot_id[-2]) % len(horarios)
    day = dias[day_index]
    time = horarios[time_index]
    tipo = "Remoto" if remote_only else "Presencial"
    schedule[day][time][tipo] = asistentes[assistant_code % len(asistentes)]

st.markdown(f"<h1 class='title'>Cupi-horarios</h1>", unsafe_allow_html=True)

selected_tab = display_option_menu()

if selected_tab == "Horario":
    display_schedule_table(schedule, dias, horarios)

elif selected_tab == "Disponibilidad":
    display_availability_table(selected_tab, selected_times, dias, horarios, llaves_turno, asistentes)

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
