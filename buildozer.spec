[app]
title = Mini SudoKemistry
package.name = minisudokemistry
package.domain = monigames_informatik
source.dir = .
source.include_exts = py,png,jpg,ttf
version = 1.0.0

# Requisitos importantes para o Pygame rodar no Android
requirements = python3,pygame,kivy

orientation = portrait
fullscreen = 1

# Permissões necessárias para exibir anúncios do Google AdMob
android.permissions = INTERNET, ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 21