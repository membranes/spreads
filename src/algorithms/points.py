import logging

class Points:

    def __init__(self) -> None:
        
        logging.basicConfig(level=logging.INFO, format='%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def lower_decile(self, x):

        return x.quantile(0.10)
    
    def lower_quartile(self, x):

        return x.quantile(0.25)
    
    def median(self, x):

        return x.quantile(0.50)
    
    def upper_quartile(self, x):

        return x.quantile(0.75)
    
    def upper_decile(self, x):

        return x.quantile(0.90)
