import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtCore import QTimer, Qt, QRect, QPoint
from PySide6.QtGui import QPainter, QColor, QFont, QPixmap, QPalette
from GameManager import GameManager  # Assuming GameManager and Card classes are defined
from GameUI import CardGameUI, CustomTooltip  # Importing the modified CardGameUI
from Card import get_all_cards

class CardGalleryUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.tooltip = CustomTooltip(self)
        self.tooltip.hide()
        self.hover_timer = QTimer(self)
        self.hover_timer.setSingleShot(True)
        self.hover_timer.timeout.connect(self.tooltip.hide)

    def initUI(self):
        self.setGeometry(300, 300, 1600, 900)
        self.setWindowTitle('Card Gallery')
        self.all_cards = get_all_cards()  # Assuming this function correctly retrieves all cards
        self.animation_states = [{...} for _ in self.all_cards]  # Simplified state for each card

        self.bg_pixmap = QPixmap('img/gallery_bg.png')
        self.applyBackground()

        self.setLayout(QVBoxLayout())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        self.draw_cards(painter)

    def draw_cards(self, painter):
        rows, cols = 5, 5
        card_width, card_height = 140, 210
        padding = 10
        start_x, start_y = 50, 50

        for i, card in enumerate(self.all_cards):
            row = i // cols
            col = i % cols
            x = start_x + col * (card_width + padding)
            y = start_y + row * (card_height + padding)
            # Prepare state for each card
            state = {
                'width': card_width,
                'height': card_height,
                'small': False  # Assume all cards are large enough to show details
            }
            CardGameUI.draw_card(painter, card, x, y, state)  # Static call

    def applyBackground(self):
        scaled_pixmap = self.bg_pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding)
        palette = QPalette()
        palette.setBrush(QPalette.Window, scaled_pixmap)
        self.setPalette(palette)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CardGalleryUI()
    ex.show()
    sys.exit(app.exec())