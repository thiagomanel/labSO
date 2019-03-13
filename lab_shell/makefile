xeu: *.cpp xeu-utils
	g++ *.cpp *.o -o xeu
	rm -f *.o

test: xeu-utils-tests xeu_utils/__tests__/__lib__/main.cpp
	g++ --std=c++11 *.o xeu_utils/__tests__/__lib__/main.cpp -o tests-bin
	rm -f *.o
	./tests-bin
	rm -f tests-bin

xeu-utils: xeu_utils/*.cpp
	g++ xeu_utils/*.cpp -c

xeu-utils-tests: xeu-utils xeu_utils/__tests__/*.cpp
	g++ --std=c++11 xeu_utils/__tests__/*.cpp -c

clean:
	rm -f xeu tests-bin *.o

$(V).SILENT: