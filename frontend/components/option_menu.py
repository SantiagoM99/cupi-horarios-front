import streamlit as st
from streamlit_option_menu import option_menu

def display_option_menu():
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
    return selected_tab
