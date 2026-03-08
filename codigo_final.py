# ============================================
# GALACTIC DOMINATION - BOT PARA RAILWAY
# Versión con ahorro automático de horas
# ============================================

import requests
import json
import time
import sys
import os
from datetime import datetime, timedelta
from threading import Thread

# ============================================
# CONFIGURACIÓN DE AHORRO DE HORAS
# ============================================
INICIO = datetime.now()
ULTIMA_ACTIVIDAD = datetime.now()
HORAS_MAXIMAS_CONTINUAS = 16  # Se apaga después de 16h seguidas
MINUTOS_INACTIVIDAD_MAX = 45   # Se apaga si nadie habla en 45 minutos
MODO_PRUEBA = False            # Cambiar a True solo para pruebas rápidas

def verificar_limites():
    """Verifica si debemos apagar el bot para ahorrar horas"""
    ahora = datetime.now()
    
    # 1. Verificar límite de horas continuas
    horas_transcurridas = (ahora - INICIO).total_seconds() / 3600
    if horas_transcurridas >= HORAS_MAXIMAS_CONTINUAS and not MODO_PRUEBA:
        print(f"\n⏰ Límite de {HORAS_MAXIMAS_CONTINUAS}h alcanzado. Apagando para ahorrar horas...")
        print("Railway reiniciará automáticamente cuando haya disponibilidad.")
        sys.exit(0)
    
    # 2. Verificar inactividad
    minutos_inactivo = (ahora - ULTIMA_ACTIVIDAD).total_seconds() / 60
    if minutos_inactivo >= MINUTOS_INACTIVIDAD_MAX and not MODO_PRUEBA:
        print(f"\n💤 {MINUTOS_INACTIVIDAD_MAX} minutos sin actividad. Apagando para ahorrar horas...")
        sys.exit(0)

def actualizar_actividad():
    """Llama a esta función cada vez que hay interacción"""
    global ULTIMA_ACTIVIDAD
    ULTIMA_ACTIVIDAD = datetime.now()

# ============================================
# CONFIGURACIÓN DEL BOT
# ============================================
TOKEN = os.environ.get('TOKEN', "8330954795:AAHANv63h9F1BBpQuOFasc1fNNwHwBD2KUw")
API = f"https://api.telegram.org/bot{TOKEN}"

