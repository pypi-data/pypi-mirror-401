import json
import logging
import os
import re

from lxf.ai.agents.interviewer import Interviewer
from lxf.ai.ocr.pdf_utilities import remove_highligth
from lxf.domain.loan import Emprunteur, Montant, ObjetFinancement, Personne, Preteur
from lxf.extractors.finance.loans.loan_extractor import get_text_and_tables_from_pdf
from lxf.domain.loan_proposal import ConditionsFinancieres, GarantieFinanciereAchevement, LoanProposal
from lxf.ai.ocr.ocr_pdf import do_ocr
from lxf.domain.tables import lxfTable
from lxf.services.try_safe import try_safe_execute, try_safe_execute_async 

SETLEVEL = logging.DEBUG
logger = logging.getLogger('Loan Proposal Extractor')
fh = logging.FileHandler('./logs/loan_proposal_extractor.log')
fh.setLevel(SETLEVEL)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(SETLEVEL)
logger.addHandler(fh)

def sanitize_logo(text:str)->str :
    """
    Docstring for sanitize_logo
    
    :param text: Description
    :type text: str
    :return: Description
    :rtype: str
    """
    regex=r"\+X, BOURGOGNE FRANCHE-COMTE"
    subst=""
    result = re.sub(regex,subst,text,0,re.MULTILINE|re.DOTALL)
    return result

def sanitize_footer(text:str)->str:
    """
    Docstring for sanitize_footer
    
    :param text: Description
    :type text: str
    :return: Description
    :rtype: str
    """
    regex=r"Les personnes c.ncern.es.*?bpbfc\.(b|h)anquepopulaire\.fr"
    subst=""
    text = re.sub(regex,subst,text,0,re.MULTILINE|re.DOTALL)
    # second footer paragraph
    regex = r"BPBFC Soci.t..*?N° ORIAS Courtier Assurances : 07023116\."
    result = re.sub(regex,subst,text,0,re.MULTILINE|re.DOTALL)
    return result    

def sanitize_bullet(text:str)->str :
    """
    Docstring for sanitize_bullet
    
    :param text: Description
    :type text: str
    :return: Description
    :rtype: str
    """
    regex=r"^e "
    subst="* "
    result = re.sub(regex,subst,text,0,re.MULTILINE|re.DOTALL)
    return result 

def sanitize_miscelanous(text:str)->str:
    """
    Docstring for sanitize_miscelanous
    
    :param text: Description
    :type text: str
    :return: Description
    :rtype: str
    """
    subst=""
    regex=r"\\"
    result = re.sub(regex, subst, text,0,re.MULTILINE|re.DOTALL)
    regex=r"swift.*BOURGOGNE Franche-COMTE\n"
    result = re.sub(regex,subst,result,0,re.MULTILINE|re.DOTALL|re.IGNORECASE)
    regex=r"( [A-Za-z0-9,éèù'/àç] +[A-Za-z0-9éèà'ù/,ç] )"
    result = re.sub(regex,subst,result,0,re.MULTILINE|re.DOTALL|re.IGNORECASE)
    return result

def extract_json(text:str)->tuple[int,str|None] :
    """
    Docstring for extract_json
    
    :param text: Description
    :type text: str
    :return: Description
    :rtype: tuple [int,str | None]
    """
    regex=r"(?P<json>{.*})"
    matches=re.findall(regex,text,re.DOTALL|re.MULTILINE)
    if matches !=None and len(matches)>0:
        json_str=matches[0]     
        return 0,json_str
    return -1, None
    

