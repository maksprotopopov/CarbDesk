# CarbDesk

### CarbDesk is a desktop application for calculating carbohydrates and bread units (BU) in food products.

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

This file is included in the application build and is used as the default product database on the first launch.

After the first launch, the application stores user-modified product data separately from the application files. This prevents the user’s product history from being lost when the application is updated or rebuilt.

### Windows

User product data is stored in:

```
%LOCALAPPDATA%\CarbDesk\products.json
```

For example:

```
C:\Users\<Username>\AppData\Local\CarbDesk\products.json
```

### MacOS

User product data is stored in:

```
~/Library/Application Support/CarbDesk/products.json
```

For example:

```
/Users/<Username>/Library/Application Support/CarbDesk/products.json
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

## Building the Application

The same PyInstaller specification file (CarbDesk.spec) can be used to build the application on both Windows and macOS.

However, PyInstaller builds applications for the platform on which it is executed. Therefore, the application must be built separately on each target operating system.

### Windows

Run the following command on Windows:

```bash
pyinstaller CarbDesk.spec
```

The resulting application will be located in:

```
dist/CarbDesk/
```

The executable can be launched using:

```
dist/CarbDesk/CarbDesk.exe
```

User-modified product data is stored separately in:

```
%LOCALAPPDATA%\CarbDesk\products.json
```

### MacOS

Run the following command on macOS:

```bash
pyinstaller CarbDesk.spec
```

The resulting application will be located in:

```
dist/CarbDesk.app
```

The executable can be launched using:

```bash
open dist/CarbDesk.app
```

Or directly from the terminal:

```bash
dist/CarbDesk.app/Contents/MacOS/CarbDesk
```

User-modified product data is stored separately in:

```
~/Library/Application Support/CarbDesk/products.json
```

## Creating a DMG on macOS

After successfully building the macOS application, a .dmg disk image can be created using create-dmg.

If create-dmg is not installed, install it with Homebrew:

```bash
brew install create-dmg
```

Then create the DMG:

```bash
create-dmg \
  --volname "CarbDesk" \
  --window-size 600 400 \
  --app-drop-link 450 200 \
  "CarbDesk.dmg" \
  "dist/CarbDesk.app"
```

The resulting file will be created in the current project directory:

```
CarbDesk.dmg
```

The .dmg contains the CarbDesk.app application and can be distributed to other macOS users.

## Running the Application from Source

Install the required project dependencies and run the main Python file:

```bash
python main.py
```

#### The project structure and launch process may change during further development.