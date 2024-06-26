import sys
import copy
import uuid

from PySide6.QtWidgets import QApplication, QWidget, QLabel, QToolTip, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, \
    QComboBox, QGroupBox
from PySide6.QtCore import QTimer, Qt, QRect, QPoint
from PySide6.QtGui import QPainter, QColor, QFont, QPixmap, QPalette, QTextOption, QFontMetrics
from GameManager import GameManager


class GameUI(QWidget):
    def __init__(self, debug_mode=False):
        super().__init__()
        self.debug_mode = debug_mode

        if debug_mode:
            self.game_manager = GameManager(debug_mode=True)
        else:
            self.game_manager = GameManager()

        self.game_over = False
        self.animation_states = {}
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
        self.continue_button.clicked.connect(self.continue_turn)

    def print_debug(self, message):
        if self.debug_mode:
            print(message)

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

        # Font setup
        self.font = QFont('Arial', 16)

        # Timer for animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000 // 120)  # roughly 120 fps

        # Animation state initialization
        self.init_animation_states()

        # Tooltip setup
        QToolTip.setFont(QFont('Arial', 14))

        # Create a main layout
        main_layout = QVBoxLayout()  # Vertical box layout

        # Enemy Stats Label
        self.enemy_stats_label = QLabel(
            f"{self.game_manager.current_match.enemy.name}\nHP: {self.game_manager.current_match.enemy.hp}\nMana: {self.game_manager.current_match.enemy.mana}")
        self.enemy_stats_label.setFont(QFont('Arial', 42))
        self.enemy_stats_label.setStyleSheet("color: black;")

        # Player Stats Label
        self.player_stats_label = QLabel(f"{self.game_manager.current_match.player.name}\nHP: {self.game_manager.current_match.player.hp}\nMana: {self.game_manager.current_match.player.mana}")
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
        self.continue_button = QPushButton("-->")
        self.continue_button.setMinimumSize(160, 60)
        self.continue_button.setStyleSheet("QPushButton { font-size: 20px; padding: 10px; }")
        button_layout.addWidget(self.continue_button)

        # Debug Menu Button
        if self.debug_mode:
            self.debug_button = QPushButton("Debug Menu")
            self.debug_button.setMinimumSize(160, 60)
            self.debug_button.setStyleSheet("QPushButton { font-size: 20px; padding: 10px; }")
            self.debug_button.clicked.connect(self.open_debug_window)
            button_layout.addWidget(self.debug_button, 0, Qt.AlignLeft)  # Add to the left of the button layout

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
            self.print_debug(f"DEBUG: Player card UUID: {card.uuid}")
        # For enemy's cards
        for card in self.game_manager.current_match.enemy.hand.cards:
            self.animation_states[card.uuid] = self.create_card_animation_state(False)
            self.print_debug(f"DEBUG: Enemy card UUID: {card.uuid}")

        for card in self.game_manager.player.cards_on_board.cards:
            self.animation_states[card.uuid] = self.create_card_animation_state(True)
            self.print_debug(f"DEBUG: Player card on board UUID: {card.uuid}")

        for card in self.game_manager.current_match.enemy.cards_on_board.cards:
            self.animation_states[card.uuid] = self.create_card_animation_state(False)
            self.print_debug(f"DEBUG: Enemy card on board UUID: {card.uuid}")

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
        if self.game_manager.game_over:
            self.game_over_screen()

    def interpolate(self, value, target, speed):
        return value + (target - value) * speed

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.game_over:
            painter.setFont(QFont('Arial', 48))
            if self.game_manager.current_match.winner is None:
                painter.drawText(self.rect(), Qt.AlignCenter, f"Game Over!\nIt's a draw!\nWins: {self.game_manager.player_wins}")
            else:
                painter.drawText(self.rect(), Qt.AlignCenter, f"Game Over!\n{self.game_manager.current_match.winner.name} wins!\nWins: {self.game_manager.player_wins}")
        if self.game_manager.check_match():
            self.update_stats()
            self.update()
        else:
            # Normal game drawing happens here
            self.draw_deck(painter, self.game_manager.current_match.player.hand, self.width() // 8, self.height() * 3 // 4 + 50)
            self.draw_deck(painter, self.game_manager.current_match.enemy.hand, self.width() // 8,
                           self.height() // 4 - 50)
            self.draw_deck(painter, self.game_manager.current_match.player.cards_on_board, self.width() // 8, self.height() // 2 + 75,
                           "board")
            self.draw_deck(painter, self.game_manager.current_match.enemy.cards_on_board, self.width() // 8,
                           self.height() // 2 - 80, "board")
            self.update_stats()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            clicked_uuid = None
            for uuid, state in self.animation_states.items():
                self.print_debug(f"DEBUG: Checking card {uuid}")
                card_rect = QRect(state['x'] - state['width'] // 2, state['y'] - state['height'] // 2, state['width'],
                                  state['height'])
                if card_rect.contains(event.pos()) and state['player_card'] and not state['is_on_board']:
                    state['clicked'] = not state['clicked']
                    clicked_uuid = uuid
                    break
            if clicked_uuid:
                self.handle_card_click(clicked_uuid)
            self.update_play_cards_button()

    def handle_card_click(self, card_uuid):
        card = self.get_card_by_uuid(card_uuid)
        if self.animation_states[card_uuid]['clicked']:
            self.print_debug(f"DEBUG handle_card_click: Card {card.name} is clicked!")
        else:
            self.print_debug(f"DEBUG handle_card_click: Card {card.name} is unclicked!")

    def reset_card_states(self):
        for state in self.animation_states.values():
            state['clicked'] = False  # Reset the clicked state of all cards
        self.update_play_cards_button()  # Update the button states

    def get_card_by_uuid(self, card_uuid):
        all_cards = (self.game_manager.current_match.player.hand.cards +
                     self.game_manager.current_match.enemy.hand.cards +
                     self.game_manager.current_match.player.cards_on_board.cards +
                     self.game_manager.current_match.enemy.cards_on_board.cards +
                     self.game_manager.current_match.player.dead_deck.cards +
                     self.game_manager.current_match.enemy.dead_deck.cards +
                     self.game_manager.current_match.player.alive_deck.cards +
                     self.game_manager.current_match.enemy.alive_deck.cards)
        for card in all_cards:
            if card.uuid == card_uuid:
                return card
        return None

    def update_play_cards_button(self):
        any_card_clicked = any(
            state['clicked'] for state in self.animation_states.values() if state.get('player_card', False) and not state.get('is_on_board', False))
        self.play_cards_button.setEnabled(any_card_clicked)

    def continue_turn(self):
        # Submit the cards on the board and go to the effects phase of the battle
        self.print_debug(f"Phase: {self.game_manager.current_match.phase.name}")
        self.game_manager.current_match.cycle_phase()
        for uuid, state in self.animation_states.items():
            if state['clicked'] and state['player_card']:
                card = self.get_card_by_uuid(uuid)
                if card in self.game_manager.current_match.player.cards_on_board.cards:
                    state['is_on_board'] = True
        self.reset_card_states()

    def play_cards(self):
        for uuid, state in self.animation_states.items():
            if state['clicked'] and state['player_card'] and not state['is_on_board']:
                card = self.get_card_by_uuid(uuid)
                if self.game_manager.current_match.player.play_card(card):
                    state['is_on_board'] = True
        self.reset_card_states()

    def open_debug_window(self):
        if self.debug_mode:  # Ensure it opens only in debug mode
            self.debug_window = DebugWindow(self.game_manager, self)
            self.debug_window.show()

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
        # Ensure that there is an animation state for every card drawn
        if uuid not in animation_states:
            animation_states[uuid] = self.create_card_animation_state(card)
            print(f"Created animation state for new card with UUID: {uuid}")
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

    def game_over_screen(self):
        self.game_over = True
        # Clear UI elements
        self.enemy_stats_label.hide()
        self.player_stats_label.hide()
        self.play_cards_button.hide()
        self.continue_button.hide()
        if self.debug_mode:
            self.debug_button.hide()
        # Set background to game over screen (actually repurposed title screen)
        self.bg_pixmap = QPixmap('img/title screen.png')
        self.applyBackground()
        self.update()  # Ensure the widget repaints after these changes

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
        self.resize(width + 2 * self.text_margin, height + 6 * self.text_margin)

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


class DebugWindow(QWidget):
    def __init__(self, game_manager, game_ui):
        super().__init__()
        self.game_manager = game_manager
        self.game_ui = game_ui
        self.all_cards = self.game_manager.current_match.player.hand.get_all_cards()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 800)
        self.setWindowTitle("Debug Menu")
        self.setStyleSheet(
            "QWidget { font-size: 14px; } QPushButton { font-weight: bold; background-color: #222222; color: #ffffff; padding: 5px; margin: 5px; } QLineEdit { padding: 2px; } QGroupBox { font-weight: bold; }")

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # Card Actions Group
        card_actions_group = QGroupBox("Card Actions")
        card_actions_layout = QVBoxLayout()
        self.card_selector = QComboBox()
        for card in self.all_cards:
            self.card_selector.addItem(card.name, card)
        card_actions_layout.addWidget(self.card_selector)
        self.add_card_to_player_button = QPushButton('Add Card to Player')
        self.add_card_to_player_button.clicked.connect(lambda: self.add_card_to_hand('player'))
        card_actions_layout.addWidget(self.add_card_to_player_button)
        self.add_card_to_enemy_button = QPushButton('Add Card to Enemy')
        self.add_card_to_enemy_button.clicked.connect(lambda: self.add_card_to_hand('enemy'))
        card_actions_layout.addWidget(self.add_card_to_enemy_button)
        card_actions_group.setLayout(card_actions_layout)
        layout.addWidget(card_actions_group)

        # Stat Modifications Group
        stat_modifications_group = QGroupBox("Stat Modifications")
        stat_modifications_layout = QVBoxLayout()
        hp_layout = QHBoxLayout()
        self.hp_label = QLabel('HP:')
        self.hp_input = QLineEdit()
        hp_layout.addWidget(self.hp_label)
        hp_layout.addWidget(self.hp_input)
        self.modify_hp_button = QPushButton('Modify Player HP')
        self.modify_hp_button.clicked.connect(lambda: self.modify_hp('player'))
        hp_layout.addWidget(self.modify_hp_button)
        self.modify_enemy_hp_button = QPushButton('Modify Enemy HP')
        self.modify_enemy_hp_button.clicked.connect(lambda: self.modify_hp('enemy'))
        hp_layout.addWidget(self.modify_enemy_hp_button)
        stat_modifications_layout.addLayout(hp_layout)

        mana_layout = QHBoxLayout()
        self.mana_label = QLabel('Mana:')
        self.mana_input = QLineEdit()
        mana_layout.addWidget(self.mana_label)
        mana_layout.addWidget(self.mana_input)
        self.modify_mana_button = QPushButton('Modify Player Mana')
        self.modify_mana_button.clicked.connect(lambda: self.modify_mana('player'))
        mana_layout.addWidget(self.modify_mana_button)
        self.modify_enemy_mana_button = QPushButton('Modify Enemy Mana')
        self.modify_enemy_mana_button.clicked.connect(lambda: self.modify_mana('enemy'))
        mana_layout.addWidget(self.modify_enemy_mana_button)
        stat_modifications_layout.addLayout(mana_layout)
        stat_modifications_group.setLayout(stat_modifications_layout)
        layout.addWidget(stat_modifications_group)

        # Battle Controls Group
        battle_controls_group = QGroupBox("Battle Controls")
        battle_controls_layout = QVBoxLayout()
        self.win_battle_button = QPushButton('Win Battle')
        self.win_battle_button.clicked.connect(self.win_battle)
        battle_controls_layout.addWidget(self.win_battle_button)
        self.lose_battle_button = QPushButton('Lose Battle')
        self.lose_battle_button.clicked.connect(self.lose_battle)
        battle_controls_layout.addWidget(self.lose_battle_button)
        battle_controls_group.setLayout(battle_controls_layout)
        layout.addWidget(battle_controls_group)

        self.setLayout(layout)

    def add_card_to_hand(self, target):
        card_index = self.card_selector.currentIndex()
        card_to_add = copy.copy(self.all_cards[card_index])
        card_to_add.uuid = uuid.uuid4()  # Generate a new UUID for the card
        if target == 'player':
            self.game_manager.current_match.player.hand.cards.append(card_to_add)
            print(f"Added {card_to_add.name} to player's hand.")
        elif target == 'enemy':
            self.game_manager.current_match.enemy.hand.cards.append(card_to_add)
            print(f"Added {card_to_add.name} to enemy's hand.")
        self.game_ui.init_animation_states()

    def modify_hp(self, target):
        new_hp = int(self.hp_input.text())
        if target == 'player':
            self.game_manager.current_match.player.hp = new_hp
            print(f"Player HP set to {new_hp}.")
        elif target == 'enemy':
            self.game_manager.current_match.enemy.hp = new_hp
            print(f"Enemy HP set to {new_hp}.")

    def modify_mana(self, target):
        new_mana = int(self.mana_input.text())
        if target == 'enemy':
            self.game_manager.current_match.enemy.mana = new_mana
            print(f"Enemy mana set to {new_mana}.")
        elif target == 'player':
            self.game_manager.current_match.player.mana = new_mana
            print(f"Player mana set to {new_mana}.")

    def win_battle(self):
        from Match import Phase  # Local import to avoid circular dependency
        self.game_manager.current_match.enemy.hp = 0
        self.game_manager.current_match.phase = Phase.ATTACKS
        self.game_manager.current_match.perform_phase()

    def lose_battle(self):
        from Match import Phase  # Local import to avoid circular dependency
        self.game_manager.current_match.player.hp = 0
        self.game_manager.current_match.phase = Phase.ATTACKS
        self.game_manager.current_match.perform_phase()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GameUI()
    ex.show()
    sys.exit(app.exec())
