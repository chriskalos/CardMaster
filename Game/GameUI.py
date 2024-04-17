import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QToolTip, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtCore import QTimer, Qt, QRect, QPoint
from PySide6.QtGui import QPainter, QColor, QFont, QPixmap, QPalette, QTextOption, QFontMetrics
from GameManager import GameManager  # Assuming GameManager and Card classes are defined in this module

class GameUI(QWidget):
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
        self.current_hover_uuid = None  # Track the uuid of the currently hovered card
        self.play_cards_button.clicked.connect(self.play_cards)
        self.end_turn_button.clicked.connect(self.end_turn)

    def hide_tooltip(self):
        if not any(self.animation_states[i]['tooltip_shown'] for i in self.animation_states):
            self.tooltip.hide()
            self.current_hover_uuid = None

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
        self.timer.start(1000 // 120)  # roughly 120 fps

        # Animation state initialization
        self.animation_states = {}
        self.init_animation_states()

        # Tooltip setup
        QToolTip.setFont(QFont('Arial', 14))

        # Create a main layout
        main_layout = QVBoxLayout()  # Vertical box layout

        # Enemy Stats Label
        self.enemy_stats_label = QLabel(
            f"Enemy\nHP: {self.game_manager.current_match.enemy.hp}\nMana: {self.game_manager.current_match.enemy.mana}")
        self.enemy_stats_label.setFont(QFont('Arial', 42))
        self.enemy_stats_label.setStyleSheet("color: black;")

        # Player Stats Label
        self.player_stats_label = QLabel(f"Player\nHP: {self.game_manager.current_match.player.hp}\nMana: {self.game_manager.current_match.player.mana}")
        self.player_stats_label.setFont(QFont('Arial', 42))
        self.player_stats_label.setStyleSheet("color: black;")

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)  # Push buttons to the right

        # Play Card(s) Button
        self.play_cards_button = QPushButton("Play Card(s)")
        self.play_cards_button.setEnabled(False)
        self.play_cards_button.setMinimumSize(160, 60)
        self.play_cards_button.setStyleSheet("QPushButton { font-size: 20px; padding: 10px; }")
        button_layout.addWidget(self.play_cards_button)

        # End Turn Button
        self.end_turn_button = QPushButton("End Turn")
        self.end_turn_button.setMinimumSize(160, 60)
        self.end_turn_button.setStyleSheet("QPushButton { font-size: 20px; padding: 10px; }")
        button_layout.addWidget(self.end_turn_button)

        # Layout for stats
        stats_layout = QVBoxLayout()
        stats_layout.addWidget(self.enemy_stats_label)
        stats_layout.addStretch(1)  # Push player stats to the bottom
        stats_layout.addWidget(self.player_stats_label)

        # Combine stats and buttons into a final layout
        final_layout = QHBoxLayout()
        final_layout.addLayout(stats_layout)  # Stats on the left
        final_layout.addStretch(1)  # Center the game area
        final_layout.addLayout(button_layout)  # Buttons on the right

        main_layout.addLayout(final_layout)

        # Set the main layout to the central widget or the main window
        self.setLayout(main_layout)

    def init_animation_states(self):
        self.animation_states = {}
        # For player's cards
        for card in self.game_manager.player.hand.cards:
            self.animation_states[card.uuid] = self.create_card_animation_state(True)
            # print("DEBUG: Player card UUID:", card.uuid)
        # For enemy's cards
        for card in self.game_manager.current_match.enemy.hand.cards:
            self.animation_states[card.uuid] = self.create_card_animation_state(False)
            # print("DEBUG: Enemy card UUID:", card.uuid)

        for card in self.game_manager.player.cards_on_board.cards:
            self.animation_states[card.uuid] = self.create_card_animation_state(True)
            # print("DEBUG: Player card on board UUID:", card.uuid)

        for card in self.game_manager.current_match.enemy.cards_on_board.cards:
            self.animation_states[card.uuid] = self.create_card_animation_state(False)
            # print("DEBUG: Enemy card on board UUID:", card.uuid)

    def create_card_animation_state(self, is_player_card):
        return {
            'width': 100, 'height': 150,
            'target_width': 100, 'target_height': 150,
            'small': True,
            'tooltip_shown': False,
            'clicked': False,
            'player_card': is_player_card,
            'is_on_board': False
        }

    def update_stats(self):
        self.enemy_stats_label.setText(f"Enemy\nHP: {self.game_manager.current_match.enemy.hp}\nMana: {self.game_manager.current_match.enemy.mana}")
        self.player_stats_label.setText(f"Player\nHP: {self.game_manager.current_match.player.hp}\nMana: {self.game_manager.current_match.player.mana}")

    def update_animation_states(self):
        # Rebuild the entire animation_states to reflect current game state
        self.animation_states = {}
        self.init_animation_states()  # You may need to modify this function to work with dynamic changes

    def interpolate(self, value, target, speed):
        return value + (target - value) * speed

    def paintEvent(self, event):
        painter = QPainter(self)

        self.draw_deck(painter, self.game_manager.player.hand, self.width() // 8, self.height() * 3 // 4 + 50)
        self.draw_deck(painter, self.game_manager.current_match.enemy.hand, self.width() // 8,
                       self.height() // 4 - 50)

        self.draw_deck(painter, self.game_manager.player.cards_on_board, self.width() // 8, self.height() // 2 + 75, "board")
        self.draw_deck(painter, self.game_manager.current_match.enemy.cards_on_board, self.width() // 8, self.height() // 2 - 80, "board")
        self.update_stats()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            clicked_uuid = None
            for uuid, state in self.animation_states.items():
                print("DEBUG: Checking card", uuid)
                card_rect = QRect(state['x'] - state['width'] // 2, state['y'] - state['height'] // 2, state['width'],
                                  state['height'])
                if card_rect.contains(event.pos()) and state['player_card'] and not state['is_on_board']:
                    state['clicked'] = not state['clicked']
                    clicked_uuid = uuid
                    break
            if clicked_uuid:
                self.handle_card_click(clicked_uuid)
            self.update_play_cards_button()

    def handle_card_click(self, uuid):
        card = self.get_card_by_uuid(uuid)
        if self.animation_states[uuid]['clicked']:
            print(f"DEBUG handle_card_click: Card {card.name} is clicked!")
        else:
            print(f"DEBUG handle_card_click: Card {card.name} is unclicked!")

    def reset_card_states(self):
        for state in self.animation_states.values():
            state['clicked'] = False  # Reset the clicked state of all cards
        self.update_play_cards_button()  # Update the button states

    def get_card_by_uuid(self, uuid):
        all_cards = (self.game_manager.player.hand.cards +
                     self.game_manager.current_match.enemy.hand.cards +
                     self.game_manager.current_match.player.cards_on_board.cards +
                     self.game_manager.current_match.enemy.cards_on_board.cards +
                     self.game_manager.player.dead_deck.cards +
                     self.game_manager.current_match.enemy.dead_deck.cards +
                     self.game_manager.player.alive_deck.cards +
                     self.game_manager.current_match.enemy.alive_deck.cards)
        for card in all_cards:
            if card.uuid == uuid:
                return card
        return None

    def update_play_cards_button(self):
        any_card_clicked = any(
            state['clicked'] for state in self.animation_states.values() if state.get('player_card', False) and not state.get('is_on_board', False))
        self.play_cards_button.setEnabled(any_card_clicked)

    def end_turn(self):
        print("Phase:", self.game_manager.current_match.phase.name)
        if self.game_manager.current_match.phase.name == 'PLAY':
            self.game_manager.current_match.cycle_phase()
            self.game_manager.current_match.player.play_turn()
            self.reset_card_states()
        else:
            print("It's not the PLAY phase!")

    def play_cards(self):
        for uuid, state in self.animation_states.items():
            if state['clicked'] and state['player_card'] and not state['is_on_board']:
                card = self.get_card_by_uuid(uuid)
                if self.game_manager.current_match.player.play_card(card):
                    state['is_on_board'] = True
        self.reset_card_states()

    def draw_deck(self, painter, deck, x, y, type="hand"):
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

        if type == "board":
            # Cards start from the left edge
            adjusted_x = x
        else:
            # Calculate the adjusted starting x position to center the cards
            total_used_width = card_spacing * (num_cards - 1) + card_width
            adjusted_x = x + (max_total_width - total_used_width) // 2  # Center the cards

        i = 0
        for card in deck.cards:
            card_x = adjusted_x + i * card_spacing
            i += 1
            self.draw_card(painter, card, card_x, y, self.animation_states)

    def draw_card(self, painter, card, x, y, animation_states):
        uuid = card.uuid
        state = animation_states[card.uuid]
        mouse_pos = self.mapFromGlobal(self.cursor().pos())
        card_rect = QRect(x - state['width'] // 2, y - state['height'] // 2, state['width'], state['height'])

        state['x'] = x
        state['y'] = y

        # Adjust the card's target size only if the mouse state changes to prevent flickering
        if card_rect.contains(mouse_pos) and state['small']:
            state['small'] = False
        elif not card_rect.contains(mouse_pos) and not state['small']:
            state['small'] = True

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
        if card.color.name == "RED":
            card_color = QColor(247, 78, 59)
        elif card.color.name == "GREEN":
            card_color = QColor(143, 217, 65)
        elif card.color.name == "BLUE":
            card_color = QColor(65, 143, 217)
        elif card.color.name == "YELLOW":
            card_color = QColor(242, 192, 53)
        elif card.color.name == "PURPLE":
            card_color = QColor(143, 65, 217)
        else:
            card_color = QColor(200, 200, 200)

        painter.fillRect(card_rect, card_color if state['small'] else card_color.darker(125))
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
        # Define the rectangle where the name will be drawn
        name_rect = QRect(x - state['width'] // 2, icon_rect.top() - 25, state['width'],
                          20)  # Adjust height as needed to fit potentially wrapped text

        # Set text options to align center and wrap text
        text_option = QTextOption()
        text_option.setAlignment(Qt.AlignCenter | Qt.TextWordWrap)

        # Set the font and calculate if text needs wrapping
        font = QFont('Arial', font_size)  # You may adjust the font size based on space or other criteria
        painter.setFont(font)

        # Measure text to see if it fits in the provided rectangle
        font_metrics = QFontMetrics(font)
        required_width = font_metrics.horizontalAdvance(card.name)

        # Compare required width with available width
        if required_width > name_rect.width():
            # If text is too wide, adjust font size or rectangle
            font.setPointSize(font_size - 2)  # Decrease font size
            painter.setFont(font)
            # Optionally adjust the rectangle height based on new font size
            text_height = font_metrics.height() * 2  # Assuming it might need two lines now
            name_rect.setHeight(text_height)

        # Draw the name text with the adjusted settings
        painter.drawText(name_rect, Qt.TextWordWrap | Qt.AlignCenter, card.name)

        if state['clicked']:
            # Draw a thick border around the card when clicked
            border_width = 4  # Adjust this value to control border thickness (number of outlines)

            # Define the base color for the border
            base_color = QColor(230, 0, 0)  # Adjust color as needed

            # Draw outlines with increasing offsets to create a thicker border effect
            for i in range(border_width):
                adjusted_rect = card_rect.adjusted(i, i, -i, -i)
                pen_color = base_color.darker(100 + 15 * i)
                painter.setPen(pen_color)
                painter.drawRect(adjusted_rect)

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
            if self.current_hover_uuid != uuid:  # New card hovered
                if self.current_hover_uuid is not None:  # There was a previous card being hovered
                    self.animation_states[self.current_hover_uuid]['tooltip_shown'] = False
                self.current_hover_uuid = uuid
                self.tooltip.setText(f"{card.description}\n\nType: {card.card_class.name}\n\nEffect: {card.effect_description}")
                tooltip_pos = self.mapToGlobal(card_rect.bottomRight() + QPoint(20, -40))
                self.tooltip.move(tooltip_pos)
                self.tooltip.adjustSize()
                self.tooltip.show()
                state['tooltip_shown'] = True
                self.hover_timer.stop()  # Stop the timer as we are over a card
        else:
            if state['tooltip_shown']:
                state['tooltip_shown'] = False  # Mark the tooltip as no longer shown for this card
                if self.current_hover_uuid == uuid:  # Check if this is the last card hovered over
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
        self.resize(width + 2 * self.text_margin, height + 2 * self.text_margin)

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
    ex = GameUI()
    ex.show()
    sys.exit(app.exec())