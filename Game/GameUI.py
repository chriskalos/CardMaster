import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QToolTip
from PySide6.QtCore import QTimer, Qt, QRect, QPoint
from PySide6.QtGui import QPainter, QColor, QFont, QPixmap, QPalette
from GameManager import GameManager  # Assuming GameManager and Card classes are defined in this module

class CardGameUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.card_rects = {}  # To store rectangles of cards currently displayed

        # Tooltip stuff
        self.tooltip = CustomTooltip(self)
        self.tooltip.hide()  # Initially hidden
        self.hover_timer = QTimer(self)
        self.hover_timer.setSingleShot(True)
        self.hover_timer.timeout.connect(self.hide_tooltip)
        self.current_hover_index = None  # Track the index of the currently hovered card

    def hide_tooltip(self):
        if not any(self.animation_states[i]['tooltip_shown'] for i in self.animation_states):
            self.tooltip.hide()
            self.current_hover_index = None

    def resizeEvent(self, event):
        # Maintain a 16:9 aspect ratio
        new_width = event.size().width()
        new_height = int(new_width / 16 * 9)  # Calculate height based on a 16:9 ratio
        self.resize(new_width, new_height)

        # Update the background image to fit the new size
        self.applyBackground()

    def applyBackground(self):
        # Scale pixmap to current size and set as background
        scaled_pixmap = self.bg_pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding)
        palette = QPalette()
        palette.setBrush(QPalette.Window, scaled_pixmap)
        self.setPalette(palette)

    def initUI(self):
        self.setGeometry(300, 300, 1600, 900)
        self.setWindowTitle('CardMaster')
        # self.setStyleSheet("background-color: rgb(59, 178, 115);")

        # Load and set background image
        self.bg_pixmap = QPixmap('img/field bg.png')
        self.applyBackground()


        # Set up the game logic
        self.game_manager = GameManager()
        self.game_manager.start_match()

        # Font setup
        self.font = QFont('Arial', 16)

        # Timer for animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000 / 120)  # roughly 120 fps

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
                'tooltip_shown': False,
                'clicked': False
            }

    def interpolate(self, value, target, speed):
        return value + (target - value) * speed

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_deck(painter, self.game_manager.player.hand, self.width() // 8, self.height() * 3 // 4 + 50, 0)
        self.draw_deck(painter, self.game_manager.current_match.enemy.hand, self.width() // 8, self.height() // 4 - 50,
                       len(self.game_manager.player.hand.cards))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            for index, state in self.animation_states.items():
                card_rect = QRect(state['x'] - state['width'] // 2, state['y'] - state['height'] // 2,
                                  state['width'], state['height'])
                if card_rect.contains(event.pos()):
                    state['clicked'] = not state['clicked']  # Toggle the clicked state
                    self.handle_card_click(index)  # Call a method to handle the card click
                    break

    def handle_card_click(self, index):
        card = self.get_card_by_index(index)
        if self.animation_states[index]['clicked']:
            # Perform actions when the card is clicked
            print(f"Card {card.name} is clicked!")
            # Add your desired actions here
        else:
            # Perform actions when the card is unclicked
            print(f"Card {card.name} is unclicked!")
            # Add your desired actions here

    def get_card_by_index(self, index):
        cards = self.game_manager.player.hand.cards + self.game_manager.current_match.enemy.hand.cards
        return cards[index]

    def draw_deck(self, painter, deck, x, y, start_index=0):
        num_cards = len(deck.cards)
        card_width = 100  # Standard width for each card

        # Determine the total space available on the screen for the cards
        max_total_width = self.width() - 2 * x  # Calculate available width from starting x to window edge
        total_card_width = num_cards * card_width

        # Adjust card_spacing to fit all cards within the available width
        if total_card_width > max_total_width:
            # Reduce spacing if cards would exceed the screen width
            card_spacing = (max_total_width - card_width) / max(num_cards - 1, 1)
        else:
            # Keep standard spacing if there is enough space
            card_spacing = 120  # This can be adjusted if you want a different default spacing

        # Calculate the adjusted starting x position to center the cards
        total_used_width = card_spacing * (num_cards - 1) + card_width
        adjusted_x = x + (max_total_width - total_used_width) // 2  # Center the cards

        for i, card in enumerate(deck.cards):
            index = start_index + i
            card_x = adjusted_x + i * card_spacing
            self.draw_card(painter, card, card_x, y, self.animation_states, index)

    def draw_card(self, painter, card, x, y, animation_states, index):
        state = animation_states[index]
        mouse_pos = self.mapFromGlobal(self.cursor().pos())
        card_rect = QRect(x - state['width'] // 2, y - state['height'] // 2, state['width'], state['height'])

        state['x'] = x
        state['y'] = y

        # Adjust the card's target size only if the mouse state changes to prevent flickering
        if card_rect.contains(mouse_pos) and state['small']:
            state['small'] = False
            # state['target_width'] = 140
            # state['target_height'] = 210
        elif not card_rect.contains(mouse_pos) and not state['small']:
            state['small'] = True
            # state['target_width'] = 100
            # state['target_height'] = 150

        if state['small']:
            state['target_width'] = 100
            state['target_height'] = 150
        elif not state['small']:
            state['target_width'] = 140
            state['target_height'] = 210

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

        icon_size = max(50, state['width'] // 2, state['height'] // 2)
        icon_rect = QRect(x - icon_size // 2, y - icon_size // 2, icon_size, icon_size)
        if card.image and not card.image.isNull():
            painter.drawImage(icon_rect, card.image)  # Directly draw the QImage
        else:
            # Draw a simple rectangle in the place of the image
            painter.fillRect(icon_rect, QColor(100, 100, 100))

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
        painter.drawText(x - state['width'] // 4, icon_rect.top() - font_size - 16,
                         state['width'] // 2, font_size + 6, Qt.AlignCenter, card.name)

        if state['clicked']:
            # Draw a border around the card when clicked
            painter.setPen(QColor(255, 0, 0))
            painter.drawRect(card_rect.adjusted(1, 1, -1, -1))

        if not state['small']:
            # Only draw detailed text for large cards
            detail_text_margin = state['width'] * 0.1
            detail_text_rect = QRect(card_rect.left() + detail_text_margin, icon_rect.bottom() + 20,
                                     card_rect.width() - 2 * detail_text_margin,
                                     state['height'] - icon_rect.bottom() - 20)

            detail_font_size = max(8, int(detail_text_rect.height() / 12))
            detail_font = QFont('Arial', detail_font_size)
            painter.setFont(detail_font)

        if card_rect.contains(mouse_pos):
            if self.current_hover_index != index:  # New card hovered
                if self.current_hover_index is not None:  # There was a previous card being hovered
                    self.animation_states[self.current_hover_index]['tooltip_shown'] = False
                self.current_hover_index = index
                self.tooltip.setText(f"{card.description}\n\nEffect: {card.effect_description}")
                tooltip_pos = self.mapToGlobal(card_rect.bottomRight() + QPoint(20, -40))
                self.tooltip.move(tooltip_pos)
                self.tooltip.adjustSize()
                self.tooltip.show()
                state['tooltip_shown'] = True
                self.hover_timer.stop()  # Stop the timer as we are over a card
        else:
            if state['tooltip_shown']:
                state['tooltip_shown'] = False  # Mark the tooltip as no longer shown for this card
                if self.current_hover_index == index:  # Check if this is the last card hovered over
                    self.hover_timer.start(100)  # Delay before hiding tooltip to check if another card is hovered

class CustomTooltip(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.ToolTip)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.text = ""
        self.text_margin = 10  # Margin around the text
        self.setMinimumWidth(100)  # Minimum width of the tooltip
        self.font = QFont('Arial', 12)  # Set the font once here

    def setText(self, text):
        self.text = text
        self.updateGeometry()  # Update the geometry based on the new text
        self.update()  # Trigger a repaint with the new text

    def updateGeometry(self):
        # Calculate the required size based on the text
        width = self.fontMetrics().boundingRect(QRect(0, 0, 200, 1000), Qt.TextWordWrap, self.text).width()
        height = self.fontMetrics().boundingRect(QRect(0, 0, width, 1000), Qt.TextWordWrap, self.text).height()
        self.resize(width + 2 * self.text_margin, height + 4 * self.text_margin)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(50, 50, 50))  # Set a darker background color
        painter.setPen(Qt.NoPen)  # No border
        painter.drawRect(self.rect())  # Draw a simple rectangle

        # Draw the text
        painter.setPen(QColor(255, 255, 255))  # Text color
        painter.setFont(self.font)  # Use the font set in __init__
        text_rect = self.rect().adjusted(self.text_margin, self.text_margin, -self.text_margin, -self.text_margin)
        painter.drawText(text_rect, Qt.TextWordWrap, self.text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CardGameUI()
    ex.show()
    sys.exit(app.exec())
