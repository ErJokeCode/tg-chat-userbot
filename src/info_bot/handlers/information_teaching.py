from aiogram import Router
from aiogram import types
from aiogram.fsm.context import FSMContext

from states import Info_teaching
from keyboards.info_teaching import next_and_back, list_topics
from texts.error import Registration
import texts.information_teaching as text


router = Router()

async def show_info_teaching(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if user_data.get('email') and user_data.get('personal_number'):
        msg = await message.answer("Выбери тему. Можешеь начать с первой и пройти все, чтобы получить азы обучения в ИРИТ РТФ", reply_markup=list_topics(user_data))
        await state.update_data(del_msg = [msg.message_id])
    else:
        await message.delete()
        await message.answer(Registration.no())





@router.callback_query(lambda c: c.data == "cards")
async def cards(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Info_teaching.CARD)

    user_data = await state.get_data()
    del_msg = user_data.get('del_msg')
    await callback_query.message.bot.delete_messages(chat_id=callback_query.message.chat.id, message_ids=del_msg)

    msg_1 = await callback_query.message.answer(text.cards(), reply_markup=next_and_back())
    await state.update_data(del_msg = [msg_1.message_id], cards = True)


@router.callback_query(lambda c: c.data == "auditoria")
async def auditoria(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Info_teaching.NUMBER_ROOM)

    user_data = await state.get_data()
    del_msg = user_data.get('del_msg')
    await callback_query.message.bot.delete_messages(chat_id=callback_query.message.chat.id, message_ids=del_msg)

    msg_2 = await callback_query.message.answer(text.auditoria(), reply_markup=next_and_back())
    await state.update_data(del_msg = [ msg_2.message_id], auditoria = True)


@router.callback_query(lambda c: c.data == "navigator")
async def navigator(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Info_teaching.NAVIGATOR)

    user_data = await state.get_data()
    del_msg = user_data.get('del_msg')
    await callback_query.message.bot.delete_messages(chat_id=callback_query.message.chat.id, message_ids=del_msg)
    
    msg_2 = await callback_query.message.answer(text.navigator(), reply_markup=next_and_back())
    await state.update_data(del_msg = [msg_2.message_id], navigator = True)


@router.callback_query(lambda c: c.data == "lk_student")
async def lk_student(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Info_teaching.LK_URFU)

    user_data = await state.get_data()
    del_msg = user_data.get('del_msg')
    await callback_query.message.bot.delete_messages(chat_id=callback_query.message.chat.id, message_ids=del_msg)
    
    msg_2 = await callback_query.message.answer(text.lk_student(), reply_markup=next_and_back())
    await state.update_data(del_msg = [msg_2.message_id], lk_student = True)


@router.callback_query(lambda c: c.data == "online_course_all_info")
async def online_course_all_info(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Info_teaching.ONLINE_COURSE)

    user_data = await state.get_data()
    del_msg = user_data.get('del_msg')
    await callback_query.message.bot.delete_messages(chat_id=callback_query.message.chat.id, message_ids=del_msg)
    
    msg_2 = await callback_query.message.answer(text.online_course_all_info(), reply_markup=next_and_back())
    await state.update_data(del_msg = [msg_2.message_id], online_course_all_info=True)


@router.callback_query(lambda c: c.data == "rating")
async def rating(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Info_teaching.REITING)

    user_data = await state.get_data()
    del_msg = user_data.get('del_msg')
    await callback_query.message.bot.delete_messages(chat_id=callback_query.message.chat.id, message_ids=del_msg)
    
    msg_2 = await callback_query.message.answer(text.rating(), reply_markup=next_and_back(next=False))
    await state.update_data(del_msg = [msg_2.message_id], rating = True)





@router.callback_query(lambda c: c.data == "next_topic")
async def next_topic(callback_query: types.CallbackQuery, state: FSMContext):
    last_state = await state.get_state()

    if last_state == Info_teaching.CARD:
        await auditoria(callback_query, state)
    elif last_state == Info_teaching.NUMBER_ROOM:
        await navigator(callback_query, state)
    elif last_state == Info_teaching.NAVIGATOR:
        await lk_student(callback_query, state)
    elif last_state == Info_teaching.LK_URFU:
        await online_course_all_info(callback_query, state)
    elif last_state == Info_teaching.ONLINE_COURSE:
        await rating(callback_query, state)


@router.callback_query(lambda c: c.data == "back_to_topics")
async def back_to_topic(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    del_msg = user_data.get('del_msg')
    await state.set_state(Info_teaching.INFO)

    await callback_query.message.bot.delete_messages(chat_id=callback_query.message.chat.id, message_ids=del_msg)
    await show_info_teaching(callback_query.message, state)