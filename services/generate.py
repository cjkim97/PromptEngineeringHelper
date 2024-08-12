# 랭체인
from langchain_core.prompts import ChatPromptTemplate

# 모델종류
from langchain_openai import ChatOpenAI 
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import  ChatGoogleGenerativeAI

# 파서
from langchain_core.output_parsers import StrOutputParser

import asyncio



# OpenAI 출력
async def get_result(model_config, chatprompt = []) : 
    
    # 모델 세팅
    model_name = model_config['model_name']
    temperature = model_config['temperature']
    api_key = model_config['api_key']
    top_p = model_config['top_p']

    if 'gpt' in model_name : 
        print(">>>>>>> OPENAI MODEL INFERNCING 을 시작합니다")
        llm = ChatOpenAI(
                temperature=temperature,
                model=model_name,
                api_key=api_key,
                max_retries = 5,
                top_p = top_p
            )
    elif 'claude' in model_name :
        print(">>>>>>> ANTHROPIC MODEL INFERNCING 을 시작합니다")
        llm = ChatAnthropic(
            temperature=temperature,
            model=model_name,
            api_key=api_key,
            max_retries = 5,
            top_p = top_p,
            max_tokens=4096
        )
    elif 'gemini' in model_name :
        print(">>>>>>> GOOGLE MODEL INFERNCING을 시작합니다")
        llm = ChatGoogleGenerativeAI(
            temperature=temperature,
            model=model_name,
            api_key=api_key,
            max_retries = 5,
            top_p = top_p
        )
    
    # 프롬프트 세팅
    prompt = ChatPromptTemplate(chatprompt)

    # chain
    chain = prompt | llm | StrOutputParser()

    return model_config, chain.invoke(input={})

async def generate(configs = [], generate_times=1, chatprompt=[]):
    '''
    configs : List[Dict]
    - model_name : str
    - api_apikey : str
    - temperature : float
    - top_p : float
    - chat_prompt : List[tuple]
    
    '''
    tasks = []
    for i in range(generate_times) : 
        for config in configs:
            tasks.append(get_result(config, chatprompt))

    results = await asyncio.gather(*tasks)
    return results

# # 비동기 루프 실행
# results = asyncio.run(generate())
# print(results)