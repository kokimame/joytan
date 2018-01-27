PREFIX=/usr/local

all:
	@echo "You can run Joytan with ./bin/joytan"
	@echo "If you wish to install it system wide, type 'sudo make install'"
	@echo "Uninstall with 'sudo make uninstall'"

install:
	rm -rf ${PREFIX}/share/joytan
	mkdir -p ${PREFIX}/share/joytan
	cp -av * ${PREFIX}/share/joytan/
	mkdir -p ${PREFIX}/bin
	ln -sf ${PREFIX}/share/joytan/bin/joytan ${PREFIX}/bin/
	mkdir -p ${PREFIX}/share/pixmaps
	mkdir -p ${PREFIX}/share/applications
	cd ${PREFIX}/share/joytan && (\
		mv joytan.xpm joytan.png ${PREFIX}/share/pixmaps;\
		mv joytan.desktop ${PREFIX}/share/applications/)
	xdg-mime install joytan.xml --novendor
	xdg-mime default joytan.desktop applications/x-joytan
	@echo
	@echo "Install complete. Type 'joytan' to run."

uninstall:
	-xdg-mime uninstall ${PREFIX}/share/joytan/joytan.xml
	rm -rf ${PREFIX}/share/joytan
	rm -rf ${PREFIX}/bin/joytan
	rm -rf ${PREFIX}/share/pixmaps/joytan.xpm
	rm -rf ${PREFIX}/share/pixmaps/joytan.png
	rm -rf ${PREFIX}/share/applications/joytan.desktop
	@echo
	@echo "Uninstall complete. Thank you for using Joytan."
