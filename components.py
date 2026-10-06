from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QCompleter,
)

from PySide6.QtCore import QStringListModel, Qt, Signal
import json
from pathlib import Path


class ProductCard(QFrame):
    delete_requested = Signal()

    def __init__(self, name, weight, carbs_per_100g, carbohydrates, bread_units):
        super().__init__()

        self.setObjectName("productCard")

        # =========================
        # Header
        # =========================

        name_label = QLabel(name)
        name_label.setObjectName("productName")

        self.delete_button = QPushButton("×")
        self.delete_button.setObjectName("deleteButton")
        self.delete_button.setFixedSize(22, 22)

        self.delete_button.clicked.connect(self.delete_requested.emit)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(4)

        header_layout.addWidget(name_label)
        header_layout.addStretch()
        header_layout.addWidget(self.delete_button)

        # =========================
        # Statistics
        # =========================

        weight_card = StatCard("Netto", f"{weight} g")
        carbs_card = StatCard("Carbohydrates / 100 g", f"{carbs_per_100g} g")
        carbohydrates_card = StatCard("Carbohydrates", f"{carbohydrates} g")
        bread_units_card = StatCard("Bread Units", f"{bread_units}")

        stat_layout = QGridLayout()
        stat_layout.setContentsMargins(0, 0, 0, 0)
        stat_layout.setHorizontalSpacing(6)
        stat_layout.setVerticalSpacing(6)

        stat_layout.addWidget(weight_card, 0, 0)
        stat_layout.addWidget(carbs_card, 0, 1)
        stat_layout.addWidget(carbohydrates_card, 1, 0)
        stat_layout.addWidget(bread_units_card, 1, 1)

        # =========================
        # Main layout
        # =========================

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 8, 10, 8)
        main_layout.setSpacing(6)

        main_layout.addLayout(header_layout)
        main_layout.addLayout(stat_layout)

        self.setMaximumWidth(420)


class StatCard(QFrame):
    def __init__(self, title, value):
        super().__init__()

        self.setObjectName("statCard")

        title_label = QLabel(title)
        title_label.setObjectName("statTitle")

        value_label = QLabel(value)
        value_label.setObjectName("statValue")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(1)

        layout.addWidget(title_label)
        layout.addWidget(value_label)


class Product:
    def __init__(self, name, carbs_per_100g):
        self.name = name
        self.carbs_per_100g = carbs_per_100g

    def calculate_carbohydrates(self, weight):
        return round(weight * self.carbs_per_100g / 100, 1)

    def calculate_bread_units(self, weight, bread_units_value):
        carbohydrates = self.calculate_carbohydrates(weight)
        return round(carbohydrates / bread_units_value, 1)


class ProductHistory:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def find_product(self, name):
        for product in self.products:
            if product.name.lower() == name.lower():
                return product

        return None

    def get_products(self):
        return self.products

    def import_history(self):
        file_path = Path(__file__).parent / "data" / "products.json"

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            print("History file not found:", file_path)
            return

        self.products = [
            Product(item["name"], item["carbs_per_100g"])
            for item in data
            if (isinstance(item, dict) and "name" in item and "carbs_per_100g" in item)
        ]

    def export_history(self, file_path="./data/products.json"):
        data = [
            {"name": product.name, "carbs_per_100g": product.carbs_per_100g}
            for product in self.products
        ]

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)


class ProductDialog(QDialog):

    def __init__(self, parent=None, history: ProductHistory = None):
        super().__init__(parent)

        self.history = history
        self.selected_product = None

        self.setWindowTitle("Add Product")
        self.setModal(True)
        self.setMinimumWidth(380)

        self.setObjectName("productDialog")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        self.name_input = QLineEdit()
        self.name_input.setObjectName("productInput")
        self.name_input.setPlaceholderText("Product Name")

        # =========================
        # Name Completer
        # =========================

        self.completer = QCompleter(self)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.completer.activated.connect(self.product_selected)

        self.name_input.setCompleter(self.completer)

        self.update_completer()

        # =========================
        # Name Completer
        # =========================

        self.carbs_input = QLineEdit()
        self.carbs_input.setObjectName("productInput")
        self.carbs_input.setPlaceholderText("Carbohydrates per 100 g (g)")

        self.weight_input = QLineEdit()
        self.weight_input.setObjectName("productInput")
        self.weight_input.setPlaceholderText("Weight (g)")

        self.add_button = QPushButton("Add")
        self.add_button.setObjectName("dialogAddButton")
        self.add_button.clicked.connect(self.validate_and_accept)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName("dialogCancelButton")
        self.cancel_button.clicked.connect(self.reject)

        layout.addWidget(self.name_input)
        layout.addWidget(self.carbs_input)
        layout.addWidget(self.weight_input)
        layout.addSpacing(8)
        layout.addWidget(self.add_button)
        layout.addWidget(self.cancel_button)

    def update_completer(self):
        names = [product.name for product in self.history.get_products()]

        model = QStringListModel(names, self.completer)
        self.completer.setModel(model)

    def product_selected(self, name):
        product = self.history.find_product(name)

        if product is None:
            return

        self.selected_product = product

        self.name_input.setText(product.name)
        self.carbs_input.setText(str(product.carbs_per_100g))

    def validate_and_accept(self):
        name = self.name_input.text().strip()
        weight = self.weight_input.text().strip()
        carbs = self.carbs_input.text().strip()

        if not name:
            QMessageBox.warning(
                self,
                "Error",
                "Enter product name.",
            )
            self.name_input.setFocus()
            return

        try:
            weight = float(weight)
        except ValueError:
            QMessageBox.warning(
                self,
                "Error",
                "Weight must be a number.",
            )
            self.weight_input.setFocus()
            return

        if weight <= 0:
            QMessageBox.warning(
                self,
                "Error",
                "Weight must be greater than 0.",
            )
            self.weight_input.setFocus()
            return

        try:
            carbs = float(carbs)
        except ValueError:
            QMessageBox.warning(
                self,
                "Error",
                "Carbohydrates must be a number.",
            )
            self.carbs_input.setFocus()
            return

        if carbs < 0:
            QMessageBox.warning(
                self,
                "Error",
                "Carbohydrates cannot be negative.",
            )
            self.carbs_input.setFocus()
            return

        if self.selected_product is not None:
            self.product = self.selected_product
        else:
            self.product = Product(name=name, carbs_per_100g=carbs)
            self.history.add_product(self.product)
            self.history.export_history()

        self.accept()

    def get_product_data(self):
        return self.product, float(self.weight_input.text())
