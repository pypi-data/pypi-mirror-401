# ai-soulmate-sketch-filter

A Python library designed to demonstrate the core functionalities of AI-powered soulmate sketch generation and provide a seamless integration point for exploring the SuperMaker AI's soulmate drawing tool. This package offers a simplified interface to experiment with generating potential soulmate sketches based on various input parameters.

## Installation

Install the package using pip:
bash
pip install ai-soulmate-sketch-filter

## Basic Usage Examples

Here are a few examples showcasing how to use the `ai-soulmate-sketch-filter` package:

**1. Generating a basic soulmate sketch with default settings:**
python
from ai_soulmate_sketch_filter import SoulmateSketchGenerator

generator = SoulmateSketchGenerator()
sketch = generator.generate_sketch()

# sketch is a PIL Image object.  You can save it to a file.
sketch.save("soulmate_default.png")
print("Generated and saved a default soulmate sketch to soulmate_default.png")

**2. Generating a sketch with specific age and gender preferences:**
python
from ai_soulmate_sketch_filter import SoulmateSketchGenerator

generator = SoulmateSketchGenerator()
sketch = generator.generate_sketch(age_range=(25, 35), gender="female")

sketch.save("soulmate_age_gender.png")
print("Generated and saved a soulmate sketch (female, 25-35) to soulmate_age_gender.png")

**3. Generating a sketch with custom facial feature hints (experimental):**
python
from ai_soulmate_sketch_filter import SoulmateSketchGenerator

generator = SoulmateSketchGenerator()
sketch = generator.generate_sketch(facial_features={"eyes": "almond", "hair": "brunette"})

sketch.save("soulmate_facial_features.png")
print("Generated and saved a soulmate sketch with specified facial features to soulmate_facial_features.png")

**4. Controlling the randomness seed for reproducible results:**
python
from ai_soulmate_sketch_filter import SoulmateSketchGenerator

generator1 = SoulmateSketchGenerator(seed=42)
sketch1 = generator1.generate_sketch()
sketch1.save("soulmate_seed_42_1.png")

generator2 = SoulmateSketchGenerator(seed=42)
sketch2 = generator2.generate_sketch()
sketch2.save("soulmate_seed_42_2.png")

# sketch1 and sketch2 will be identical (if no other parameters are changed)
print("Generated two identical soulmate sketches using the same seed.")

**5. Generating a sketch with a preferred ethnicity (experimental):**
python
from ai_soulmate_sketch_filter import SoulmateSketchGenerator

generator = SoulmateSketchGenerator()
sketch = generator.generate_sketch(ethnicity="asian")

sketch.save("soulmate_ethnicity_asian.png")
print("Generated and saved a soulmate sketch with 'asian' ethnicity to soulmate_ethnicity_asian.png")

## Feature List

*   Generates a potential soulmate sketch based on AI algorithms.
*   Provides options to specify age range, gender, and ethnicity preferences.
*   Allows for experimental specification of facial feature hints.
*   Offers seed control for reproducible results.
*   Returns a PIL Image object for easy saving and manipulation.
*   Simple and easy-to-use API.

## License

MIT

This project is a gateway to the ai-soulmate-sketch-filter ecosystem. For advanced features and full capabilities, please visit: https://supermaker.ai/image/blog/ai-soulmate-drawing-free-tool-generate-your-soulmate-sketch/