print("=" * 50)
print("🚀 GALACTIC DOMINATION - BOT PARA RAILWAY")
print("=" * 50)
print(f"✅ Bot iniciado: {INICIO.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"✅ Límite continuo: {HORAS_MAXIMAS_CONTINUAS}h")
print(f"✅ Inactividad máxima: {MINUTOS_INACTIVIDAD_MAX}min")
print("✅ Esperando mensajes...")
print("=" * 50)

# ============================================
# FUNCIONES AUXILIARES
# ============================================
def enviar_menu(chat_id):
    keyboard = {
        "inline_keyboard": [
            [{"text": "👤 Mi Perfil", "callback_data": "perfil"}],
            [{"text": "⚔️ Elegir Raza", "callback_data": "razas"}],
            [{"text": "🏰 Mi Base", "callback_data": "base"}],
            [{"text": "🔧 Construir", "callback_data": "construir"}]
        ]
    }
    requests.post(f"{API}/sendMessage", json={
        "chat_id": chat_id,
        "text": "🎮 **GALACTIC DOMINATION**\nElige una opción:",
        "parse_mode": "Markdown",
        "reply_markup": json.dumps(keyboard)
    })
    actualizar_actividad()

def enviar_perfil(chat_id, username):
    texto = (
        f"👤 **PERFIL DE GUERRERO**\n\n"
        f"📛 Usuario: @{username}\n"
        f"⚔️ Raza: Equilibrada\n"
        f"📊 Nivel: 1\n"
        f"💪 Poder: 1000\n"
        f"💰 $GALAX: 100\n"
        f"🏰 Base: Nivel 1\n"
        f"👥 Alianza: Sin alianza"
    )
    requests.post(f"{API}/sendMessage", json={
        "chat_id": chat_id,
        "text": texto,
        "parse_mode": "Markdown"
    })
    actualizar_actividad()

def mostrar_razas(chat_id, message_id):
    keyboard = {
        "inline_keyboard": [
            [{"text": "⚔️ Ofensiva (+20% ataque)", "callback_data": "raza_offensive"}],
            [{"text": "⚖️ Equilibrada (+10% todo)", "callback_data": "raza_balanced"}],
            [{"text": "🛡️ Defensiva (+20% defensa)", "callback_data": "raza_defensive"}],
            [{"text": "🔙 Volver", "callback_data": "volver_menu"}]
        ]
    }
    requests.post(f"{API}/editMessageText", json={
        "chat_id": chat_id,
        "message_id": message_id,
        "text": "🌟 **ELIGE TU RAZA**",
        "parse_mode": "Markdown",
        "reply_markup": json.dumps(keyboard)
    })
    actualizar_actividad()

def mostrar_base(chat_id, message_id):
    texto = (
        "🏰 **BASE ESPACIAL**\n\n"
        "📊 Nivel: 1\n"
        "⚡ Energía: 1000/1000\n"
        "🔬 Investigación: Nivel 1\n\n"
        "🚀 **NAVES**\n"
        "🛩️ Cazas: 10\n"
        "💥 Destructores: 0\n"
        "🛡️ Acorazados: 0\n\n"
        "⏱️ Producción: 10 $GALAX/hora"
    )
    keyboard = {
        "inline_keyboard": [
            [{"text": "🔧 Construir", "callback_data": "construir"}],
            [{"text": "🔙 Volver", "callback_data": "volver_menu"}]
        ]
    }
    requests.post(f"{API}/editMessageText", json={
        "chat_id": chat_id,
        "message_id": message_id,
        "text": texto,
        "parse_mode": "Markdown",
        "reply_markup": json.dumps(keyboard)
    })
    actualizar_actividad()

def mostrar_construccion(chat_id, message_id):
    keyboard = {
        "inline_keyboard": [
            [{"text": "🛩️ Cazas (50⚡)", "callback_data": "build_fighter"}],
            [{"text": "💥 Destructores (200⚡)", "callback_data": "build_destroyer"}],
            [{"text": "🛡️ Acorazados (500⚡)", "callback_data": "build_battleship"}],
            [{"text": "🏰 Mejorar Base (1000⚡)", "callback_data": "build_base"}],
            [{"text": "🔬 Investigar (500⚡)", "callback_data": "build_research"}],
            [{"text": "🔙 Volver", "callback_data": "volver_menu"}]
        ]
    }
    requests.post(f"{API}/editMessageText", json={
        "chat_id": chat_id,
        "message_id": message_id,
        "text": "🔧 **CONSTRUCCIÓN**\nElige qué construir:",
        "parse_mode": "Markdown",
        "reply_markup": json.dumps(keyboard)
    })
    actualizar_actividad()

# ============================================
# BUCLE PRINCIPAL CON VERIFICACIÓN DE LÍMITES
# ============================================
ultimo_id = 0

while True:
    try:
        # Verificar si debemos apagar el bot
        verificar_limites()
        
        # Obtener mensajes nuevos
        respuesta = requests.get(f"{API}/getUpdates", params={
            "offset": ultimo_id + 1,
            "timeout": 30
        }, timeout=35)
        
        updates = respuesta.json().get("result", [])
        
        for update in updates:
            # ===== MENSAJES DE TEXTO =====
            if "message" in update and "text" in update["message"]:
                chat_id = update["message"]["chat"]["id"]
                texto = update["message"]["text"]
                username = update["message"]["from"].get("username", "Jugador")
                
                print(f"\n📩 @{username}: {texto}")
                actualizar_actividad()
                
                if texto == "/start":
                    requests.post(f"{API}/sendMessage", json={
                        "chat_id": chat_id,
                        "text": f"🚀 ¡Bienvenido @{username} a GALACTIC DOMINATION!\n\nUsa /menu para comenzar."
                    })
                elif texto == "/menu":
                    enviar_menu(chat_id)

            # ===== BOTONES =====
            if "callback_query" in update:
                cb = update["callback_query"]
                chat_id = cb["message"]["chat"]["id"]
                message_id = cb["message"]["message_id"]
                data = cb["data"]
                username = cb["from"].get("username", "Jugador")
                
                # Responder al callback
                requests.post(f"{API}/answerCallbackQuery", json={
                    "callback_query_id": cb["id"]
                })
                
                print(f"🔘 @{username} presionó: {data}")
                actualizar_actividad()
                
                if data == "perfil":
                    enviar_perfil(chat_id, username)
                elif data == "razas":
                    mostrar_razas(chat_id, message_id)
                elif data == "base":
                    mostrar_base(chat_id, message_id)
                elif data == "construir":
                    mostrar_construccion(chat_id, message_id)
                elif data == "volver_menu":
                    enviar_menu(chat_id)
                elif data.startswith("raza_"):
                    raza = data.replace("raza_", "")
                    nombres = {
                        "offensive": "⚔️ Ofensiva",
                        "balanced": "⚖️ Equilibrada",
                        "defensive": "🛡️ Defensiva"
                    }
                    texto = f"✅ ¡Ahora eres de la raza **{nombres[raza]}**!"
                    keyboard = {
                        "inline_keyboard": [
                            [{"text": "🔙 Volver", "callback_data": "volver_menu"}]
                        ]
                    }
                    requests.post(f"{API}/editMessageText", json={
                        "chat_id": chat_id,
                        "message_id": message_id,
                        "text": texto,
                        "parse_mode": "Markdown",
                        "reply_markup": json.dumps(keyboard)
                    })
            
            ultimo_id = update["update_id"]
            
    except KeyboardInterrupt:
        print("\n👋 Bot detenido manualmente")
        break
    except Exception as e:
        print(f"❌ Error: {e}")
        time.sleep(5)