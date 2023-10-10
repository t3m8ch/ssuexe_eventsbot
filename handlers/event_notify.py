from datetime import datetime
from zoneinfo import ZoneInfo

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from models.media_item_model import MediaItemModel
from models.user_model import UserModel
from services.event_service import EventService
from services.user_service import UserService
from utils.media_mappers import map_media_message_to_dict
from utils.menu_kb_gen import generate_menu_kb


class EventNotifyStates(StatesGroup):
    entering_post = State()
    choosing_time = State()


router = Router()


@router.message(F.text.lower() == 'уведомить о событии')
async def notify_about_event(message: types.Message, state: FSMContext, user_service: UserService) -> None:
    user = await user_service.get_user_by_id(message.from_user.id)
    if user.role != 'ADMIN':
        await message.answer('Вы не имеете доступ к этой команде')
        return

    await message.answer(
        text='Введите текст и приложите фотографии, если требуется',
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.set_state(EventNotifyStates.entering_post)


@router.message(EventNotifyStates.entering_post)
async def entering_post(
        message: types.Message,
        album: list[types.Message],
        state: FSMContext,
) -> None:
    if not (message.text or message.caption) and not (message.photo or message.video):
        await message.answer('Вы должны ввести текст или приложить фотографии')
        return

    if message.text:
        await state.update_data(event_text=message.text)
    elif message.caption:
        await state.update_data(event_text=message.caption)
    else:
        await state.update_data(event_text=None)

    await state.update_data(media_items=[map_media_message_to_dict(m) for m in album if m.photo or m.video])

    await message.answer(
        'Введите время по Саратову, когда отослать уведомление, в формате: DD.MM.YY HH:MM\n'
        'Например: 07.10.23 13:40'
    )
    await state.set_state(EventNotifyStates.choosing_time)


@router.message(EventNotifyStates.choosing_time)
async def choosing_time(
        message: types.Message,
        state: FSMContext,
        event_service: EventService,
        user: UserModel,
) -> None:
    state_data = await state.get_data()

    publish_at = datetime.strptime(message.text, '%m.%d.%y %H:%M').replace(tzinfo=ZoneInfo('Europe/Saratov'))
    media_items = [MediaItemModel(file_id=i['file_id'], media_type=i['media_type']) for i in state_data['media_items']]
    text = state_data['event_text']

    await event_service.schedule_event(text=text, media_items=media_items, publish_at=publish_at)

    await message.answer('Уведомление о событии запланировано', reply_markup=generate_menu_kb(user.role))
    await state.clear()
