import logging

log_format = '%(asctime)s:%(levelname)s:%(filename)s:%(message)s'
logging.basicConfig(filename='erro.log',
                    # w -> sobrescreve o arquivo a cada log
                    # a -> não sobrescreve o arquivo
                    filemode='a',
                    level=logging.ERROR,
                    format=log_format)
logger = logging.getLogger('root')

def geraLog(msg) :
  logger.error(msg)
