import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button

# Cấu hình màn hình dọc giống điện thoại
Window.size = (400, 600)

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Biến trò chơi
        self.score = 0
        self.game_over = False
        self.fish_speed = 4
        
        # Khởi tạo người chơi (Cái giỏ)
        self.basket_width = 100
        self.basket_height = 20
        self.basket_x = 150
        self.basket_y = 50
        
        # Khởi tạo quả cầu (Con cá)
        self.fish_size = 30
        self.fish_x = random.randint(0, 370)
        self.fish_y = 600
        
        # Label hiển thị điểm số (Dùng font mặc định của máy)
        self.score_label = Label(
            text="Score: 0", 
            pos=(20, 530), 
            font_size=24,
            halign='left'
        )
        self.add_widget(self.score_label)
        
        # Nút chơi lại khi Game Over (ẩn lúc đầu)
        self.replay_btn = Button(
            text="Replay", 
            pos=(140, 250), 
            size=(120, 50),
            font_size=20
        )
        self.replay_btn.bind(on_press=self.reset_game)
        
        # Vẽ giao diện ban đầu
        with self.canvas:
            self.draw_game()
            
        # Chạy vòng lặp cập nhật game (60 khung hình/giây)
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def draw_game(self):
        self.canvas.clear()
        
        # Vẽ con cá (Màu đỏ)
        Color(1, 0.3, 0.3, 1)
        Ellipse(pos=(self.fish_x, self.fish_y), size=(self.fish_size, self.fish_size))
        
        # Vẽ cái giỏ hứng (Màu xanh nước biển)
        Color(0.2, 0.6, 1, 1)
        Rectangle(pos=(self.basket_x, self.basket_y), size=(self.basket_width, self.basket_height))

    def on_touch_move(self, touch):
        # Vuốt màn hình để điều khiển giỏ di chuyển theo ngón tay
        if not self.game_over:
            self.basket_x = touch.x - self.basket_width / 2
            # Giữ giỏ không đi ra ngoài màn hình
            if self.basket_x < 0: self.basket_x = 0
            if self.basket_x > self.width - self.basket_width: 
                self.basket_x = self.width - self.basket_width

    def update(self, dt):
        if self.game_over:
            return

        # Cho cá rơi xuống
        self.fish_y -= self.fish_speed
        
        # Kiểm tra nếu cá rơi trúng giỏ
        if (self.basket_y < self.fish_y < self.basket_y + self.basket_height) and \
           (self.basket_x < self.fish_x < self.basket_x + self.basket_width):
            self.score += 1
            self.score_label.text = f"Score: {self.score}"
            self.reset_fish()
            if self.score % 5 == 0:
                self.fish_speed += 1

        # Nếu cá rơi ra ngoài màn hình (Game Over)
        if self.fish_y < 0:
            self.game_over = True
            self.score_label.text = f"Game Over! Score: {self.score}"
            self.add_widget(self.replay_btn)

        # Vẽ lại màn hình
        self.draw_game()

    def reset_fish(self):
        self.fish_y = 600
        self.fish_x = random.randint(0, int(self.width) - self.fish_size)

    def reset_game(self, instance):
        self.score = 0
        self.fish_speed = 4
        self.game_over = False
        self.score_label.text = "Score: 0"
        self.remove_widget(self.replay_btn)
        self.reset_fish()

class FishingGameApp(App):
    def build(self):
        return GameWidget()

if __name__ == '__main__':
    FishingGameApp().run()
