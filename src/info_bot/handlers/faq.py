from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

import keyboards.main_menu as keyboard
from worker import manager_faq


router = Router()


@router.callback_query(lambda c: c.data.split("_")[0] == "faq")
async def faq_online_course(callback_query: types.CallbackQuery, state: FSMContext):
    data = manager_faq.get_all(id="_".join(callback_query.data.split("_")[1:]))

    if data is None:
        await callback_query.message.delete()
        await callback_query.message.answer("Тема не найдена", reply_markup=keyboard.back_to_FAQ())
        return

    faq_text = f"Тема: {data.name}\n\n"
    faqs = data.faqs
    for f in faqs:
        faq_text += f"Вопрос: {f.question}\nОтвет: {f.answer}\n\n"

    await callback_query.message.delete()
    await callback_query.message.answer(faq_text, reply_markup=keyboard.back_to_FAQ())
