from logger import setup_logger

logger = setup_logger(name=__name__, enable_console=True, enable_file=False)

class Sample:
    def print_log(self):
        logger.debug(f'[PRINT LOG] DEBUG')
        logger.info(f'[PRINT LOG] INFO')
        logger.warning(f'[PRINT LOG] WARNING')
        logger.error(f'[PRINT LOG] ERROR')


s = Sample()
s.print_log()