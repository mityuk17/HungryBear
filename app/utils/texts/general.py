from database.schemas.general import User, Tarif
from datetime import datetime


def html(text) -> str:
    text = str(text)
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text


def start_menu() -> str:
    text = "Добро пожаловать в Telegram-бот проекта <b>Hungry Bear</b>"
    
    return text


def pick_tool_menu() -> str:
    text = "Выберите сервис:"
    
    return text


def user_info(user_data: User) -> str:
    text = f"""Профиль {html(user_data.id)}
<i>Имя:</i> {html(user_data.name)}
$BEAR: {user_data.balance}
Подписка: {user_data.active_subscription()}"""

    if user_data.active_subscription() != Tarif.Free:
        text += f"\nАктивна до: {html(user_data.subsctiption_endtime)}"

    return text


def points_info() -> str:
    text = "Информация о $BEAR"
    
    return text


def get_amount_for_deposit() -> str:
    text = """Введите сумму в Stars, на которую хотите пополнить баланс
❗️1 ⭐️ = 1 $BEAR"""

    return text

def incorrect_amount_for_deposit() -> str:
    text = "Сумма должна быть целым числом"
    
    return text


def successful_payment(amount: int) -> str:
    text = f"Ваш баланс был пополнен на {html(amount)} $BEAR"

    return text


def about_project() -> str:
    text = "О проекте"
    
    return text


def manage_subscription_menu(user_data: User) -> str:
    text = f"""<b>Управление подпиской</b>\n\n"""
    if user_data.active_subscription() == Tarif.Free:
        text += "У вас нет активной подписки"
    else:
        text += f"""Уровень подписки: {user_data.tarif}
Активна до: {html(user_data.subsctiption_endtime)}"""

    text += f"""\nПреимущества подписки:..."""
    
    return text


def insufficient_balance() -> str:
    text = f"У вас недостаточно $BEAR"
    
    return text

def subscription_bought(tarif: str, endtime: datetime) -> str:
    text = f"""{tarif} подписка оформлена.
Активна до: {html(endtime)}"""

    return text


def subscription_autorenewed(tarif: str) -> str:
    text = f"""{tarif} подписка автопродлена на 30 дней."""
    
    return text


def subscription_cancelled(tarif: str) -> str:
    text = f"""{tarif} подписка отменена, так как недостаточно $BEAR для автопродления."""
    
    return text


def subscription_ended(tarif: str) -> str:
    text = f"""{tarif} подписка закончилась."""
    
    return text


def notificate_about_subscription_endtime(user_data: User) -> str:
    text = f"""{user_data.tarif} подписка скоро закончится!
Автопродление <b>{"включено" if user_data.auto_renewal else "отключено"}</b>"""