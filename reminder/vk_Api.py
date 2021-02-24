import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from datetime import datetime
import requests.exceptions

from random import randint
import time

class Memory:

    def __init__(self):
        self.file = "My_Memory.txt"

    def write_new_note(self, note):
        # добавить обработка записи
        with open(self.file, 'a') as f:
            f.write("{} to do {}\n".format(datetime.now().strftime("%d %B %Y"), note))

    def clear(self):
        with open(self.file, "w") as f:
            return "Notes are clear"

    def show_all(self):
        with open(self.file, 'r') as f:
            return [note for note in f.readlines()]

    def delete_note(self, index):
        self.show_all().pop(index + 1)
        return "deleted complete"

    def logError(self, message: str):
        with open(self.important, "a") as f:
            f.write(message)



class Bot(Memory):
    def __init__(self):
        super().__init__()
        self.token = "{your token}"
        self.vk_session = vk_api.VkApi(token=self.token)
        self.longpoll = VkLongPoll(self.vk_session)
        self.VK = self.vk_session.get_api()
        self.vkKeyboard = VkKeyboard(one_time=True)
        self.vkKeyboard.add_button("Напомнить", color=VkKeyboardColor.POSITIVE)

        # main loop
        while (True):
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW:
                    if event.to_me:
                        message = str(event.text.lower())
                        user_id = event.user_id
                        if message == "удалить":
                            self.write_msg(user_id, self.clear())
                        elif message == "напомнить":
                            ans = " ".join(self.show_all())
                            if len(ans) > 0:
                                self.write_msg(user_id, ans)
                            else:
                                self.write_msg(user_id, "Заметок нет")
                        else:
                            self.write_msg(user_id, "Заметка записана")
                            self.write_new_note(str(message))

    def write_msg(self, user_id=0, message=''):
        try:
            self.VK.messages.send(
                user_id=user_id,
                message=message,
                keyboard=self.vkKeyboard.get_keyboard(),
                random_id=randint(1, 999999),
                verify=False
            )
        except Exception as e:
            self.logError(str(e))
            self.write_msg(user_id, message)


if __name__ == "__main__":
    try:
        Bot()
    except  requests.exceptions.ReadTimeout():
        time.sleep(600)
        Bot()
    except Exception as error:
        Bot().logError(str(error)+"\n")
