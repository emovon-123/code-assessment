# Kandinsky-Style Air Quality Abstract Art
## 康定斯基风格空气质量抽象艺术

Transform air quality data into Kandinsky-style abstract geometric shapes and line variations, creating pure artistic expression.

## Project Overview

This project transforms the UCI Beijing Multi-Site Air Quality dataset into Kandinsky-style abstract art, displaying no place names, data, or letters, purely expressing air quality changes through geometric shapes, lines, and color variations.

## Artistic Style

### 🎨 Kandinsky Abstract Elements
- **Abstract Circles**: Multi-layered circular structures based on PM2.5 concentration changes
- **Abstract Triangles**: Based on SO2 concentration and temperature variations
- **Abstract Rectangles**: Reflecting NO2 concentration and humidity changes
- **Abstract Lines**: Expressing dynamic changes in wind speed and direction
- **Abstract Polygons**: Complex geometric shapes based on O3 concentration

### 🌈 Color System
- **Primary Colors**: Red, cyan, blue, green, yellow, purple
- **Secondary Colors**: Orange, purple, pink, gold, etc.
- **Accent Colors**: Dynamically adjusted based on pollutant concentrations
- **Background Color**: Beige background (#e5dbc3), highlighting geometric shapes

### 🔄 Dynamic Changes
- **Geometric Shapes**: Real-time changes in size, position, and rotation angles
- **Color Gradients**: Adjusting colors and transparency based on data intensity
- **Flowing Lines**: Wind-driven dynamic line effects
- **Background Gradients**: Visual feedback of overall pollution levels

## Data Mapping

### Pollutants to Artistic Elements
- **PM2.5 → Circles**: Primary pollutant, expressed through circles
- **SO2 → Triangles**: Sharp triangular expression
- **NO2 → Rectangles**: Stable rectangular structure
- **CO → Lines**: Flowing line effects
- **O3 → Polygons**: Complex polygonal shapes

### Meteorological Data to Visual Effects
- **Temperature**: Affects shape size and transparency
- **Humidity**: Adjusts shape transparency
- **Wind Speed**: Controls line length and thickness
- **Wind Direction**: Determines line and shape movement direction

## File Structure

```
weather_art_project/
├── kandinsky_air_art.py        # Kandinsky-style abstract art (animation version)
├── kandinsky_art_save.py       # Kandinsky-style abstract art (save version)
├── beijing_air_quality_art.py  # Basic air quality visualization
├── requirements.txt            # Project dependencies
├── .gitignore                  # Git ignore file
└── README.md                   # Project documentation
```

## Installation and Running

### Requirements
- Python 3.7+
- matplotlib
- numpy
- pandas
- seaborn
- scipy

### Installation Steps

1. **Clone the project**
```bash
git clone https://github.com/emovon-123/code-assessment.git
cd code-assessment
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the program**

#### Kandinsky-Style Abstract Art (Recommended)
```bash
python kandinsky_air_art.py
```

#### Save Image Version
```bash
python kandinsky_art_save.py
```

#### Basic Air Quality Visualization
```bash
python beijing_air_quality_art.py
```

## Usage Instructions

### Kandinsky-Style Version
- Pure abstract artistic expression with no text or data
- Dynamic changes in geometric shapes and lines
- Real-time adjustment based on air quality data
- 1000ms interval updates for smooth animation effects
- Press Ctrl+C to stop animation

### Artistic Features
- **Pure Abstraction**: No specific information displayed
- **Geometric Aesthetics**: Circles, triangles, rectangles, polygons
- **Color Harmony**: Kandinsky-style color combinations
- **Dynamic Changes**: Real-time response to data changes
- **Visual Impact**: Strong artistic expression

## Technical Implementation

### Abstract Shape Generation
- **Circle System**: Multi-layered circular structures with nested inner and outer circles
- **Triangle System**: Equilateral triangles with rotation support
- **Rectangle System**: Rectangular elements with dynamic rotation
- **Line System**: Wind-based flowing lines
- **Polygon System**: 5-8 sided complex geometry

### Color Mapping Algorithm
- **Value to Color**: Mapping pollutant concentrations to color palette
- **Transparency Control**: Adjusting based on humidity and temperature
- **Background Gradients**: Visual feedback of overall pollution levels
- **Dynamic Coloring**: Real-time color changes

### Animation System
- **Frame Rate Control**: 1000ms intervals
- **Element Updates**: Regenerating abstract elements each frame
- **Smooth Transitions**: Avoiding abrupt changes
- **Performance Optimization**: Efficient rendering algorithms

## Artistic Philosophy

### Kandinsky Influence
- **Geometric Abstraction**: Pure geometric forms
- **Color Theory**: Connection between colors and emotions
- **Dynamic Balance**: Balance between static and dynamic
- **Inner Expression**: Expressing inner feelings through abstraction

### Data Art
- **Information Visualization**: Converting data into visual art
- **Abstract Expression**: Artistic expression beyond specific information
- **Emotional Communication**: Conveying emotions through colors and shapes
- **Aesthetic Pursuit**: Pursuing pure aesthetic experience

## Extended Features

### Future Plans
- [ ] Add more abstract shape types
- [ ] Implement 3D abstract art
- [ ] Add audio visualization
- [ ] Support interactive controls
- [ ] Implement artistic style switching
- [ ] Add particle system effects

### Custom Extensions
- Modify `kandinsky_colors` palette
- Adjust abstract shape generation algorithms
- Extend geometric shape types
- Customize animation effects

## Contributing

Welcome to contribute code, report issues, or make suggestions!

1. Fork the project
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Create a Pull Request

## License

This project is licensed under the MIT License

## Acknowledgments

- Thanks to Kandinsky's abstract art theory
- Thanks to UCI Machine Learning Repository for providing the dataset
- Thanks to the matplotlib community for the excellent visualization library
- Thanks to all developers who contribute to open source projects

## Contact

For questions or suggestions, please contact us through:
- Submit an Issue
- Send an email
- Participate in discussions

---
