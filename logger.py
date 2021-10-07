import logging


logging.basicConfig(handlers=[logging.FileHandler(filename="LOG.log",
                                                 encoding='windows-1251'),
                              logging.StreamHandler()],
                    level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s - %(message)s',
                    )

logger = logging.getLogger(__name__)