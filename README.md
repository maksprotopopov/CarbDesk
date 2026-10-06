# LocalMind

### LocalMind is a desktop application for calculating carbohydrates and bread units (BU) in food products.

The application is being developed using Python and PySide6, with a focus on providing a simple and convenient way to manage products and perform nutritional calculations locally.

### Features

The following features are currently implemented:

* adding products to a calculation;
* entering product weight;
* automatic carbohydrate calculation;
* automatic bread unit (BU) calculation;
* displaying added products as cards;
* removing products from the current calculation;
* calculating total carbohydrates;
* calculating total bread units;
* storing and using product history;
* viewing previously added products;
* configuring the amount of carbohydrates corresponding to one bread unit;
* local storage of product data in JSON format.

### Interface

The application features a dark, minimalistic interface designed for desktop use.

#### The main screen contains:

* a calculation section;
* a list of added products;
* total calculation results;
* access to product history;
* application settings.

#### The “Image Analysis” section is currently under development.

### Technologies

* Python
* PySide6
* JSON for local data storage

### Data Structure

Product history is stored locally in:

```bash
data/products.json
```

Each product contains its name and the amount of carbohydrates per 100 grams.

Example:
``` json
[
    {
        "name": "Bread",
        "carbs_per_100g": 49
    },
    {
        "name": "Milk",
        "carbs_per_100g": 4.8
    }
]
```

## Development Status

The project is currently under active development.

The core functionality for product management and nutritional calculations has already been implemented. Additional features, including image analysis, are still being developed.

## Running the Application

Install the required project dependencies and run the main Python file:

```bash
python main.py
```

#### The project structure and launch process may change during further development.