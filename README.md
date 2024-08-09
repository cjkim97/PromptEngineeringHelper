# P.E Helper(v.1.0.0 release)
평소에 모든 생성형AI 사이트마다 들어가서 결과를 생성하고 붙여 넣는게 귀찮아서, 만들었습니다 :)
"펠퍼"는 Streamlit 기반으로 만들어졌으며, 국내 1호 프롬프트 엔지니어인 강수진 대표님께 영감을 받아, 제가 평소에 쓰면서 필요했던 기능을 담아 만들었습니다. 

# 사용설명서
1. 프롬프트를 입력합니다. Systemprompt 와 human/ai prompt 를 세팅할 수 있습니다.
  ![프롬프트입력](https://github.com/user-attachments/assets/1b85362d-52c7-4af5-afc6-aa6311fe22b8)

2. 생성할 모델을 설정합니다. 각 모델을 추가할 때마다 추가한 모델의 temperature와 top-p 값을 조절할 수 있습니다!
  ![모델세팅_fast](https://github.com/user-attachments/assets/7f5b1003-0af8-49f7-8955-be07ddf82dc1)

3. API key, 모델 호출 횟수를 입력한 뒤 생성버튼을 누릅니다. (각 모델이 생성 시도 수 만큼 호출되기 때문에 api 비용 조심하세요 :) )
  ![생성](https://github.com/user-attachments/assets/6db8ca61-f0db-4d9d-851e-91d6631c372e)

## 이럴때 사용해보세요! 
### 🤖 같은 프롬프트에 다양한 모델의 결과를 한번에 비교하고 싶어요!
1. System prompt(선택), Human prompt(필수) 칸에 프롬프트를 작성합니다.
2. 비교하고 싶은 모델을 select box 에서 선택하고, 각 모델별로 config 를 설정해줍니다.
3. 이때, 동일 모델의 config 만 바꿔서 비교하는 것도 가능합니다!
4. 생성시도는 결과를 얻기위해 각 모델을 몇번 실행시킬 것인지를 의미합니다. 모델의 결과만 보고 싶은 경우, 1회를 추천드립니다.
5. Generate 를 클릭합니다

###  📝 프롬프트가 안정적인지 확인하기 위해 여러번 생성하고 결과를 보고 싶어요!
1. System prompt(선택), Human prompt(필수) 칸에 프롬프트를 작성합니다.
2. 확인하려는 모델을 select box 에서 선택하고, config 를 설정해줍니다.
3. 생성시도 횟수를 지정합니다.
4. Generate 를 클릭합니다.

# Update
- 2024.08.09 "펠퍼v1.0.0" release 
