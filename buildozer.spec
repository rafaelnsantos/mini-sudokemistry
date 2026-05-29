# Força o uso do NDK 25b, que é a versão mais estável e recomendada para Pygame/SDL2
android.ndk = 25b

# Garante que as APIs de build usem versões compatíveis
android.permissions = INTERNET, ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 21
android.sdk = 33

# Se a sua linha "requirements" estiver muito carregada, deixe-a simples assim por enquanto:
requirements = python3,pygame
