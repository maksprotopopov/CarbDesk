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
    QStackedWidget,
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
        central_layout.setContentsMargins(12, 8, 12, 12)
        central_layout.setSpacing(0)

        # =========================
        # Data
        # =========================

        self.history = ProductHistory()
        self.history.import_history()

        self.product_list = []
        self.bread_units_value = 10

        # =========================
        # Header
        # =========================

        header = QWidget()
        header_layout = QHBoxLayout(header)

        header_layout.setContentsMargins(8, 4, 8, 4)

        self.logo = QLabel("LocalMind")
        self.logo.setObjectName("logo")

        self.settings_button = QPushButton("⚙ Settings")
        self.settings_button.setObjectName("settingsButton")
        self.settings_button.clicked.connect(self.toggle_settings)

        header_layout.addWidget(self.logo)
        header_layout.addStretch()
        header_layout.addWidget(self.settings_button)

        central_layout.addWidget(header)

        # =========================
        # Content container
        # =========================

        self.content_container = QWidget()

        content_layout = QVBoxLayout(self.content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)

        central_layout.addWidget(self.content_container)

        # =========================
        # Main content
        # =========================

        main_content = QWidget()

        main_content_layout = QVBoxLayout(main_content)
        main_content_layout.setContentsMargins(24, 12, 24, 24)
        main_content_layout.setSpacing(10)

        content_layout.addWidget(main_content)

        # =========================
        # Page header
        # =========================

        self.title = QLabel("Calculation")
        self.title.setObjectName("pageTitle")

        subtitle = QLabel("Add products to calculate carbohydrates and bread units.")
        subtitle.setObjectName("pageSubtitle")

        main_content_layout.addWidget(self.title)
        main_content_layout.addWidget(subtitle)

        # =========================
        # Meal calculation section
        # =========================

        self.meal_section = QFrame()
        self.meal_section.setObjectName("card")

        self.meal_layout = QVBoxLayout(self.meal_section)
        self.meal_layout.setContentsMargins(16, 16, 16, 16)
        self.meal_layout.setSpacing(12)

        # =========================
        # Meal header
        # =========================

        meal_header = QHBoxLayout()

        meal_title = QLabel("Products")
        meal_title.setObjectName("sectionTitle")

        self.add_product_button = QPushButton("+ Add Product")
        self.add_product_button.setObjectName("secondaryButton")

        meal_header.addWidget(meal_title)
        meal_header.addStretch()
        meal_header.addWidget(self.add_product_button)

        self.meal_layout.addLayout(meal_header)

        self.add_product_button.clicked.connect(self.show_product_dialog)

        # =========================
        # Product list
        # =========================

        self.meal_scroll = QScrollArea()
        self.meal_scroll.setWidgetResizable(True)
        self.meal_scroll.setFrameShape(QFrame.NoFrame)

        self.meal_content = QWidget()

        self.meal_content_layout = QGridLayout(self.meal_content)
        self.meal_content_layout.setContentsMargins(0, 0, 0, 0)
        self.meal_content_layout.setHorizontalSpacing(8)
        self.meal_content_layout.setVerticalSpacing(8)

        self.meal_content_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # self.meal_content_layout.setColumnMinimumWidth(0, 300)
        # self.meal_content_layout.setColumnMinimumWidth(1, 300)
        self.meal_content_layout.setColumnStretch(0, 0)
        self.meal_content_layout.setColumnStretch(1, 0)

        self.meal_scroll.setWidget(self.meal_content)

        self.meal_layout.addWidget(self.meal_scroll, 1)

        # =========================
        # Totals
        # =========================

        result_section = QHBoxLayout()
        result_section.setSpacing(8)

        self.total_carbs = QLabel("Carbohydrates\n0 g")
        self.total_bread_units = QLabel("Bread Units\n0 BU")

        self.total_carbs.setObjectName("totalCarbs")
        self.total_bread_units.setObjectName("totalBreadUnits")

        result_section.addWidget(self.total_carbs)
        result_section.addWidget(self.total_bread_units)

        self.meal_layout.addLayout(result_section)

        main_content_layout.addWidget(self.meal_section, 1)

        # =========================
        # Image analysis
        # =========================

        self.image_section = QFrame()
        self.image_section.setObjectName("imageSection")

        image_layout = QHBoxLayout(self.image_section)
        image_layout.setContentsMargins(14, 12, 14, 12)

        image_text_layout = QVBoxLayout()
        image_text_layout.setSpacing(2)

        image_title = QLabel("Image Analysis")
        image_title.setObjectName("sectionTitle")

        image_description = QLabel("Add a product image for analysis.")
        image_description.setObjectName("sectionDescription")

        image_text_layout.addWidget(image_title)
        image_text_layout.addWidget(image_description)

        self.image_button = QPushButton("Add Image")
        self.image_button.setObjectName("secondaryButton")
        self.image_button.setEnabled(False)

        development_label = QLabel("In development")
        development_label.setObjectName("developmentLabel")

        image_layout.addLayout(image_text_layout)
        image_layout.addStretch()
        image_layout.addWidget(development_label)
        image_layout.addWidget(self.image_button)

        main_content_layout.addWidget(self.image_section)

        # =========================
        # Settings panel
        # =========================

        self.settings_panel = QFrame()
        self.settings_panel.setObjectName("settingsPanel")

        self.settings_panel.setParent(self.content_container)
        self.settings_panel.setFixedWidth(280)

        settings_layout = QVBoxLayout(self.settings_panel)
        settings_layout.setContentsMargins(20, 20, 20, 20)
        settings_layout.setSpacing(12)

        self.settings_stack = QStackedWidget()

        settings_layout.addWidget(self.settings_stack)

        # =========================
        # Settings page
        # =========================

        settings_page = QWidget()

        settings_page_layout = QVBoxLayout(settings_page)
        settings_page_layout.setContentsMargins(0, 0, 0, 0)
        settings_page_layout.setSpacing(12)

        settings_title = QLabel("Settings")
        settings_title.setObjectName("settingsTitle")

        bread_units_equals_label = QLabel("1 Bread Unit (g):")
        bread_units_equals_label.setObjectName("breadUnitsEqualsLabel")

        self.bread_units_equals_edit = QLineEdit()
        self.bread_units_equals_edit.setObjectName("breadUnitsEqualsEdit")
        self.bread_units_equals_edit.setText("10")
        self.bread_units_equals_edit.setPlaceholderText("10 - 15")

        submit_button = QPushButton("Save")
        submit_button.setObjectName("primaryButton")

        history_button = QPushButton("Open History")
        history_button.setObjectName("secondaryButton")

        settings_page_layout.addWidget(settings_title)
        settings_page_layout.addWidget(bread_units_equals_label)
        settings_page_layout.addWidget(self.bread_units_equals_edit)
        settings_page_layout.addWidget(submit_button)

        settings_page_layout.addStretch()

        settings_page_layout.addWidget(history_button)

        submit_button.clicked.connect(self.save_settings)

        # =========================
        # History page
        # =========================

        history_page = QWidget()

        history_page_layout = QVBoxLayout(history_page)
        history_page_layout.setContentsMargins(0, 0, 0, 0)
        history_page_layout.setSpacing(10)

        history_title = QLabel("History")
        history_title.setObjectName("settingsTitle")

        back_button = QPushButton("← Settings")
        back_button.setObjectName("secondaryButton")

        history_scroll = QScrollArea()
        history_scroll.setWidgetResizable(True)
        history_scroll.setFrameShape(QFrame.NoFrame)

        history_content = QWidget()

        self.history_content_layout = QVBoxLayout(history_content)
        self.history_content_layout.setContentsMargins(0, 0, 0, 0)
        self.history_content_layout.setSpacing(8)
        self.history_content_layout.setAlignment(Qt.AlignTop)

        history_scroll.setWidget(history_content)

        history_page_layout.addWidget(history_title)
        history_page_layout.addWidget(history_scroll, 1)
        history_page_layout.addWidget(back_button)

        # =========================
        # Add pages
        # =========================

        self.settings_stack.addWidget(settings_page)
        self.settings_stack.addWidget(history_page)

        self.settings_stack.setCurrentWidget(settings_page)

        # =========================
        # Navigation
        # =========================

        history_button.clicked.connect(self.show_history)

        back_button.clicked.connect(
            lambda: self.settings_stack.setCurrentWidget(settings_page)
        )

        # =========================
        # Hide settings
        # =========================

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
                bread_units=product.calculate_bread_units(
                    weight, self.bread_units_value
                ),
            )

            product_card.delete_requested.connect(
                lambda: self.delete_product(product_card, product, weight)
            )

            self.refresh_product_grid()
            self.update_totals()

    def delete_product(self, product_card, product, weight):
        if [product, weight] in self.product_list:
            self.product_list.remove([product, weight])

        self.refresh_product_grid()
        self.update_totals()

    def update_totals(self):
        total_carbs_value = sum(
            product.calculate_carbohydrates(weight)
            for product, weight in self.product_list
        )

        total_bread_units_value = sum(
            product.calculate_bread_units(weight, self.bread_units_value)
            for product, weight in self.product_list
        )

        self.total_carbs.setText(f"Total Carbohydrates: {total_carbs_value} g")

        self.total_bread_units.setText(f"Total: {total_bread_units_value} BU")

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

    def save_settings(self):
        bread_units_value = self.bread_units_equals_edit.text()
        if bread_units_value.isdigit():
            bread_units_value = int(bread_units_value)
            if 10 <= bread_units_value <= 15:
                self.bread_units_value = bread_units_value
                self.settings_panel.hide()

    def show_history(self):
        self.settings_stack.setCurrentIndex(1)

        while self.history_content_layout.count():
            item = self.history_content_layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        for product in reversed(self.history.get_products()):
            product_label = QLabel(
                f"{product.name}\n" f"{product.carbs_per_100g} g / 100 g"
            )

            product_label.setObjectName("historyItem")

            self.history_content_layout.addWidget(product_label)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        if self.settings_panel.isVisible():
            self.settings_panel.setGeometry(
                self.content_container.width() - self.settings_panel.width(),
                0,
                self.settings_panel.width(),
                self.content_container.height(),
            )

    def refresh_product_grid(self):
        while self.meal_content_layout.count():
            item = self.meal_content_layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

        for index, (product, weight) in enumerate(self.product_list):

            product_card = ProductCard(
                name=product.name,
                weight=weight,
                carbs_per_100g=product.carbs_per_100g,
                carbohydrates=product.calculate_carbohydrates(weight),
                bread_units=product.calculate_bread_units(
                    weight, self.bread_units_value
                ),
            )

            product_card.setFixedWidth(360)

            product_card.delete_requested.connect(
                lambda card=product_card, p=product, w=weight: self.delete_product(
                    card, p, w
                )
            )

            row = index // 2
            column = index % 2

            self.meal_content_layout.addWidget(
                product_card, row, column, Qt.AlignLeft | Qt.AlignTop
            )
