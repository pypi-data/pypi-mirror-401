from langchain_ollama import ChatOllama
import re


class Interviewer():
    """
    Docstring for Interviewer
    """
    def __init__(self,
                 model:str="gpt-oss", 
                 base_url:str="http://localhost",
                 ctx:int=4096,
                 system_prompt:str="Tu es un assistant français"):
        """
        Docstring for __init__
        
        :param self: Description
        :param model: Model LLM 
        :type model: str
        :param base_url: URL du serveur OLLAMA
        :type base_url: str
        :param ctx: Taille du contexte (défaut 4096 o)
        :type ctx: int
        """
        self.llm = ChatOllama(
            model=model,
            temperature=0,
            num_ctx=ctx,
            base_url=base_url,
            validate_model_on_init=True,
            
            # other params...
        )
        self.system_prompt=system_prompt
        
    def invoke(self,user_prompt:str)->str :
        """
        """
        messages = [
            ("system",self.system_prompt),
            ("human",user_prompt)
        ]
        ai_response =self.llm.invoke(messages)
        if ai_response : 
            return ai_response.content
        return "Aucune réponse"

    async def invoke_async(self,user_prompt:str)->tuple[int,str] :
        """
        """
        messages = [
            ("system",self.system_prompt),
            ("human",user_prompt)
        ]
        ai_response =await self.llm.ainvoke(messages)
        if ai_response : 
            return 0,ai_response.content
        return -1,"Aucune réponse"