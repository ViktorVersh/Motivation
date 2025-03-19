from aiogram.fsm.state import StatesGroup, State


class Motiv(StatesGroup):
    new_motiv = State
    create = State