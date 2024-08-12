import streamlit as st
from services.generate import generate
import asyncio
####################################### streamlit basic setting  #######################################

st.set_page_config(
    page_title="PEHelper",
    page_icon="📝",
    layout='wide'
    )
# session_state 관리
if 'prompts' not in st.session_state:
    st.session_state['prompts'] = []

if 'model_configs' not in st.session_state:
    st.session_state['model_configs'] = []

if 'generation_results' not in st.session_state:
    st.session_state['generation_results'] = []

if 'add' not in st.session_state:
    st.session_state.add = False

if 'modify' not in st.session_state:
    st.session_state.modify = False

if 'api_keys' not in st.session_state:
    st.session_state.api_keys = {
        "OPENAI_API_KEY" : "",
        "ANTHROPIC_API_KEY" : "",
        "GEMINI_API_KEY" : "",
        
    }



####################################### 페이지 디자인 영역 #######################################
with open( "style.css", encoding='utf-8-sig' ) as css:
    st.markdown(f"""<style>{css.read()}</style>""", unsafe_allow_html=True)

####################################### 페이지 상호작용 함수 영역 #######################################
# 시스템 프롬프트 변경
def modify_system_prompt() : 
    st.session_state['system_prompt'] = st.session_state['sys_prom']

# 프롬프트 삭제
def delete_chat(chat_index):
    st.session_state['prompts'] = st.session_state['prompts'][:chat_index] \
        + st.session_state['prompts'][chat_index+1 : ]

# 프롬프트 추가
def add_chat() : 
    if st.session_state.new_prompt : 
            st.session_state.add = True

@st.dialog("프롬프트 수정")
def modify_chat(chat_index) : 
    now_prompt = st.session_state['prompts'][chat_index][-1]
    now_cate = st.session_state['prompts'][chat_index][0]
    categories = ["system", "human", "ai"]
    now_cate_index = categories.index(now_cate)

    # 프롬프트 수정
    cate_area, _ = st.columns([1, 2])
    modified_cate = cate_area.selectbox(label = "입력카테고리", 
                                 options = ["system", "human", "ai"], 
                                 label_visibility = 'collapsed',
                                 key= 'modified_category',
                                 index = now_cate_index)
    modified_prompt = st.text_area(label='프롬프트수정', 
                                    value=now_prompt, 
                                    label_visibility='collapsed',
                                    key='modified_prompt',
                                    height=400
                                    )
    finish_modify = st.button(label ="Modify", 
                              key=f'modify-dialog')
    if finish_modify or st.session_state.modify : 
        st.session_state['prompts'][chat_index] = (modified_cate, modified_prompt)
        st.session_state.modify = False
        st.rerun()

# 모델 추가
def add_model_config() : 
    model_name= st.session_state.add_model
    model_configs = {
        "model_name"  : model_name,
        "temperature" : 1.0,
        "maximum_token" : 4096,
        "top_p" : 1.0
    }
    if model_name != '선택' : 
        st.session_state['model_configs'].append(model_configs)

# 모델 삭제
def delete_model(model_index) : 
    st.session_state['model_configs'] = st.session_state['model_configs'][:model_index] \
        + st.session_state['model_configs'][model_index+1 : ]
    
# temperature 변경
def change_temperature(model_index):
    st.session_state['model_configs'][model_index]["temperature"] = st.session_state[f'temperature{model_index}']

# top_p 변경
def change_top_p(model_index):
    st.session_state['model_configs'][model_index]["top_p"] = st.session_state[f'top_p{model_index}']

####################################### 페이지 영역 #######################################
st.write('''<div class="main_title">
                <h1>펠퍼(P.E.Helper)</h1>
                <!--<a href="http://www.naver.com">by UgwayK</a>-->
         </div>''', unsafe_allow_html=True)
