from xmlrpc.server import SimpleXMLRPCServer
import time
import random

INSULTS = ["Tonto", "Cap de suro", "Inútil", "BocaChancla", "idiota", "estúpido", "imbécil", "gilipollas"]

class InsultFiltter:
    def __init__(self):
        self.texts = []
        self.textsFilt = []

    def add_text(self, text):
            if text not in self.texts:
                self.texts.append(text)
                # Check if the text contains any insults
                if self.contains_insult(text):
                    # Clean the text
                    cleaned_text = self.clean_text(text)
                    self.textsFilt.append(cleaned_text)
                    print(f"Text contained insults. Filtered: {cleaned_text}")
                    return f"Filtered text: {cleaned_text}"
                else:
                    self.textsFilt.append(text)
                    print(f"Clean text added: {text}")
                    return f"Added clean text: {text}"
            else:
                 if self.contains_insult(text):
                    cleaned_text = self.clean_text(text)
                    print(f"Text already exists, filtered version: {cleaned_text}")
                    return f"Already exists. Filtered text: {cleaned_text}"
                 else:
                    print(f"Text {text} already exists and is clean.")
                    return f"Already exists. Clean text: {text}"


    def get_texts(self):
        return self.texts
    
    def get_texts_filt(self):
        return self.textsFilt
    
    def contains_insult(self, text):
        for insult in INSULTS:
            if insult in text:
                return True
        return False    

    #Remplaza les insultos por "CENSURADO"
    def clean_text(self, text):
        for insult in INSULTS:
            text = text.replace(insult, "CENSORED")
            text = text.replace(insult.lower(), "CENSORED")
            text = text.replace(insult.capitalize(), "CENSORED")
        return text

# Crear el servidor XML-RPC
server = SimpleXMLRPCServer(("localhost", 9000), allow_none=True)
server.register_introspection_functions()

# Registrar el servicio
service = InsultFiltter()
server.register_instance(service)

print("Insult XML-RPC Server is running on port 9000...")
server.serve_forever()

# Dentro de la función add_text()
print(f"Recibido texto: {text}")