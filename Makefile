SOURCE = 
OBJ = $(subst .cpp,.o,$(SOURCE))
LIBS = -lglfw3 -lglew32s -lopengl32 -lgdi32
HDRDIR = -IC:\dev\lib\include
LIBS_DIR = -LC:\dev\lib\lib-glew\Release\x64 -LC:\dev\lib\lib-mingw
COMMANDC = g++ -c -std=gnu++11

App.exe: $(OBJ) 
	g++ $(OBJ) -o App.exe $(LIBS) $(LIBS_DIR)