st.write('''<div class="page_links">
            <div class="link"> <a href="https://github.com/cjkim97/PromptEngineeringHelper"> 📝 사용설명서 </a> </div>
            <div class="link"> <a href="https://blog.naver.com/nuang0530/223542333577"> 🏠 제작자의 블로그 </a> </div>
         </div>''', 
         unsafe_allow_html=True)

# 페이지 레이아웃 잡기
prompt_setting, config_setting = st.columns([2, 1])

################# 1. PROMPT SETTING AREA #################
prompt_setting.subheader("프롬프트 입력")
# 1. 추가한 프롬프트 보여주기
for ind, prompt in enumerate(st.session_state['prompts']) : 
    cate, text = prompt
    prompt_container = prompt_setting.container(border=True)
    with prompt_container : 
        prompt_container.write(f'<p>{cate}</p>', unsafe_allow_html=True)
        prompt_container.text(text)
        
        # del_button, mod_button = prompt_container.columns([1, 1], gap="small")
        delete = prompt_container.button("❌ Delete", key=f'del{ind}', on_click=delete_chat, args=(ind, ))
        modify =prompt_container.button("✏️ Modify", key=f'mod{ind}', on_click=modify_chat, args=(ind, ))

# 2. 카테고리 별 프롬프트 추가하기
add_prompt, add_button = prompt_setting.columns([5, 1])
new_prompt = add_prompt.text_area(label = '추가프롬프트', 
                                placeholder="Prompt",
                                label_visibility = 'collapsed',
                                key='new_prompt',
                                value=""
                                )
category = add_button.selectbox(label = "입력카테고리", 
                                     options = ["system", "human", "ai"], 
                                     label_visibility = 'collapsed',
                                     key= 'prompt_category')
add_button = add_button.button(label="Add", 
                               type="primary", 
                               key='add_button',
                               on_click=add_chat)

if st.session_state.add : 
    st.session_state['prompts'].append((category, new_prompt))
    print(st.session_state['prompts'])
    st.session_state.add = False # 한번만 add
    st.rerun()


################# 2. CONFIG SETTING AREA #################
config_setting.subheader('모델 세팅')
# 1. 모델 추가 selectbox
models = ['선택', 'gpt-4o', 'gpt-4o-mini','gpt-3.5-turbo', 
          'claude-3-5-sonnet-20240620', 'claude-3-opus-20240229', 'claude-3-haiku-20240307',
          'gemini-1.5-flash', 'gemini-1.5-pro']
select, button = config_setting.columns([2, 1])
add_model = select.selectbox(label='모델추가', 
                             options=models,
                             key='add_model',
                             label_visibility="collapsed"
)
add_button = button.button("Add", type="primary")
if add_button : 
    add_model_config()

# 2. 추가한 모델 config 설정
for ind, config in enumerate(st.session_state['model_configs']) : 
    model_name = config['model_name']
    config_expander = config_setting.expander(label=model_name, expanded=False)
    # temperature 세팅
    temperature = config_expander.slider(label='temperature', 
                           min_value=0.0, 
                           max_value=2.0, 
                           step=0.01, 
                           value=config['temperature'],
                           key=f'temperature{ind}',
                           on_change=change_temperature,
                           args=(ind,)
                           )
    # top_p 세팅
    config_expander.slider(label='top_p', 
                           min_value=0.0, 
                           max_value=1.0, 
                           step=0.01, 
                           value=config['top_p'],
                           key=f'top_p{ind}',
                           on_change=change_top_p,
                           args=(ind,)
                           )
    config_expander.button('Delete', key=f'model_delete{ind}', on_click=delete_model, args=(ind,))

# 2. API_KEY, Generate time 설정
choiced_model = [x['model_name'] for x in st.session_state['model_configs']]
openai_check = True if len([name for name in choiced_model if 'gpt' in name]) else False
claude_check = True if len([name for name in choiced_model if 'claude' in name]) else False
gemini_check = True if len([name for name in choiced_model if 'gemini' in name]) else False
openai_api_key = "pehelper"
claude_api_key = "pehelper"
gemini_api_key = "pehelper"

