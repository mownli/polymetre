# polymetre
PyFltk-based polyrhythmic metronome for music practice

![16-34-31](https://user-images.githubusercontent.com/101254975/157452157-e2ccbb0c-2062-44d2-bf57-9d85fea3d9eb.png)
## Dependencies
- python3
- numpy
- sounddevice
## Build/Installation
Extract the source code. Navigate to project's directory. Then run:

```
python setup.py bdist_wheel
pip install dist/*.whl
```

OR if you have all the dependencies installed:

```
make pyz
make install
```
In that case installation directory is ~/.local/bin
