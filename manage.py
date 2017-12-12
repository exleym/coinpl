# Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_script import Manager, Server, prompt_bool
from coinpl import create_app, connect
from coinpl.models import Base
from coinpl.external.gdax import GDAXDataManager
from coinpl.external.qndl import QuandlDataManager
from data import LocalDataManager

app = create_app()
manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0',
    port=8000,
    debug=True
))


@manager.command
def dbinit():
    eng = connect(app)
    Base.metadata.create_all(bind=eng)


@manager.command
def dbpopulate():
    eng = connect(app)
    mgr = GDAXDataManager(eng)
    qmgr = QuandlDataManager(eng, app)
    local_mgr = LocalDataManager(eng, app)
    mgr.populate_fixed_resources()
    local_mgr.fill_base_data()
    qmgr.backfill_historical_data('BTC', 'USD')
    #mgr.backfill_historical_data(product='ETH-USD', months=1, granularity=60)


@manager.command
def dbdrop():
    if prompt_bool('Are you sure? This will delete all your services (y/n)'):
        print('dropping database ...')
        eng = connect(app)
        Base.metadata.drop_all(bind=eng)
        print('database dropped')


@manager.command
def test():
    """ Run the unit tests """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=1).run(tests)


if __name__ == "__main__":
    manager.run()
