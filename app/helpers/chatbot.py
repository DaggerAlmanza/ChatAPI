import re
import random


class ChatBot:
    def __init__(self):
        # Diccionario con patrones y respuestas posibles
        self.responses = {
            # Saludos
            "saludos": {
                "patrones": [
                    "hola", "buenas", "buenos días", "buenas tardes",
                    "buenas noches", "qué tal", "hey", "hi"
                ],
                "respuestas": [
                    "¡Hola! ¿En qué te puedo ayudar?",
                    "¡Buenas! ¿Cómo estás?",
                    "¡Hola! Espero que tengas un buen día.",
                    "¡Hey! ¿Qué necesitas?"
                ]
            },

            # Despedidas
            "despedidas": {
                "patrones": [
                    "adiós", "chao", "hasta luego",
                    "nos vemos", "bye", "me voy"
                ],
                "respuestas": [
                    "¡Hasta luego! Que tengas un buen día.",
                    "¡Adiós! Fue un placer ayudarte.",
                    "¡Nos vemos! Cuídate mucho.",
                    "¡Chao! Vuelve cuando necesites algo."
                ]
            },

            # Agradecimientos
            "agradecimientos": {
                "patrones": [
                    "gracias", "thank you", "te agradezco", "muy amable"
                ],
                "respuestas": [
                    "¡De nada! Siempre es un placer ayudar.",
                    "¡No hay problema! Para eso estoy aquí.",
                    "¡Con gusto! ¿Necesitas algo más?",
                    "¡Es mi trabajo! Me alegra poder ayudarte."
                ]
            },

            # Cómo está
            "estado": {
                "patrones": ["cómo estás", "qué tal", "cómo te va", "cómo andas"],
                "respuestas": [
                    "¡Muy bien, gracias por preguntar! ¿Y tú?",
                    "Perfecto, listo para ayudarte. ¿Cómo estás tú?",
                    "Excelente, aquí para lo que necesites.",
                    "Todo bien por aquí. ¿En qué puedo ayudarte?"
                ]
            },

            # Preguntas sobre ayuda
            "ayuda": {
                "patrones": ["ayuda", "help", "auxilio", "necesito ayuda", "puedes ayudarme"],
                "respuestas": [
                    "¡Claro! Dime en qué te puedo ayudar.",
                    "Por supuesto, ¿cuál es tu consulta?",
                    "Estoy aquí para ayudarte. ¿Qué necesitas?",
                    "¡Con mucho gusto! Explícame tu situación."
                ]
            },

            # Información personal
            "quien_eres": {
                "patrones": ["quién eres", "qué eres", "who are you", "tu nombre"],
                "respuestas": [
                    "Soy un asistente virtual aquí para ayudarte.",
                    "Soy tu asistente personal, ¿en qué puedo ayudarte?",
                    "Soy un bot diseñado para resolver tus dudas.",
                    "Soy tu asistente digital. ¿Qué necesitas saber?"
                ]
            },

            # Problemas técnicos
            "problemas": {
                "patrones": ["problema", "error", "no funciona", "falla", "bug"],
                "respuestas": [
                    "Lamento escuchar que tienes problemas. ¿Puedes darme más detalles?",
                    "Entiendo tu frustración. ¿Qué exactamente no está funcionando?",
                    "Vamos a solucionarlo juntos. ¿Puedes describir el problema?",
                    "No te preocupes, te voy a ayudar. ¿Cuál es el error específicamente?"
                ]
            },

            # Tiempo/Clima
            "tiempo": {
                "patrones": ["clima", "tiempo", "lluvia", "sol", "temperatura"],
                "respuestas": [
                    "No tengo acceso a información del clima en tiempo real, pero puedes consultar una app del tiempo.",
                    "Para información precisa del clima, te recomiendo revisar tu app meteorológica favorita.",
                    "El clima cambia constantemente, mejor consulta un servicio meteorológico actualizado.",
                    "No puedo darte el clima actual, pero espero que tengas buen tiempo."
                ]
            },

            # Preguntas sobre el día
            "dia": {
                "patrones": ["qué día", "fecha", "today", "hoy"],
                "respuestas": [
                    "Puedes verificar la fecha en tu dispositivo o calendario.",
                    "No tengo acceso a la fecha actual, revisa tu reloj o calendario.",
                    "La fecha exacta la puedes ver en la esquina de tu pantalla.",
                    "Para la fecha actual, consulta tu dispositivo."
                ]
            },

            # Entretenimiento
            "entretenimiento": {
                "patrones": ["chiste", "diversión", "aburrido", "entretenimiento"],
                "respuestas": [
                    "¿Quieres que conversemos de algo interesante?",
                    "Podemos charlar sobre tus hobbies favoritos.",
                    "¿Te gustaría hablar de algún tema en particular?",
                    "¡Hagamos que esta conversación sea más divertida! ¿De qué quieres hablar?"
                ]
            }
        }

        # Respuestas por defecto cuando no se encuentra patrón
        self.responses_default = [
            "Interesante. ¿Puedes contarme más sobre eso?",
            "Entiendo. ¿En qué más te puedo ayudar?",
            "Hmm, ¿podrías ser más específico?",
            "No estoy seguro de entender completamente. ¿Puedes explicarme mejor?",
            "Esa es una pregunta interesante. ¿Qué opinas tú?",
            "Cuéntame más detalles sobre eso.",
            "¿Hay algo específico que quieras saber?",
            "Me parece importante lo que dices. ¿Qué más puedes agregar?",
            "¿En qué contexto te refieres a eso?",
            "¿Podrías darme un ejemplo de lo que mencionas?"
        ]

    def process_text(self, text):
        """Limpia y normaliza el texto de entrada"""
        text = text.lower().strip()
        # Remover signos de puntuación
        text = re.sub(r"[^\w\s]", '', text)
        return text

    def find_category(self, message):
        """Encuentra la categoría que mejor coincide con el mensaje"""
        clean_text = self.process_text(message)

        for category, data in self.responses.items():
            for patron in data["patrones"]:
                if patron in clean_text:
                    return category
        return None

    def get_response(self, mensaje):
        """Genera una respuesta basada en el mensaje recibido"""
        category = self.find_category(mensaje)

        if category:
            # Selecciona una respuesta aleatoria de la categoría encontrada
            possible_responses = self.responses[category]["respuestas"]
            return random.choice(possible_responses)
        # Si no encuentra patrón, usa respuesta por defecto
        return random.choice(self.responses_default)
