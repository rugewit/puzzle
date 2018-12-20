from View import *
import settings





class Stopwatch():
    def __init__(self,t,btn_start_game,label_timer,label,win):
        self.btn_start_game = btn_start_game
        self.label_timer = label_timer
        #settings.CUR_TIME = settings.TIME
        self.timer = QTimer()
        self.timer.timeout.connect(self.counter)
        self.set_time()
        # части игры (предполагалось ,что при попытке ответить пользователь имел бы тоже временное ограничение)
        #на вторую часть можно поэтому не обращать  внимание
        self.part_one = False
        self.part_two = False
        self.label = label
        self.win = win
    # n - часть игры
    def start(self, n):
        self.timer.start(1000)
        self.btn_start_game.setEnabled(False)
        if n == 1:
            self.part_one = True
        else:
            self.part_one = False
            self.part_two = True

    def reset(self):
        self.timer.stop()
        settings.CUR_TIME = settings.TIME

        self.set_time()

    def counter(self):
        settings.CUR_TIME -= 1
        self.set_time()
        if settings.CUR_TIME == 0 and self.part_one:
            self.end_part_one()
        elif settings.CUR_TIME == 0 and self.part_two:
            self.reset()

    def is_timer_active(self):
        return self.timer.isActive()

    def end_part_one(self):
        try:
            self.label.setText('Теперь попробуйте восстановить расположение квадратов и нажмите на "подтвердить"')
            self.reset()
            set_img_numbers(self.win,list(range(1, settings.COLS * settings.COLS + 1, 1)))
            self.win.squares_movable(True)
            self.win.btn_confirm.setEnabled(True)
        except Exception as e:
            print(e)


    def end_part_two(self):
        pass


    def set_time(self):
        #hora = settings.CUR_TIME / 3600
        minutos = (settings.CUR_TIME % 3600) / 60
        segundos = (settings.CUR_TIME % 3600) % 60
        self.text = '<html><head/><body><p align="center"><span style=" font-size:48pt;">{}</span></p></body></html>'.format("%02d:%02d" % (minutos, segundos))
        self.label_timer.setText(self.text)