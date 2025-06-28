import os
import asyncio
from mem0 import AsyncMemoryClient

# Mem0 클라이언트 초기화 및 사용자 ID 설정
client = AsyncMemoryClient(api_key=os.getenv("MEM0_API_KEY"))
user_id = "dabid"

async def add_to_memory(content: str) -> str:
    """메모리에 메시지를 추가하는 함수"""
    messages = [{"role": "user", "content": content}]
    await client.add(messages, user_id=user_id, output_format="v1.1")
    return f"저장된 메시지: {content}"

async def search_memory(query: str) -> str:
    """메모리에서 특정 키워드로 검색하는 함수"""
    memories = await client.search(query, user_id=user_id, output_format="v1.1")
    results = '\n'.join([result["memory"] for result in memories["results"]])
    return str(results)

async def get_all_memory() -> str:
    """저장된 모든 메모리를 가져오는 함수"""
    memories = await client.get_all(user_id=user_id, output_format="v1.1")
    results = '\n'.join([result["memory"] for result in memories["results"]])
    return str(results)


async def delete_all_memory() -> str:
    """저장된 모든 메모리를 삭제하는 함수"""
    result = await client.delete_all(user_id=user_id)
    return f"메모리 삭제 결과: {result}"



async def main():
    # 예제 1: 메모리 추가하기
    print("\n=== 메모리 추가하기 ===")
    
    await add_to_memory("오늘 서울의 날씨가 정말 좋네요. 하늘도 맑고 기온도 딱 좋아서 산책하기 좋은 날씨입니다. 이런 날에는 한강공원에 가서 피크닉을 하면 좋을 것 같아요.")
    
    # await add_to_memory("파이썬으로 새로운 프로젝트를 시작했는데 정말 재미있습니다. 특히 비동기 프로그래밍과 API 통합하는 부분을 배우고 있는데, 처음에는 어려웠지만 점점 이해가 되면서 흥미가 생기네요. 다음에는 데이터 분석 라이브러리도 공부해보고 싶습니다.")
    
    # # 예제 2: 메모리 검색하기
    # print("\n=== 메모리 검색하기 ===")
    # search_result = await search_memory("날씨")
    # print("'날씨' 검색 결과:")
    # print(search_result)
    
    # # 예제 3: 모든 메모리 가져오기
    # print("\n=== 모든 메모리 가져오기 ===")
    # all_memories = await get_all_memory()
    # print("저장된 모든 메모리:")
    # print(all_memories)

if __name__ == "__main__":
    # MEM0_API_KEY 환경 변수가 설정되어 있는지 확인
    if not os.getenv("MEM0_API_KEY"):
        print("MEM0_API_KEY 환경 변수를 설정해주세요")
    else:
        asyncio.run(main())
