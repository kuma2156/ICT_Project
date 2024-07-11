import requests
import xml.etree.ElementTree as ET
from pymongo import MongoClient

# MongoDB Atlas 클러스터 정보
atlas_username = 'haneum'
atlas_password = 'gksdldma001'
atlas_cluster = 'cluster0.qiemnkw.mongodb.net'
database_name = 'market_tracker'
collection_name = 'products'

# MongoDB Atlas 연결 URI 생성
uri = f"mongodb+srv://{atlas_username}:{atlas_password}@{atlas_cluster}/{database_name}?retryWrites=true&w=majority"

# MongoDB 클라이언트 생성
client = MongoClient(uri)

try:
    # 데이터베이스와 컬렉션 선택
    db = client[database_name]
    collection = db[collection_name]

    # 데이터베이스 및 컬렉션 존재 여부 확인
    if database_name in client.list_database_names():
        db = client[database_name]
        if collection_name in db.list_collection_names():
            print(f"데이터베이스 '{database_name}'와 컬렉션 '{collection_name}'이 이미 존재합니다.")
        else:
            print(f"컬렉션 '{collection_name}'을 생성합니다.")
            db.create_collection(collection_name)
    else:
        print(f"데이터베이스 '{database_name}'가 존재하지 않습니다. 새로 생성합니다.")
        db = client[database_name]
        db.create_collection(collection_name)

    # API 엔드포인트 및 인증키 설정
    api_url = 'http://openapi.price.go.kr/openApiImpl/ProductPriceInfoService/getProductInfoSvc.do'
    auth_key = 'dFxt8tFz/VBYDSYGtl6SG7MTLy95uwA4qCgLwwoWcBsT3sHm1KZzrLKOYqUkxR/ZFujGL4+Z/Ety3YHsFO0Yqw=='

    # 요청 파라미터 설정
    params = {
        'serviceKey': auth_key,
        '_type': 'xml'
    }

    # API 호출
    response = requests.get(api_url, params=params)
    
    # HTTP 응답 상태 코드 확인
    if response.status_code == 200:
        print('API 호출 성공')
        #print(f'Response content: {response.content.decode("utf-8")}')  # API 응답 확인
        
        # XML 데이터 파싱
        root = ET.fromstring(response.content)
        
        # 결과 코드 확인
        result_code = root.findtext('resultCode')
        result_msg = root.findtext('resultMsg')
        
        if result_code == '00':
            print('결과 코드: 00')
            
            # 성공적으로 데이터를 가져왔을 때 처리
            items = root.findall('.//item')  # 모든 'item' 태그를 찾습니다.
            products_to_insert = []

            for item in items:
                product_data = {
                    'goodId': item.findtext('goodId'),
                    'goodName': item.findtext('goodName'),
                    'goodUnitDivCode': item.findtext('goodUnitDivCode'),
                    'goodBaseCnt': item.findtext('goodBaseCnt'),
                    'goodSmlclsCode': item.findtext('goodSmlclsCode'),
                    'detailMean': item.findtext('detailMean'),
                    'goodTotalCnt': item.findtext('goodTotalCnt'),
                    'goodTotalDivCode': item.findtext('goodTotalDivCode'),
                    'productEntpCode': item.findtext('productEntpCode')
                }

                products_to_insert.append(product_data)

            # 기존 데이터 삭제
            delete_result = collection.delete_many({})
            print(f'Deleted {delete_result.deleted_count} documents from MongoDB.')

            # MongoDB에 데이터 삽입
            if products_to_insert:
                result = collection.insert_many(products_to_insert)
                print(f'Inserted {len(result.inserted_ids)} documents into MongoDB.')
            else:
                print('API에서 반환한 데이터가 없습니다.')

            # 모든 문서 조회
            all_documents = collection.find()
                
        else:
            # API 호출 실패 시 처리
            print(f'API 호출 실패: {result_code} - {result_msg}')
    else:
        # HTTP 요청 실패 시 처리
        print(f'HTTP 요청 실패: {response.status_code}')

except requests.exceptions.RequestException as e:
    # 네트워크 연결 문제 등의 예외 처리
    print(f'API 호출 중 에러 발생: {e}')
except ET.ParseError as e:
    # XML 파싱 에러 처리
    print(f'XML 파싱 에러: {e}')
except Exception as e:
    # 기타 예외 처리
    print(f'오류 발생: {e}')
finally:
    # MongoDB 클라이언트 종료
    client.close()
