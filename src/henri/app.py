import picoweb


class Henri(picoweb.WebApp):
    def init(self):
        self.push_event = None
        super().init()


APP = Henri(__name__)
