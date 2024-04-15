import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QToolTip
from PySide6.QtCore import QTimer, Qt, QRect, QPoint
from PySide6.QtGui import QPainter, QColor, QFont, QPixmap
from GameManager import GameManager  # Assuming GameManager and Card classes are defined in this module

class CardGameUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 1920, 1080)
        self.setWindowTitle('Card Game')
        self.setStyleSheet("background-color: rgb(59, 178, 115);")

        # Set up the game logic
        self.game_manager = GameManager()
        self.game_manager.start_match()

        # Font setup
        self.font = QFont('Arial', 16)

        # Timer for animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000 / 60)  # roughly 60 fps

        # Animation state initialization
        self.animation_states = {}
        self.init_animation_states()

        # Tooltip setup
        QToolTip.setFont(QFont('Arial', 14))

    # In your init_animation_states method:
    def init_animation_states(self):
        cards = self.game_manager.player.hand.cards + self.game_manager.current_match.enemy.hand.cards
        for i, card in enumerate(cards):
            self.animation_states[i] = {
                'width': 100, 'height': 150,
                'target_width': 100, 'target_height': 150,
                'small': True,
            }

    def interpolate(self, value, target, speed):
        return value + (target - value) * speed

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_deck(painter, self.game_manager.player.hand, self.width() // 8, self.height() * 3 // 4 - 75, 0)
        self.draw_deck(painter, self.game_manager.current_match.enemy.hand, self.width() // 8, self.height() // 4 + 75, len(self.game_manager.player.hand.cards))

    def draw_deck(self, painter, deck, x, y, start_index=0):
        card_spacing = 120
        for i, card in enumerate(deck.cards):
            index = start_index + i
            self.draw_card(painter, card, x + i * card_spacing, y, self.animation_states, index)

    def draw_card(self, painter, card, x, y, animation_states, index):
        state = animation_states[index]
        mouse_pos = self.mapFromGlobal(self.cursor().pos())
        card_rect = QRect(x - state['width'] // 2, y - state['height'] // 2, state['width'], state['height'])

        # Adjust the card's target size only if the mouse state changes to prevent flickering
        if card_rect.contains(mouse_pos) and state['small']:
            state['small'] = False
            state['target_width'] = 200
            state['target_height'] = 300
        elif not card_rect.contains(mouse_pos) and not state['small']:
            state['small'] = True
            state['target_width'] = 100
            state['target_height'] = 150

        # Smooth transition of card size
        state['width'] = self.interpolate(state['width'], state['target_width'], 0.1)
        state['height'] = self.interpolate(state['height'], state['target_height'], 0.1)
        card_rect = QRect(x - state['width'] // 2, y - state['height'] // 2, state['width'], state['height'])

        # Paint background of the card
        painter.fillRect(card_rect, QColor(210, 210, 210) if state['small'] else QColor(180, 180, 180))
        painter.setPen(QColor(0, 0, 0))
        painter.drawRect(card_rect)

        # Set font size based on card size
        font_size = max(10, int(state['height'] / 15))  # Adjust font size dynamically
        font = QFont('Arial', font_size)
        painter.setFont(font)

        # Calculate scaled icon size and position
        icon_size = max(50, state['width'] // 2, state['height'] // 3)
        icon_rect = QRect(x - icon_size // 2, y - state['height'] // 4, icon_size, icon_size)

        # Draw placeholder for icon
        painter.drawRect(icon_rect)  # Replace this with actual QPixmap drawing later

        # Draw tier, HP, and attack labels
        tier_label = f"Tier: {card.tier}" if not state['small'] else f"{card.tier}"
        hp_label = f"HP: {card.hp}" if not state['small'] else f"{card.hp}"
        attack_label = f"Attack: {card.attack}" if not state['small'] else f"{card.attack}"

        # Text positioning
        corner_offset = font_size // 2
        painter.drawText(card_rect.adjusted(corner_offset, corner_offset, -corner_offset, -corner_offset),
                         Qt.AlignTop | Qt.AlignRight, tier_label)
        painter.drawText(card_rect.adjusted(corner_offset, corner_offset, -corner_offset, -corner_offset),
                         Qt.AlignBottom | Qt.AlignLeft, hp_label)
        painter.drawText(card_rect.adjusted(corner_offset, corner_offset, -corner_offset, -corner_offset),
                         Qt.AlignBottom | Qt.AlignRight, attack_label)

        # Draw name centered above the icon
        painter.drawText(x - state['width'] // 4, icon_rect.top() - font_size - corner_offset,
                         state['width'] // 2, font_size, Qt.AlignCenter, card.name)

        if not state['small']:
            # Only draw detailed text for large cards
            detail_text_margin = state['width'] * 0.1
            detail_text_rect = QRect(card_rect.left() + detail_text_margin, icon_rect.bottom() + 20,
                                     card_rect.width() - 2 * detail_text_margin,
                                     state['height'] - icon_rect.bottom() - 20)

            desc_text = f"{card.description}\nEffect: {card.effect_description}"
            detail_font_size = max(8, int(detail_text_rect.height() / 12))
            detail_font = QFont('Arial', detail_font_size)
            painter.setFont(detail_font)

            # Ensure the text wraps within the card and doesn't overflow
            painter.drawText(detail_text_rect, Qt.AlignTop | Qt.AlignLeft | Qt.TextWordWrap, desc_text)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CardGameUI()
    ex.show()
    sys.exit(app.exec())
