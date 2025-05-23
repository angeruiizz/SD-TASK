from xmlrpc.server import SimpleXMLRPCServer

class InsultFilter:
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

server = SimpleXMLRPCServer(("localhost", 9000), allow_none=True)
service = InsultFilter()
server.register_instance(service)
print("Insult XML-RPC Server is running on port 9000...")
server.serve_forever()
