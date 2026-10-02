from PySide6.QtWidgets import (
    QDialog,
    QGridLayout,
    QMainWindow,
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QPushButton,
    QScrollArea,
    QLineEdit,
)
from PySide6.QtCore import Qt

from components import ProductCard, ProductDialog, ProductHistory


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LocalMind")
        self.resize(1000, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_layout = QVBoxLayout(central_widget)

        self.history = ProductHistory()
        self.history.import_history()
        self.product_list = []

        # =========================
        # Header
        # =========================

        header = QWidget()
        header_layout = QHBoxLayout(header)

        self.logo = QLabel("LocalMind")
        self.logo.setObjectName("logo")

        self.settings_button = QPushButton("⚙ Налаштування")
        self.settings_button.setObjectName("settingsButton")
        self.settings_button.clicked.connect(self.toggle_settings)

        header_layout.addWidget(self.logo)
        header_layout.addStretch()
        header_layout.addWidget(self.settings_button)

        central_layout.addWidget(header)

        # =========================
        # Content
        # =========================

        main_content = QWidget()
        main_content_layout = QVBoxLayout(main_content)

        # =========================
        # Title
        # =========================

        self.title = QLabel("Оберіть варіант")
        self.title.setObjectName("pageTitle")
        self.title.setAlignment(Qt.AlignCenter)

        main_content_layout.addWidget(self.title)

        # =========================
        # Options
        # =========================

        options_layout = QHBoxLayout()

        # =========================
        # Image analysis section
        # =========================

        self.image_section = QFrame()
        self.image_section.setObjectName("card")
        image_layout = QVBoxLayout(self.image_section)

        image_title = QLabel("Аналіз зображення")
        image_title.setAlignment(Qt.AlignCenter)

        self.image_button = QPushButton("Додати зображення")
        self.image_button.setObjectName("primaryButton")

        image_layout.addWidget(image_title)
        image_layout.addWidget(self.image_button)

        # =========================
        # Meal calculation section
        # =========================

        self.meal_section = QFrame()
        self.meal_section.setObjectName("card")
        self.meal_layout = QVBoxLayout(self.meal_section)

        meal_title = QLabel("Розрахунок")
        meal_title.setAlignment(Qt.AlignCenter)

        self.meal_layout.addWidget(meal_title)

        self.meal_scroll = QScrollArea()
        self.meal_scroll.setWidgetResizable(True)
        self.meal_scroll.setFrameShape(QFrame.NoFrame)

        self.meal_content = QWidget()
        self.meal_content_layout = QVBoxLayout(self.meal_content)
        self.meal_content_layout.setContentsMargins(0, 0, 0, 0)
        self.meal_content_layout.setSpacing(8)
        self.meal_content_layout.setAlignment(Qt.AlignTop)

        self.meal_scroll.setWidget(self.meal_content)

        self.meal_layout.addWidget(self.meal_scroll)

        # -------------------------
        # Product (INITIAL)
        # -------------------------

        # self.product = Product(name="Картопля", carbs_per_100g=20)
        # self.history.add_product(product=self.product)
        # print(
        #     "Product value:",
        #     self.product.name,
        #     self.product.carbs_per_100g,
        #     self.product.calculate_carbohydrates(200),
        #     self.product.calculate_bread_units(200),
        # )

        # -------------------------
        # Add product
        # -------------------------

        self.add_product_button = QPushButton("+ Додати продукт")
        self.add_product_button.setObjectName("secondaryButton")
        self.meal_layout.addWidget(self.add_product_button)

        self.add_product_button.clicked.connect(self.show_product_dialog)

        # -------------------------
        # Total
        # -------------------------

        total_carbs_value = 0
        total_bread_units_value = 0

        result_section = QGridLayout()

        self.total_carbs = QLabel(f"Всього вуглеводів: {total_carbs_value} г")
        self.total_bread_units = QLabel(f"Всього: {total_bread_units_value} ХО")

        self.total_carbs.setObjectName("totalCarbs")
        self.total_bread_units.setObjectName("totalBreadUnits")

        self.total_carbs.setAlignment(Qt.AlignRight)
        self.total_bread_units.setAlignment(Qt.AlignRight)

        result_section.addWidget(self.total_carbs, 0, 0)
        result_section.addWidget(self.total_bread_units, 0, 1)

        self.meal_layout.addLayout(result_section)

        # =========================
        # Add sections
        # =========================

        options_layout.addWidget(self.image_section)
        options_layout.addWidget(self.meal_section)

        main_content_layout.addLayout(options_layout)

        # =========================
        # Container
        # =========================

        self.content_container = QWidget()

        content_layout = QVBoxLayout(self.content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)

        content_layout.addWidget(main_content)
        central_layout.addWidget(self.content_container)

        # =========================
        # Settings panel
        # =========================

        self.settings_panel = QFrame()
        self.settings_panel.setObjectName("settingsPanel")

        self.settings_panel.setParent(self.content_container)
        self.settings_panel.setFixedWidth(280)

        settings_layout = QVBoxLayout(self.settings_panel)
        settings_layout.setContentsMargins(24, 24, 24, 24)
        settings_layout.setSpacing(16)

        settings_title = QLabel("Налаштування")
        settings_title.setObjectName("settingsTitle")

        bread_units_equals_label = QLabel("1 Хлібна Одиниця:")
        bread_units_equals_label.setObjectName("breadUnitsEqualsLabel")

        bread_units_equals_edit = QLineEdit()
        bread_units_equals_edit.setObjectName("breadUnitsEqualsEdit")
        bread_units_equals_edit.setPlaceholderText("10 - 15")

        settings_layout.addWidget(settings_title)
        settings_layout.addWidget(bread_units_equals_label)
        settings_layout.addWidget(bread_units_equals_edit)
        settings_layout.addStretch()

        self.settings_panel.hide()

    # =========================
    # Functions
    # =========================

    def show_product_dialog(self):
        dialog = ProductDialog(self, history=self.history)
        if dialog.exec() == QDialog.Accepted:
            product, weight = dialog.get_product_data()

            self.product_list.append([product, weight])

            product_card = ProductCard(
                name=product.name,
                weight=weight,
                carbs_per_100g=product.carbs_per_100g,
                carbohydrates=product.calculate_carbohydrates(weight),
                bread_units=product.calculate_bread_units(weight),
            )

            product_card.delete_requested.connect(
                lambda: self.delete_product(product_card, product, weight)
            )

            self.meal_content_layout.addWidget(product_card)
            self.update_totals()

    def delete_product(self, product_card, product, weight):
        self.product_list.remove([product, weight])
        self.meal_content_layout.removeWidget(product_card)
        product_card.deleteLater()
        self.update_totals()

    def update_totals(self):
        total_carbs_value = sum(
            product.calculate_carbohydrates(weight)
            for product, weight in self.product_list
        )

        total_bread_units_value = sum(
            product.calculate_bread_units(weight)
            for product, weight in self.product_list
        )

        self.total_carbs.setText(f"Всього вуглеводів: {total_carbs_value} г")

        self.total_bread_units.setText(f"Всього: {total_bread_units_value} ХО")

    def toggle_settings(self):
        if self.settings_panel.isVisible():
            self.settings_panel.hide()
            return

        self.settings_panel.show()

        self.settings_panel.setGeometry(
            self.content_container.width() - self.settings_panel.width(),
            0,
            self.settings_panel.width(),
            self.content_container.height(),
        )
