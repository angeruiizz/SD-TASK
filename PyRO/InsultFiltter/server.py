import Pyro4

@Pyro4.expose
class InsultFilter(object):
    def __init__(self):
        self.work_queue = []
        self.results = []
    
    def enqueue_text(self, text):
        self.work_queue.append(text)
        print(f"Enqueued: {text}")
        return "Text enqueued."

    def get_next_text(self):
        if self.work_queue:
            text = self.work_queue.pop(0)
            print(f"Dispatched to worker: {text}")
            return text
        else:
            return None
    
    def submit_result(self, clean_text):
        self.results.append(clean_text)
        print(f"Result saved: {clean_text}")
        return "Result saved."
    
    def get_results(self):
        return self.results

def main():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    obj = InsultFilter()  #registrar una instancia unicaa
    uri = daemon.register(obj) 
    ns.register("example.insult_filter", uri)
    print("InsultFilter server running.")
    daemon.requestLoop()


if __name__ == "__main__":
    main()
