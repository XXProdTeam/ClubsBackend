from maxapi.types import CallbackButton, ButtonsPayload


hide_text_keyboard = [[CallbackButton(text="Скрыть", payload="hide")]]

hide_text_payload = ButtonsPayload(buttons=hide_text_keyboard).pack()
