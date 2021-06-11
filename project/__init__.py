import os
from flask import Flask
import sys
from config import DevelopmentConfig, ProductionConfig


app = Flask(__name__)
# load default configuration
config_name = sys.argv[1]
print(config_name)
if config_name == 'DevelopmentConfig':
    config = DevelopmentConfig()
else:
    config = ProductionConfig()

print(config)
app.config.from_object(config)
