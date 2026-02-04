import logging
import os

# Create logs folder if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    filename='logs/scm_system.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_error(message):
    logging.error(message)

def log_info(message):
    logging.info(message)