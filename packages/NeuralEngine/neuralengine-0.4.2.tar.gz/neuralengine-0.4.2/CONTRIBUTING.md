# Contribution Guide

NeuralEngine is an open-source project, and I warmly welcome all kinds of contributions whether it's code, documentation, bug reports, feature ideas, or sharing cool examples. If you want to help make NeuralEngine better, you're in the right place!

## How to Contribute
1. **Fork the repository** and create a new branch for your feature, fix or documentation update.  
2. **Keep it clean and consistent**: Try to follow the existing code style, naming conventions and documentation patterns. Well-commented, readable code is always appreciated!  
3. **Add tests** for new features or bug fixes if you can.  
4. **Document your changes**: Update or add docstrings and README sections so others can easily understand your work.  
5. **Open a pull request** describing what you've changed and why it's awesome.

## Development Setup
To start coding, you'll need **Python 3.10+**.

1. **Fork & Clone**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/NeuralEngine.git  
   cd NeuralEngine
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv 
   # Windows  
   venv\Scripts\activate  
   # macOS/Linux  
   source venv/bin/activate
   ```

3. **Install Dependencies**:  
   ```bash
   pip install -r requirements.txt
   ```

4. **Install in Editable Mode**: This is crucial! It allows you to modify the code and see changes immediately without reinstalling.  
   ```bash
   pip install -e .
   ```

## Coding Standards
To maintain the quality and performance of NeuralEngine, please follow these technical guidelines:

- **Type Hinting**: This project uses a custom `Typed` metaclass (`neuralengine.config.Typed`) for runtime validation. All new functions and methods **must** include Python type hints.
  ```python
  # Good
  def my_function(x: Tensor, alpha: float = 0.1) -> Tensor: ...
  ```

- **Device Agnostic Code**: Do not import `numpy` or `cupy` directly for tensor operations. Use the backend provider `xp` defined in `config.py`.
  ```python
  import neuralengine.config as cf  
  # ...  
  data = cf.xp.zeros((10, 10)) # Automatically handles CPU/GPU
  ```

## What Can You Contribute?
- New layers, loss functions, optimizers, metrics, or utility functions  
- Improvements to existing components  
- Bug fixes and performance tweaks  
- Documentation updates and tutorials  
- Example scripts and notebooks  
- Feature requests, feedback and ideas

Every contribution is reviewed for quality and consistency, but don't worry—if you have questions or need help, just open an issue or start a discussion. I'm happy to help and love seeing new faces in the community!

Thanks for making NeuralEngine better, together! 🚀