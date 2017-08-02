# Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_script import Manager, Server, prompt_bool
from coinpl import create_app, connect
from coinpl.models import Base
from coinpl.external.gdax import GDAXDataManager

app = create_app()
manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0',
    port=5000
))


@manager.command
def dbinit():
    eng = connect(app)
    Base.metadata.create_all(bind=eng)


@manager.command
def dbpopulate():
    eng = connect(app)
    mgr = GDAXDataManager(eng)
    mgr.populate_fixed_resources()
    #mgr.backfill_historical_data(product='ETH-USD', months=1, granularity=60)


@manager.command
def dbdrop():
    if prompt_bool('Are you sure? This will delete all your data (y/n)'):
        print('dropping database ...')
        eng = connect(app)
        Base.metadata.drop_all(bind=eng)
        print('database dropped')


if __name__ == "__main__":
    manager.run()
