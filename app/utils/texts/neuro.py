from utils.texts.general import html


def menu() -> str:
    text = """Описание доступного функционала в YandexGPT"""
    
    return text


def chat_mode_toggle(active: bool) -> str:
    if active:
        text = f"""Режим сохранения чата включён"""
    else:
        text = f"""Режим сохранения чата выключен"""
        
    return text


def no_subscription_prompts() -> str:
    text = "Для доступа к готовым промптам необходима продвинутая подписка"
    
    return text


def no_subscription_images() -> str:
    text = "Для доступа к генерации изображений необходима продвинутая подписка"
    
    return text


def prompts_menu():
    text = "Выберите готовый промт для начала нового диалога:"
    
    return text
    
    
def new_dialog(prompt: str = None) -> str:
    text = f"""Начат новый диалог
Режим общения: {prompt if prompt else "Обычный"}"""

    return text


def dialog_ended() -> str:
    text = f"Диалог закончен. Пришлите сообщение, чтобы начать новый диалог или отправить отдельный запрос."
    
    return text
    

def get_image_prompt() -> str:
    text = f"Пришлите промпт для генерации изображения"
    
    return text