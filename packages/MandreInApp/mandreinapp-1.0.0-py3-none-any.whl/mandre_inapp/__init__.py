
from java import dynamic_proxy
from java.lang import Runnable
from android.graphics.drawable import BitmapDrawable
from android.text import TextUtils
from android.util import TypedValue
from org.telegram.messenger import AndroidUtilities, ImageLocation, R
from org.telegram.ui.Components import BulletinFactory, Bulletin
from org.telegram.ui.ActionBar import Theme
from org.telegram.tgnet import TLRPC

# Попытка импорта утилит Mandre/Client. 
# Если библиотека запускается вне среды Telegram, это предотвратит краш при импорте, но работать не будет.
try:
    from client_utils import get_last_fragment
    from android_utils import run_on_ui_thread, log
except ImportError:
    def get_last_fragment(): return None
    def run_on_ui_thread(f): f()
    def log(t): print(t)

class _MandreRunnable(dynamic_proxy(Runnable)):
    def __init__(self, fn):
        super().__init__()
        self._fn = fn
    def run(self):
        try:
            if self._fn: self._fn()
        except Exception as e:
            print(f"MandreInApp Error: {e}")

class MandreInApp:
    """
    Упрощенная библиотека для показа In-App уведомлений в стиле Telegram.
    Based on code by @meeowPlugins.
    """

    @staticmethod
    def show(title: str, subtitle: str, photo_object=None, top: bool = True, 
             max_lines: int = 2, duration_sec: int = 3, 
             button_text: str = None, on_click=None):
        """
        Показывает уведомление.
        
        :param title: Заголовок (Жирный текст).
        :param subtitle: Подзаголовок (Текст сообщения).
        :param photo_object: Объект TLRPC.User или TLRPC.Chat для аватарки. Если None - без аватарки.
        :param top: True = сверху, False = снизу.
        :param max_lines: Максимум строк текста.
        :param duration_sec: Длительность (1 = коротко, 3+ = долго).
        :param button_text: Текст кнопки (например "Открыть").
        :param on_click: Функция (lambda), вызываемая при нажатии на кнопку.
        """
        
        def _ui_task():
            try:
                fragment = get_last_fragment()
                if not fragment:
                    return

                # Если фото не передано, используем простой Bulletin
                if photo_object is None and not button_text:
                    factory = BulletinFactory.of(fragment)
                    bulletin = factory.createSimpleBulletin(title, subtitle)
                    bulletin.show(top)
                    return

                # Сложный Layout
                context = fragment.getContext()
                resource_provider = fragment.getResourceProvider()
                layout = Bulletin.TwoLineLayout(context, resource_provider)

                # Настройка фото
                if photo_object and (isinstance(photo_object, TLRPC.User) or isinstance(photo_object, TLRPC.Chat)):
                    location = ImageLocation.getForUserOrChat(photo_object, ImageLocation.TYPE_SMALL)
                    layout.imageView.setImage(location, "64_64", BitmapDrawable(), None)
                    layout.imageView.getImageReceiver().setRoundRadius(AndroidUtilities.dp(5))
                else:
                    # Если фото нет, но мы в сложном режиме, можно скрыть иконку или поставить заглушку
                    # Здесь просто оставляем пустым, AndroidUtilities обработает
                    pass

                # Настройка текста
                layout.titleTextView.setText(title)
                layout.titleTextView.setSingleLine(True)
                layout.titleTextView.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 15)
                layout.titleTextView.setTypeface(AndroidUtilities.bold())

                layout.subtitleTextView.setText(subtitle)
                layout.subtitleTextView.setSingleLine(False)
                layout.subtitleTextView.setMaxLines(max_lines)
                layout.subtitleTextView.setEllipsize(TextUtils.TruncateAt.END)
                layout.subtitleTextView.setTextColor(Theme.getColor(Theme.key_chats_message))

                # Настройка кнопки
                if button_text and on_click:
                    layout.setButton(
                        Bulletin.UndoButton(context, True, resource_provider)
                        .setText(button_text)
                        .setUndoAction(_MandreRunnable(on_click))
                    )

                # Показ
                duration_ms = 1500 if duration_sec <= 1 else 2750
                if duration_sec > 4: duration_ms = 5000
                
                factory = BulletinFactory.of(fragment)
                bulletin = factory.create(layout, duration_ms)
                bulletin.show(top)

            except Exception as e:
                log(f"[MandreInApp] Error: {e}")

        run_on_ui_thread(_ui_task)

