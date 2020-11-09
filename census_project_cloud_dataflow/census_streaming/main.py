import logging
from runner import runner

if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  runner.run()