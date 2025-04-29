# insult_filter_server.py
import Pyro4

@Pyro4.expose
class InsultFilter:
    def __init__(self):
        self.insults = ["tonto", "estúpido", "imbécil", "idiota", "lento", "cap de suro", "gilipollas"]
        self.results = []

    def submit_text(self, text):
        """Filtra los insultos y guarda el texto limpio."""
        print(f"Received: {text}")
        for insult in self.insults:
            text = text.replace(insult, "CENSORED")
        self.results.append(text)
        print(f"Saved cleaned text: {text}")
        return "Text processed."

    def get_results(self):
        return self.results


# Inicializar el servidor Pyro
def main():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(InsultFilter)
    ns.register("example.insult_filter", uri)

    print("InsultFilter service is running...")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
