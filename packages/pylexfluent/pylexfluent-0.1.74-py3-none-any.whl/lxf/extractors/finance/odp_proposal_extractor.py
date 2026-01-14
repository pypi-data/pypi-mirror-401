import logging
from multiprocessing import Process
import os 
from lxf.settings import get_logging_level

###################################################################

logger = logging.getLogger('odp_proposal_extractor')
fh = logging.FileHandler('./logs/odp_proposal_extractor.log')
fh.setLevel(get_logging_level())
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(get_logging_level())
logger.addHandler(fh)
#################################################################

from lxf.services.measure_time import measure_time_async
from lxf.extractors.finance.loans.loan_proposal_extractor import LoanProposalDataExtractor
from lxf.services.try_safe import try_safe_execute_async

@measure_time_async
async def extract_data(file_path:str,**kwargs)->str|None:
    """
    Extrait les données d'une proposition d'offre de prêt 
    """
    if file_path==None: 
        logger.error("Extract Data: file_path ne peut pas etre None")
        return None
    logger.debug(f"Demande extraction de donnees pour {file_path}")
    loan_proposal:LoanProposalDataExtractor= LoanProposalDataExtractor(file_path)
    result= await try_safe_execute_async(logger,loan_proposal.extract_data)         
    return result