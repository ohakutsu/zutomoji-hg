FROM archlinux:base-devel

RUN pacman -Syu --noconfirm && pacman -S --noconfirm fontforge

WORKDIR /zutomoji-hg

CMD ["./patch.py"]
