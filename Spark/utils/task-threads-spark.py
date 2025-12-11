
# spark task thread python
# pip install pyspark[sql]

from pyspark.sql import SparkSession
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# SparkSession 초기화
spark = SparkSession.builder \
    .appName("SparkThreadFileLoad") \
    .getOrCreate()

# 처리할 파일 목록
file_paths = ["path/to/file1.csv", "path/to/file2.csv", "path/to/file3.csv"]

def load_and_process(file_path):
    """각 파일 경로를 받아 데이터를 로드하고 간단한 처리를 수행하는 함수"""
    try:
        print(f"[{time.strftime('%H:%M:%S')}] {file_path} 로딩 시작...")
        df = spark.read.csv(file_path, header=True, inferSchema=True)
        # 간단한 카운트와 같은 작업
        count = df.count()
        print(f"[{time.strftime('%H:%M:%S')}] {file_path} 로딩 완료. 레코드 수: {count}")
        return (file_path, count)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return (file_path, None)

# ThreadPoolExecutor를 사용하여 병렬 처리
# max_workers는 클러스터 환경에 맞게 조정 (예: Executor 수)
with ThreadPoolExecutor(max_workers=3) as executor:
    future_to_file = {executor.submit(load_and_process, path): path for path in file_paths}
    results = []
    for future in as_completed(future_to_file):
        results.append(future.result())

print("\n--- 모든 작업 완료 ---")
for path, count in results:
    print(f"파일: {path}, 레코드 수: {count}")

spark.stop()