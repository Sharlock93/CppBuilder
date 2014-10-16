HDRDIR = C:\dev\lib\include\Shar C:\dev\lib\include\GLFW s C:\dev\lib\include\Shar C:\dev\lib\include\GLFW s
OBJ = $(subst .cpp,.o,$(SOURCE))$(subst .cpp,.o,$(SOURCE))
SOURCE = hjhj.cpp somelib.cpp
COMMANDC = g++ -cg++ -c

App.exe : $(OBJ) 
	 g++ $(OBJ) -o App.exe

hjhj.o: hjhj.cpp
	$(COMMANDC) hjhj.cpp

somelib.o: somelib.cpp
	$(COMMANDC) somelib.cpp

