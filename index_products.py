from pymongo import MongoClient

# MongoDB Atlas 클러스터 정보
atlas_username = 'haneum'
atlas_password = 'gksdldma001'
atlas_cluster = 'cluster0.qiemnkw.mongodb.net'
database_name = 'market_tracker'
product_trends_collection_name = 'product_trends'
index_collection_name = 'index_products'

# MongoDB Atlas 연결 URI 생성
uri = f"mongodb+srv://{atlas_username}:{atlas_password}@{atlas_cluster}/{database_name}?retryWrites=true&w=majority"

# MongoDB 클라이언트 생성
client = MongoClient(uri)

try:
    # 데이터베이스 선택
    db = client[database_name]

    # 컬렉션 선택
    product_trends_collection = db[product_trends_collection_name]
    index_products_collection = db[index_collection_name]

    # product_trends의 데이터를 가져와서 index_products에 맞게 변환
    cursor = product_trends_collection.find()  # 모든 product_trends 데이터 가져오기

    for document in cursor:
        name = document.get('product_name', 'Unknown')  # 상품 이름
        category = document.get('category_small', 'Unknown')  # 상품 소분류
        date = document.get('date', None)  # 날짜 정보
        price = document.get('price', None)  # 가격 정보

        # 가격이 유효한 숫자인지 확인
        try:
            price = int(price)  # 가격을 정수로 변환
        except (ValueError, TypeError):
            print(f"유효하지 않은 price 값 건너뜀: {document}")
            continue

        # 기존 제품 확인 (name을 기준으로)
        existing_product = index_products_collection.find_one({'name': name})

        if existing_product:
            # 기존 제품이 있으면 price_data 배열에 날짜와 가격을 추가
            index_products_collection.update_one(
                {'name': name},
                {
                    '$push': {'price_data': {'date': date, 'price': price}},
                    '$set': {'category': category}  # 기존 카테고리 값을 업데이트
                }
            )
            print(f'기존 제품 업데이트됨: {name}, 날짜: {date}, 추가된 가격: {price}, 카테고리: {category}')
        else:
            # 새로운 제품이면 새로운 문서를 삽입
            index_product = {
                'name': name,
                'category': category,  # category_small을 category 필드에 저장
                'price_data': [{'date': date, 'price': price}],  # 날짜와 가격 배열로 초기화
                'estimated_price': None  # 예상 가격을 null로 설정
            }
            index_products_collection.insert_one(index_product)
            print(f'새로운 제품 삽입됨: {name}, 날짜: {date}, 가격: {price}, 카테고리: {category}')

    print(f'데이터가 성공적으로 {index_collection_name} 컬렉션에 저장되었습니다.')

except Exception as e:
    print(f"오류 발생: {e}")

finally:
    # MongoDB 클라이언트 종료
    client.close()
