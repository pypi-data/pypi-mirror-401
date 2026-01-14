from typing import List
from pydantic import BaseModel,Field

from lxf.domain.loan import Emprunteur, Montant, ObjetFinancement, Preteur

class ConditionsFinancieres(BaseModel):
    """
    Docstring for ConditionsFinancieres
    """
    is_taux_variable:bool=Field(default=False)
    calcul_taux_variable:str=Field(default="")
    commission_engagement:float=Field(default=0.0)
    periodicite_commission:str=Field(default="")
    frais_dossier:Montant=Field(default=Montant())
    source:str=Field(default="")

class GarantieFinanciereAchevement(BaseModel) :
    """
    Docstring for GarantieFinanciereAchevement
    """
    label:str=Field(default="")
    montant:Montant = Field(default=Montant())
    taux_annuel_commission:float=Field(default=0.0)
    modalite_reglement:str=Field(default="")
    frais_dossier:Montant=Field(default=Montant())
    conditions:str = Field(default="")
    source:str=Field(default="")

class LoanProposal(BaseModel) :
    """
    Docstring for LoanProposal
    """
    num_suivi:str=Field("")
    header_offre:str=Field("")
    header_ref:str=Field("")
    header_emprunteur:str=Field("")
    header_responsable_suivi:str=Field("")
    header_num_etude:str=Field("")
    date_emission_offre:str=Field("")
    objets_financement:List[ObjetFinancement]=[]
    preteur: Preteur = Field(default=Preteur())
    emprunteurs:List[Emprunteur]=[]   
    gfa:GarantieFinanciereAchevement=Field(default=GarantieFinanciereAchevement())
    conditions_financieres:ConditionsFinancieres=Field(default=ConditionsFinancieres())
    source:str=Field(default="")