class LoanProposalDataExtractor :
    """
    Docstring for LoanProposalDataExtractor
    """
    QUESTION="question"
    EXTRACTEUR="extracteur"
    
    def __init__(self,filename:str) -> None:
        """
        Ctor         
        filename : the file name 
        """
        if os.path.exists(filename) :
            self.filename=filename
        else :
            raise NameError(f"{filename} non trouvé")    

    async def ask(self,interviewer:Interviewer, question:str,proposition)->tuple[int,str]:
        """
        Docstring for ask
        
        :param question: La question à poser
        :type question: str
        :param propositon: Texte de la proposition sur laquelle on pose une question
        :return: Le code erreur et la réponse si le code d'erreur = 0 (OK)
        :rtype: tuple[int, str]
        """
        full_question=f"""{question}\n - Utilise la proposition ci-dessous pour réondre à la question \n{proposition}"""
        error, response = await interviewer.invoke_async(full_question)
        return error, response
    
    def extract_preteur(self,json_str:str, loan_proposal:LoanProposal)->tuple[int,LoanProposal] :
        """
        Docstring for extract_preteur
        
        :param self: Description
        :param json_str: Description
        :type json_str: str
        :return: Description
        :rtype: tuple int, LoanProposal
        """
        try:
            err,json_str=extract_json(json_str)
            if err!=0 or json_str == None : return -3, loan_proposal
            data = json.loads(json_str)
            if data!=None : 
                preteur:Preteur=Preteur()
                preteur.raison_sociale = data.get('preteur',"")
                preteur.adresse = data.get("adresse","")
                preteur.code_postal=data.get("code_postal","")
                preteur.ville = data.get("ville","")
                preteur.source=data.get('source',"")
                loan_proposal.preteur = preteur
                return 0,loan_proposal
        except Exception as ex:
            logger.error(f"Exception : {ex}")            
        return -1 , loan_proposal
    def extract_emprunteur(self, json_str:str, loan_proposal:LoanProposal)->tuple[int,LoanProposal]:
        """
        Docstring for extract_emprunteur
        
        :param self: Description
        :param json_str: Description
        :return: Description
        :rtype: tuple[int, Emprunteur]
        """
        try :
            err,json_str=extract_json(json_str)
            if err!=0 or json_str == None : return -3, loan_proposal         
            data = json.loads(json_str)
            if data!=None : 
                emprunteurs=data.get('emprunteurs',None)
                source=data.get("source",None)
                rs = data.get("raison_sociale",None)
                if rs!=None and rs!="" :
                    # Personne morale
                    emprunteur:Emprunteur=Emprunteur()
                    emprunteur.raison_sociale=rs
                    emprunteur.est_personne=False
                    emprunteur.source=source
                    emprunteur.represente_par =[]                
                    for emp in emprunteurs: 
                        pers:Personne=Personne()
                        pers.nom = emp.get("nom","")
                        pers.prenoms=emp.get("prenom","")
                        pers.est_personne=True
                        emprunteur.represente_par.append(pers)
                    loan_proposal.emprunteurs.append(emprunteur)
                else :
                    # Personnes physiques
                    for emp in emprunteurs :
                        emprunteur:Emprunteur=Emprunteur()                   
                        emprunteur.nom = emp["nom"]
                        emprunteur.prenoms = emp["prenom"]
                        emprunteur.est_personne=True
                        emprunteur.source=source
                        loan_proposal.emprunteurs.append(emprunteur)
                return 0, loan_proposal
        except Exception as ex:
            logger.error(f"Exception : {ex}")
        return -1, loan_proposal    
    def extract_header(self, json_str:str, loan_proposal:LoanProposal)->tuple[int,LoanProposal]:
        """
        Docstring for extract_header        
        :param self: Description
        :param json_str: Description
        :param loan_proposal: Description
        :type loan_proposal: LoanProposal
        :return: Description
        :rtype: tuple[int, LoanProposal]
        """
        try:
            err,json_str=extract_json(json_str)
            if err!=0 or json_str == None : return -3, loan_proposal            
            data = json.loads(json_str)
            if data!=None :
                ref = data.get("référence",None)
                if ref!=None :
                    loan_proposal.header_ref=ref
                offre = data.get("titre",None)
                if offre!=None :
                    loan_proposal.header_offre=offre
                responsable_suivi=data.get("responsable",None)
                if responsable_suivi!=None :
                    loan_proposal.header_responsable_suivi= responsable_suivi
                num_etude=data.get("numéro",None)
                if num_etude!=None :
                    loan_proposal.header_num_etude = num_etude
                return 0, loan_proposal 
        except Exception as ex:
            logger.error(f"Exception : {ex}")               
        return -1, loan_proposal        
    def extract_objet_financement(self, json_str:str,loan_proposal:LoanProposal)->tuple[int,LoanProposal]:
        """
        Docstring for extract_objet_financement
        
        :param self: Description
        :param json_str: Description
        :type json_str: str
        :param loan_proposal: Description
        :type loan_proposal: LoanProposal
        :return: Description
        :rtype: tuple[int, LoanProposal]
        """
        try:
            err,json_str=extract_json(json_str)
            if err!=0 or json_str == None : return -3, loan_proposal            
            data = json.loads(json_str)
            if data !=None :
                objet:ObjetFinancement = ObjetFinancement()
                objet.titre = data.get("titre","")
                objet.description = data.get("description","")
                objet.adresse = data.get("adresse","")
                objet.code_postal=data.get("code_postal","")
                objet.ville = data.get("ville","")
                objet.usage =data.get("usage","")
                objet.nature=data.get("nature","")
                objet.deblocage_plusieurs_phases = data.get("deblocage_plusieurs_phases","False")
                objet.phase_1=data.get("phase_1","")
                objet.phase_2=data.get("phase_2","")
                objet.source = data.get("source","")                
                loan_proposal.objets_financement.append(objet)
                return 0, loan_proposal
        except Exception as ex:
            logger.error(f"Exception : {ex}")        
        return -1, loan_proposal    
    def extract_conditions_financieres(self,json_str:str,loan_proposal:LoanProposal)->tuple[int,LoanProposal]:
        """
        Docstring for extract_conditions_financiers
        
        :param self: Description
        :param json_str: Description
        :type json_str: str
        :param loan_proposal: Description
        :type loan_proposal: LoanProposal
        :return: Description
        :rtype: tuple[int, LoanProposal]
        """
        err,json_str=extract_json(json_str)
        if err!=0 or json_str == None : return -3, loan_proposal            
        data = json.loads(json_str)
        if data !=None :
            source = data.get("source","")
            cf:ConditionsFinancieres= loan_proposal.conditions_financieres
            cf.source = source
            cf.commission_engagement =data.get("commission_engagement",0.0)
            m:Montant=Montant()
            cf.frais_dossier=data.get("frais_dossier",m)
            cf.is_taux_variable = data.get("is_taux_variable")
            cf.calcul_taux_variable=data.get("calcul_taux_variable","")
            cf.periodicite_commission=data.get("periodicite_commission","")
            return 0, loan_proposal
        return -1, loan_proposal
    def extract_gfa(self, json_str:str,loan_proposal:LoanProposal)->tuple[int,LoanProposal]:
        """
            :param self: Description
            :param json_str: Description
            :type json_str: str
            :param loan_proposal: Description
            :type loan_proposal: LoanProposal
            :return: Description
            :rtype: tuple[int, LoanProposal]
            """
        err,json_str=extract_json(json_str)
        if err!=0 or json_str == None : return -3, loan_proposal            
        data = json.loads(json_str)
        if data !=None :
            source = data.get("source","")
            return 0, loan_proposal
        return -1, loan_proposal
        
    async def extract_data(self) ->LoanProposal :
        """
        Extrait les données de la proposition
        """
        proposal:LoanProposal=LoanProposal()
        found_tables=list[lxfTable]
        required_ocr_cleanup=False
        text,found_tables = await try_safe_execute_async(logger,get_text_and_tables_from_pdf,filename=self.filename)
        # Eliminer les textes inférieurs à 200 caractères
        if len(text)<=200 : text=""
        if text == None or text=="" : 
            # try with OCR  
            # Remove HighLight and convert to b&w 
            prepared_pdf= self.filename.replace('.pdf','_prepared.pdf')            
            err, error_message = remove_highligth(self.filename, prepared_pdf)    
            if err<0 :
                logger.error(f"Remove hightligth a échoué : {error_message}")
                return proposal       
            output_ocr_pdf= prepared_pdf.replace('_prepared.pdf','_ocr.pdf')
            result = do_ocr(input_pdf=prepared_pdf, output_pdf=output_ocr_pdf)  
            os.remove(prepared_pdf)
            if os.path.exists(output_ocr_pdf):
                ## Todo Processing the data    
                required_ocr_cleanup=True        
                text,found_tables = await try_safe_execute_async(logger,get_text_and_tables_from_pdf,filename=output_ocr_pdf)
                os.remove(output_ocr_pdf)
        if text!=None :    
            text=sanitize_miscelanous(sanitize_bullet(sanitize_footer(sanitize_logo(text))) )   
            interviewer:Interviewer=Interviewer(base_url="http://172.16.255.172:11434/",
                                                system_prompt="tu es un assistant français spécialisé en gestion de prêts bancaires",
                                                ctx=100*1024,
                                                #model="nemotron-mini:4b-instruct-fp16"
                                                )    
            if required_ocr_cleanup :       
                nettoyage=f"""
    Voici un texte issue d'un OCR, ta mission consiste à corriger les mots mal orthographiés ou incomplets. 
    Voici le texte à traiter: 
    {text}
    """  
                error, corrected_text = await interviewer.invoke_async(nettoyage)
                # print the corrected text
                if error==0: 
                    print(corrected_text)                
                    print("\n"*3)
                    text=corrected_text
                else :
                    return None
            # start the interview 
            requests=[
                {self.QUESTION:
                """
                Qui est l'établissement prêteur ? quelle est l'adresse du siège social? 
                # Consignes: 
                - Donne ta réponse dans un json avec impérativement les éléments suivants: 
                    "preteur" : doit contenir l'identification du prêteur,
                    "adresse": doit contenir l'adresse du siège social,
                    "code_postal": doit contenir le code postal, 
                    "ville": doit contenir la ville , 
                    "source" : doit contenir la partie du texte qui a permis d'identifier le prêteur.
                - Donne uniquement le json brute sans aucune autre information.
                """,self.EXTRACTEUR:self.extract_preteur},
                {self.QUESTION:
                """
                 Trouve tous les emprunteurs et la raison sociale de l'entreprise, si elle est précisiée, à qui est adressé cette proposition.
                # Consignes: 
                - Ignore tous les contacts de la banque y compris dans la signature après le nom de la banque
                - Les emprunteurs peuvent être une personne ou une entreprise représentée par une ou plusieurs personnes.
                - Cette information se trouve par ordre de priorité :  
                    1- Après le texte suivant : 'A l'attention de ...' ou 'À l'atention de ...' 
                    2- Dans le cas d'une entreprise, ajoute aux données précédentes la raison sociale qui apparait pour la signature de la proposition. Généralement après le texte : Pour la ...                       
                - Donne ta réponse dans un json avec impérativement les éléments suivants:
                    - "raison_sociale": doit contenir, si l'information est présente, la raison sociale de l'entreprise. Sinon la chaine.
                    - "emprunteurs" : doit contenir la liste des emprunteurs. Chaque emprunteur doit contenir le nom et le prémon. 
                    - "source": la ou les parties du texte qui ont permis d'identifier les emprunteurs.
                - Donne uniquement le json brute sans aucune autre information.                 
                 """,self.EXTRACTEUR:self.extract_emprunteur},
                {self.QUESTION:
                """
                 Quels sont les informations suivantes :
                 - La **référence** de l'offre,
                 - le **titre** de l'offre,
                 - le **responsable** de l'offre,
                 - le **numéro** de l'offre.
                 # Consignes :
                - Donne ta réponse dans un json avec impérativement les éléments suivants:
                    - référence
                    - titre
                    - responsable
                    - numéro
                    - "source": la ou les parties du texte qui ont permis d'identifier les informations.
                - Donne uniquement le json brute sans aucune autre information. 
                 """,self.EXTRACTEUR:self.extract_header},
                {self.QUESTION:
                    """
                    Répond à tous les questions ci-dessous, en suivant les consignes données
                       - Quelle est l'objet principal et l'adresse du bien du financement?
                       - Quel besoin va couvrir le financement ?
                       - A quel usage est destiné le financement ?
                       - Existe-il un déblocage en 2 phases ou 2 temps? 
                       - Si Déblocage en 2 phases ou 2 temps: 
                            - Donne moi la description détaillée de la Phase 1 ?
                            - Donne moi la description détaillée de la Phase 2 ?
                        # Consignes :
                            - Donne ta réponse dans un json avec impérativement les éléments suivants:
                                - "description" : doit contenir l'objet du fiancement,
                                - "titre": doit contenir le besoin du financement, 
                                - "adresse" : doit contenir l'adresse du financement
                                - "code_postal": doit contenir le code postal du bien financé,
                                - "ville" : doit contenir la ville du bien financé,
                                - "nature" : doit contenir la nature du bien financé,
                                - "usage": doit contenir l'usage du bien financé,
                                - "deblocage_plusieurs_phases": True s'il existe un déblocage en 2 phases ou 2 temps, False sinon.
                                - si déblocage en 2 phases ou 2 temps :
                                    - "phase_1": doit contenir la description détaillée de la phase 1.
                                    - "phase_2": doit contenir la description détaillée de la phase 2.
                                - "source": la ou les parties du texte qui ont permis d'identifier les informations.
                            - Donne uniquement le json brute sans aucune autre information.
                    """,
                    self.EXTRACTEUR:self.extract_objet_financement},
                # {self.QUESTION:
                #     """
                #     Ta mission consiste à extraire les conditions financières:
                #     - Vérifier s'il s'agit d'un taux fixe ou variable, 
                #         - S'il s'agit d'un taux variable:
                #             - tu devras extraire le calcul indexation du taux ,
                #             - Le taux du jour
                #             - Toutes les informations concernant ce taux
                #     - la périodicité à laquelle sera perçu la commission d'engagement,
                #     - le montant des frais de dossier contenu dans le paragraphe des conditions financiers              
                #     # Consignes : 
                #         - Donne ta réponse dans un json avec impérativement les éléments suivants:
                #             - "commission_engagement" : doit contenir le montant du taux annuel sous la forme d'un float compris entre 0 et 1 (100%),
                #             - "is_taux_variable": True si le taux est variable, False sinon,                         
                #             - "calcul_taux_variable": si le taux de commission est variable, doit contenir les modalités détaillées du calcule du taux variable, 
                #             - "periodicite_commission": doit contenir périodicité à laquelle sera perçue la commission d'engagement,
                #             - "frais_dossier": doit contenir le montant des frais de dossier sous la forme {"value":<montant des frais de dossier>, "devise":<devise monétaire du montant des frais de dossier>}
                #             - "source": la ou les parties du texte qui ont permis d'identifier les informations.
                #         - Donne uniquement le json brute sans aucune autre information.                    
                #     """,
                #     self.EXTRACTEUR:self.extract_conditions_financieres },
                    
                #     {self.QUESTION:
                #         """
                        
                #         """,
                #         self.EXTRACTEUR:self.extract_gfa},
                    # "Quelles sont toutes les garanties",
                    # "Quelles sont les modalités de fonctionnement",
                    # "Quelles sont les conditions générales"
            ]
            for request in requests :
                error, response = await self.ask(interviewer,request[self.QUESTION],text)
                extracteur = request.get(self.EXTRACTEUR,None)
                if extracteur !=None :
                    if error==0 : 
                        # pas d'erreur
                        error, proposal = try_safe_execute(logger,extracteur,json_str=response, loan_proposal=proposal)
                        if error!=0 :
                            logger.error(f"Extraction des données impossible(error={error}). Réponse:\n{response}")
                    else :
                        logger.warning(f"La question {request.get(self.QUESTION,'')} n'a pu être répondue")
                else : 
                    logger.error(f"Erreur Extracteur, introuvable !\nQuestion:\n{request.get(self.QUESTION,"")}")
        else :
            logger.error("Aucun texte n'a pu être extrait ! ")
        return proposal