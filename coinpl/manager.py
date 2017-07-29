from coinpl import connect


class CutManager(object):

    def __init__(self, app):
        self.app = app
        self.eng = connect(self.app)

    def calculate(self, effective):
        """ Calculate holdings and PL and generate Cuts
        :param effective:
        :return:
        """