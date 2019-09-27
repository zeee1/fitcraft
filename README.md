# fitcraft

BIC 2018 "Enjoying Minecraft with Wearable Devices" 논문에 활용된 데이터 분석 및 시각화 코드

- 웨어러블 디바이스를 착용한 게임 유저가 일정 운동량을 달성할때마다 게임 아이템을 보상으로 받을때, 게임 유저의 운동량 변화와 게이밍 패턴을 분석한 연구 

src/DB_controller.py SQLITE에 저장된 게임 로그 데이터를 불러오는 기능 제공
src/fb_fc_analyzer.py 일반적인 fitbit 유저와 fitcraft 유저의 운동량을 분석하는 스크립트
src/log_cleanser.py 게임로그 데이터 클렌징
src/log_consume_event_analyzer.py 게임 로그에서 아이템 소비 이벤트 로그만을 분석하여 소비된 아이템의 비율을 분석하는 스크립트
src/log_get_item_from_each_category.py 게임의 직군 카테고리(헌터, 마이너, 아키텍쳐 등)마다 주로 소비한 아이템을 분석하는 스크립트
src/log_user_category_analyzer.py 게임의 직군 카테고리 분포를 파악하는 스크립트
