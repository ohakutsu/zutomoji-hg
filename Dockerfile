FROM archlinux:base-devel

RUN pacman -Syu --noconfirm && pacman -S --noconfirm fontforge

ARG user=dockeruser
RUN useradd -m -s /bin/bash "${user}"
USER "${user}"

WORKDIR /zutomoji-hg

CMD ["./patch.py"]
