SRC=$(wildcard src/*.cpp)
OBJ=$(SRC:.cpp=.o)
TARGET=obd-log-86

.PHONY: all clean clobber

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $(LDFLAGS) -o $@ $^

clean:
	$(RM) $(OBJ)

clobber: clean
	$(RM) $(TARGET)