key_input = config_setting.container()
with key_input :
    if openai_check : 
        openai_api_key = key_input.text_input(label="OPENAI_API_KEY", 
                                              type="password",
                                              value=st.session_state['api_keys']['OPENAI_API_KEY'])
        st.session_state['api_keys']['OPENAI_API_KEY'] = openai_api_key
    if claude_check : 
        claude_api_key = key_input.text_input(label="ANTHROPIC_API_KEY", 
                                              type="password",
                                              value=st.session_state['api_keys']['ANTHROPIC_API_KEY'])
        st.session_state['api_keys']['ANTHROPIC_API_KEY'] = claude_api_key
    if gemini_check : 
        gemini_api_key = key_input.text_input(label="GEMINI_API_KEY", 
                                              type="password",
                                              value=st.session_state['api_keys']['GEMINI_API_KEY'])
        st.session_state['api_keys']['GEMINI_API_KEY'] = gemini_api_key
    generate_times = key_input.number_input(label="생성 시도 수", min_value=1, max_value=10, value=1, step=1, key="generate_times")
    gen_button = key_input.button("GENERATE", type='primary')

Error = ""
results = ""
# ERROR CHECK
if gen_button : 
    # 대화 내용이 있는지
    if not st.session_state['prompts'] : 
        Error = config_setting.error('프롬프트를 입력해주세요.')
    # 모델을 설정했는지
    elif not st.session_state['model_configs'] : 
        Error = config_setting.error('생성을 위한 모델을 선택해주세요.')
    # API key 입력이 잘 됐는지
    elif not openai_api_key : 
        Error = config_setting.error('API KEY를 입력해주세요.')
    elif not claude_api_key : 
        Error = config_setting.error('API KEY를 입력해주세요.')
    elif not gemini_api_key : 
        Error = config_setting.error('API KEY를 입력해주세요.')

    # api key 연결
    for config in st.session_state['model_configs'] : 
        model_name = config['model_name']
        if 'gpt' in model_name : 
            config['api_key'] = openai_api_key
        if 'claude' in model_name : 
            config['api_key'] = claude_api_key
        if 'gemini' in model_name : 
            config['api_key'] = gemini_api_key
    # 중복제거
    # st.session_state['model_configs'] = list(set(st.session_state['model_configs']))

    if not Error : 
        with config_setting : 
            with st.spinner('텍스트 생성 중...') : 
                try : 
                    # 비동기 루프 실행
                    results = asyncio.run(generate(st.session_state['model_configs'], 
                                                   generate_times=generate_times, 
                                                   chatprompt= st.session_state['prompts']))
                   
                    st.session_state['generation_results'] = results
                    st.toast("결과가 나왔어요!", icon='🎉')
                except Exception as e : 
                    print(e)
                    st.error(e)

################# 3. RESULT AREA #################
# 결과후처리
if st.session_state['generation_results'] : 
    unique_configs = []
    result_group = []
    for result in st.session_state['generation_results'] : 
        conf, generated_text = result
        if conf in unique_configs : 
            config_index = unique_configs.index(conf)
            result_group[config_index].append(generated_text)
        else : 
            unique_configs.append(conf)
            result_group.append([generated_text])
    #### 화면 표시 ####
    st.subheader("결과")
    result_container = st.columns(len(unique_configs), 
                                  vertical_alignment="top")
    for conf_ind, conf in enumerate(unique_configs) : 
        display_area = result_container[conf_ind]
        model_name = conf['model_name']
        temperature = conf['temperature']
        top_p = conf['top_p']
        tap = display_area.container(border=True)
        with tap : 
            tap.write(f'''<p>{model_name}-temp{temperature}-topP{top_p}</p>''', unsafe_allow_html=True)
            for ind, result_generate in enumerate(result_group[conf_ind]) : 
                tap.code(body=result_generate, language='plaintext')