CXX = g++
CXXFLAGS = -std=c++11 -Wall
TARGET = snake
SRCDIR = src
INCDIR = include

$(TARGET): $(SRCDIR)/snake.cpp
	$(CXX) $(CXXFLAGS) -I$(INCDIR) -o $(TARGET) $(SRCDIR)/snake.cpp

clean:
	rm -f $(TARGET)

run: $(TARGET)
	./$(TARGET)
