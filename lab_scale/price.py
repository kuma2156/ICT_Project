import pandas as pd
from pymongo import MongoClient

# MongoDB Atlas 클러스터 정보
atlas_username = 'haneum'
atlas_password = 'gksdldma001'
atlas_cluster = 'cluster0.qiemnkw.mongodb.net'
database_name = 'market_tracker'
collection_name = 'product_trends'

# MongoDB Atlas 연결 URI 생성
uri = f"mongodb+srv://{atlas_username}:{atlas_password}@{atlas_cluster}/{database_name}?retryWrites=true&w=majority"

# MongoDB 클라이언트 생성
client = MongoClient(uri)

try:
    # 데이터베이스와 컬렉션 선택
    db = client[database_name]
    collection = db[collection_name]

    # 데이터베이스 및 컬렉션 존재 여부 확인 후 생성
    if database_name in client.list_database_names():
        db = client[database_name]
        if collection_name in db.list_collection_names():
            print(f"컬렉션 '{collection_name}'이 이미 존재합니다. 기존 데이터를 삭제하고 새로 적재합니다.")
            # 기존 데이터 삭제
            delete_result = collection.delete_many({})
            print(f"기존 데이터 {delete_result.deleted_count} 개를 삭제했습니다.")
        else:
            print(f"컬렉션 '{collection_name}'을 생성합니다.")
            db.create_collection(collection_name)
    else:
        print(f"데이터베이스 '{database_name}'가 존재하지 않습니다. 새로 생성합니다.")
        db = client[database_name]
        db.create_collection(collection_name)

    # 엑셀 파일 경로 설정
    excel_files = ['data/생필품상품별_동향1.xls', 'data/생필품상품별_동향2.xls']
    sheet_names = ['생필품상품별동향']  # 각각의 시트명에 맞게 설정해주세요

    # 엑셀 파일에서 데이터 읽기
    for excel_file, sheet_name in zip(excel_files, sheet_names):
        # 엑셀 파일에서 데이터 읽기
        df = pd.read_excel(excel_file, sheet_name=sheet_name)

        # MongoDB에 적재할 데이터 생성
        products_to_insert = []
        for index, row in df.iterrows():
            for date_column in df.columns[10:]:  # 날짜 컬럼은 10번 인덱스부터 마지막까지
                # 가격 데이터 가져오기
                price_str = str(row[date_column])
                if '/' in price_str:
                    price_cleaned = price_str.split('/')[0].strip()  # '/' 기준으로 나눠 첫 번째 값 사용
                elif '-' in price_str:
                    price_cleaned = ''  # '-'는 비워둠
                else:
                    price_cleaned = price_str  # 다른 경우는 그대로 사용

                # 데이터 포맷 생성
                product_data = {
                    'date': date_column,        # 날짜 정보 추가
                    'price': price_cleaned,     # 가격 정보 추가
                    'number': row['번호'],
                    'product_name': row['상품명'],
                    'category_main': row['대분류명'],
                    'category_middle': row['중분류명'],
                    'category_small': row['소분류명'],
                    'manufacturer': row['제조사명'],
                    'total_capacity': row['총용량'],
                    'total_capacity_unit': row['총용량명'],
                    'unit_capacity': row['단위용량'],
                    'unit_capacity_unit': row['단위용량명']
                }
                products_to_insert.append(product_data)

        # MongoDB에 데이터 삽입
        if products_to_insert:
            result = collection.insert_many(products_to_insert)
            print(f"'{excel_file}'의 '{sheet_name}' 시트에서 {len(result.inserted_ids)} 개의 문서를 MongoDB에 삽입했습니다.")
        else:
            print(f"'{excel_file}'의 '{sheet_name}' 시트에서 삽입할 데이터가 없습니다.")

except Exception as e:
    print(f"오류 발생: {e}")

finally:
    # MongoDB 클라이언트 종료
    client.close()
