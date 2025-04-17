# 한이음 가격변동 예측 프로젝트

![프로젝트 이미지](https://github.com/user-attachments/assets/7515c996-fedd-4e67-8631-294892e4d5da)

## 프로젝트 개요
이 프로젝트는 **가격 변동 예측** 모델을 개발하는 것을 목표로 하며, 주어진 데이터를 기반으로 가격 변동을 예측하고 시장 변화를 파악하는 시스템을 구현합니다.

---

## 팀 구성
| 역할             | 팀원      | 주요 작업                                                                                              |
|------------------|-----------|-------------------------------------------------------------------------------------------------------|
| **백엔드**        | 김명규    | 데이터베이스 설계, 데이터 전처리 및 가공,  데이터 클린징 및 관리                            |
| **프론트엔드**     | 강석현    | 사용자 인터페이스(UI) 개발, 가격 변동 예측 결과 시각화(차트 구현) ,API                                     |
| **데이터 분석**    | 고욱현    | 예측 모델 개발, 데이터 분석, 모델 평가 및 성능 향상                                                 |
| **시스템 관리자**  | 김명준    | 서버 배포, 운영 환경 설정, 데이터 보안 관리                                                        |

---

<div align="left">
    <h1>💻 백엔드</h1>
    <table>
        <tr>
            <td align="center"><img src="https://github.com/user-attachments/assets/61049fd5-5e06-4b17-bb51-d925ea3e68dc" width="250"></td>
        </tr>
        <tr>
            <td align="center"><b>김명규</b></td>
        </tr>
        <tr>
            <td align="center"><b>https://github.com/kuma2156</b></td>
        </tr>
    </table>
</div>


## 주요 역할 및 기능

#### **주요 역할**:
- **데이터베이스 설계 및 관리**:
    - **MongoDB**를 사용하여 대용량의 실시간 가격 변동 데이터를 처리하고 저장
    - 데이터 모델 설계: 가격 변동 및 예측 데이터의 효율적인 저장을 위한 컬렉션 구조 설계
    - **인덱스 최적화**: 빠른 조회를 위해 적절한 인덱스를 설정하여 데이터베이스 성능 최적화

- **데이터 정제 및 전처리**:
    - 원본 데이터를 분석하여 필요 없는 데이터를 필터링하고, 결측값 및 이상값을 처리
    - **데이터 정리**: 실시간 데이터와 예측 결과를 결합하여 분석 및 예측에 적합한 형태로 변환
    - **데이터 클린징**: 데이터의 정확성을 보장하기 위해 정기적인 클린징 작업 수행

- **API 통합 및 데이터 연동**:
    - RESTful API를 통해 외부 시스템과의 데이터 통합
    - 실시간으로 변동하는 가격 데이터를 MongoDB에 저장하고, 이를 API로 호출하여 실시간 업데이트 처리

---

## 데이터 구조
<div align="left">
    <table>
        <tr>
            <td h3>데이터 흐름</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/user-attachments/assets/112d2999-80b7-40d8-aae6-87066056e047" width="700"></td>
        </tr>
    </table>
</div>

| 데이터 단계          | 설명                                                                                              |
|----------------------|---------------------------------------------------------------------------------------------------|
| **수집된 원본 데이터** | JSON, CSV 형식으로 외부 시스템에서 제공됨                                                      |
| **데이터베이스**      | MongoDB: 시간에 따른 변동 데이터를 저장하고 대용량 데이터 처리                                  |
| **데이터 처리 과정**  | 1. **데이터 정제**: 누락된 값 및 불필요한 데이터 제거<br> 2. **변환**: 예측 모델에 맞는 형태로 변환<br> 3. **가공**: 예측 모델 학습을 위한 데이터 가공 |

### 데이터베이스 설계


### 🗄️ 데이터베이스 (Database)
<table style="background:white; padding:10px; border-radius:8px;">
    <tr>
        <td align="center">
            <img src="https://github.com/user-attachments/assets/fc3295ef-a7ad-4bc6-a680-92acf3598804" width="64" height="64">
        </td>
    </tr>
    <tr>
        <td align="center"><b>MySQL</b></td>
    </tr>
</table>

---

### ☁️ 배포 및 기타 (Deployment & DevOps)
<table style="background:white; padding:10px; border-radius:8px;">
    <tr>
        <td align="center">
            <img src="https://github.com/user-attachments/assets/e4a176de-bf94-4f83-b45c-eb79492f4477" width="64" height="64">
        </td>
        <td align="center">
            <img src="https://github.com/user-attachments/assets/67ebb9cf-313a-419f-9edc-5654750bad30" width="64" height="64">
        </td>
    </tr>
    <tr>
        <td align="center"><b>PM2</b></td>
        <td align="center"><b>GitHub</b></td>
    </tr>
</table>


#### **MongoDB 데이터 모델**
MongoDB를 사용하여 가격 변동 데이터를 효율적으로 처리할 수 있는 구조를 설계했습니다. 주요 컬렉션은 아래와 같습니다.

1. **price_data** 컬렉션
    - 항목: `상품명`, `가격`, `거래량`, `날짜`
    - 예시 데이터:
    ```json
    {
        "상품명": "상품1",
        "가격": "1000원",
        "거래량": "200개",
        "날짜": "2025-04-01"
    }
    ```

2. **price_change_data** 컬렉션
    - 항목: `상품명`, `시간`, `가격`, `변동률`
    - 예시 데이터:
    ```json
    {
        "시간": "2025-04-01 10:00:00",
        "상품명": "상품1",
        "가격": "1020원",
        "변동률": "+2%"
    }
    ```

### 인덱스 설계
- **상품명**과 **날짜** 필드에 인덱스를 설정하여 가격 변동 데이터를 빠르게 조회할 수 있도록 최적화
- 예시:
  ```javascript
  db.price_data.createIndex({"상품명": 1, "날짜": -1});
  db.price_change_data.createIndex({"상품명": 1, "시간": -1});
