import re

stri = "컴퓨터 프로그램 소스를 공유하고 협업하여 개발할 수 있는 버전 관리 시스템인 깃(Git)에 프로젝트 관리 지원 기능을 확장하여 제공하는 웹 호스팅 서비스. 2008년 미국 깃허브사(GitHub Inc)에서 서비스를 시작하였다. 사용자에게 무료로 계정과 저장소를 제공하며, 분산형 버전 관리 서비스로 서버 장애 시 데이터 복원력이 뛰어나다. 전 세계에서 오"

regex = re.compile("\.{3,}")
yesOrNo = regex.search(stri)

print(yesOrNo is None)

t_array = stri.split('.')[0:-4]
desc = ''
for x in t_array:
    desc += x + '.\n'

print(desc)