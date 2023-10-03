from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


class EventNotifyStates(StatesGroup):
    entering_post = State()
    choosing_time = State()


router = Router()


@router.message(F.text.lower() == 'уведомить о событии')
async def notify_about_event(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        text='Введите текст и приложите фотографии, если требуется',
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.set_state(EventNotifyStates.entering_post)


@router.message(EventNotifyStates.entering_post)
async def entering_post(message: types.Message, state: FSMContext) -> None:
    await state.update_data(event_text=message.text)
    await message.answer('Введите время, когда отослать уведомление, в формате: ')
    await state.set_state(EventNotifyStates.choosing_time)


@router.message(EventNotifyStates.choosing_time)
async def choosing_time(message: types.Message, state: FSMContext) -> None:
    # TODO: Schedule event
    await message.answer('Уведмоление о событии запланировано')
    await state.clear()
