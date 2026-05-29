[app]

# Força o uso do NDK 25b, estável para Pygame
android.ndk = 25b

# Informações básicas do seu jogo
title = Mini SudoKemistry
package.name = sudokemistry
package.domain = org.seu_nome
source.dir = .
source.include_exts = py,png,jpg,ttf
version = 1.0.0

# Requisitos do sistema
requirements = python3,pygame

android.p4a_extra_args = --exclude-recipes=sdl2_mixer,fluidsynth,libmodplug

orientation = portrait
fullscreen = 1

# Permissões de Internet e APIs
android.permissions = INTERNET, ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 21
android.sdk = 33
