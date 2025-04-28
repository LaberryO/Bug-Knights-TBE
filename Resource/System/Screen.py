# 화면 사이즈 객체

from Resource import Exception

class Screen:
    def __init__(self, width, height):
        self._width = width
        self._height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if value > 0:
            self._width = value
        else:
            Exception.ValueException("width")

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if value > 0:
            self._height = value
        else:
            Exception.ValueException("height")

    @property
    def size(self):
        return (self._width, self._height)

    @property
    def centerX(self):
        return self._width / 2
    
    @property
    def centerY(self):
        return self._height / 2