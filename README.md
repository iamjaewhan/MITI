# 🏀MITI

#### 🎯프로젝트 목적

생활 스포츠 문화에는 부족한 팀원을 초대하여 함께 운동을 즐기는 게스트 문화가 존재합니다. 농구, 축구, 풋살, 테니스 등 스포츠를 즐기기 위해 온/오프라인을 통해 게스트를 초대하지만 이러한 과정이 매우 복잡하고 번거로운 프로세스로 이루어져 원활한 초대가 이루어지지 않았습니다. MITI 는 이러한 문제의 원인 2가지를 해결하여 더욱 많은 사람들이 스포츠를 즐길 수 있도록 하는 서비스를 개발하는 것이 목표입니다.
![miti 프로젝트 설명](https://user-images.githubusercontent.com/67890930/203727499-e86e9d0c-f8f6-4a10-9789-6fa2d33e658e.jpg)

목표 1. 장소, 시간, 인원 및 비용 등 게스트의 참여 의사 결정에 필요한 정보를 게스트들에게 제공한다.

목표 2. 초대자와 게스트의 매칭 단계를 최소화하여 게스트 참여율을 높인다.


<br>

#### 🛠개발 환경 및 사용 기술

![MITI architecture](https://user-images.githubusercontent.com/67890930/203727865-48d635c6-f577-4f34-8f23-9d0116f9edeb.jpg)

Python 3.9.0

Django 4.1

MySQL 8.0.30

djangorestframework 3.13.1

djangorestframework-simplejwt 5.2.0

RabbitMQ  3.11.0

celery 5.2.7

channels 3.0.5

channels-redis 3.4.1


<br>

#### 구현 기능

- [x] 회원가입

- [x] 회원탈퇴

- [x] 로그인

- [x] 로그아웃

- [x] 회원정보수정


- [x] 경기 등록
- [ ] 경기 정보 조회

  - [x] 모든 경기 목록 조회
  - [ ] 경기 조건 검색(검색 조건: 경기 시작시간, 장소)
- [ ] 경기 취소
- [x] 경기 수정
- [x] 경기 참여
- [ ] 경기 참여 취소
- [ ] 경기 모집 마감
- [ ] 경기 모집 실패

- [ ] 참가자 <-> 참가자 리뷰
- [ ] 참가자 <-> 호스트 리뷰

- [x] 경기 모집 완료 알람

- [ ] 경기 모집 실패 알람

  


<br>

#### 🧾API 목록

**User**

| ID   | 기능           | Method | URI                   | 비고 |
| :--- | -------------- | ------ | --------------------- | ---- |
| 1    | 회원가입       | POST   | /users/signup*        |      |
| 2    | 로그인         | POST   | /users/login          |      |
| 3    | 로그아웃       | POST*  | /users/logout         |      |
| 4    | 유저 정보      | GET    | /users/\<int:user_id> |      |
| 5    | 회원 탈퇴      | DELETE | /users/\<int:user_id> |      |
| 6    | 회원 정보 수정 | PATCH  | /users/\<int:user_id> |      |
| 7    | 탈퇴 회원 복구 | PUT    | /users/\<int:user_id> |      |
| 8    | 토큰 재발급    | *      | **                    |      |
| 9    |                |        |                       |      |
| 10   |                |        |                       |      |
| 11   |                |        |                       |      |
| 12   |                |        |                       |      |
| 13   |                |        |                       |      |
| 14   |                |        |                       |      |

**Games**

| ID   | 기능                  | Method | URI                                           | 비고                       |
| ---- | --------------------- | ------ | --------------------------------------------- | -------------------------- |
| 1    | 경기 목록 조회        | GET    | /games*                                       | 검색 조건 querystring 추가 |
| 2    | 경기 등록             | POST   | /games                                        |                            |
| 3    | 경기 정보 조회        | GET    | /games/\<int:game_id>                         |                            |
| 4    | 경기 참여자 목록 조회 | GET    | /games/\<int:game_id>/players                 |                            |
| 5    | 경기 참여             | POST   | /games/\<int:game_id>/players*                | 정정 필요                  |
| 6    | 참여자 정보 조회      | GET    | /games/\<int:game_id>/players/\<int:user_id>  |                            |
| 7    | 경기 참여 취소        | DELETE | /games/\<int:game_id>/players/\<int:user_id>* | 정정 필요                  |
| 8    |                       |        |                                               |                            |
| 9    |                       |        |                                               |                            |

**Payments**

| ID   | 기능      | Method | URI                                                      | 비고      |
| ---- | --------- | ------ | -------------------------------------------------------- | --------- |
| 1    | 결제 준비 | POST   | participations/\<int:participation_id>/payment-requests/ |           |
| 2    | 결제 승인 | POST   | requests/\<int:payment_request_id>/approval/             |           |
| 3    | 결제 실패 | POST   | requests/\<int:payment_request_id>/fail/*                | 정정 필요 |
| 4    | 결제 취소 | POST   | requests/\<int:payment_request_id>/cancel/*              | 정정 필요 |
| 5    |           |        |                                                          |           |
| 6    |           |        |                                                          |           |
| 7    |           |        |                                                          |           |
| 8    |           |        |                                                          |           |
| 9    |           |        |                                                          |           |
