import asyncio
import argparse
import time
from policelibrary import asr_wav


async def asr_test(file_path: str):
    async for text, definite in asr_wav(file_path):
        print(f"识别结果: {text} (确定: {definite})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, default="/root/vepfs/projects2026/police/policelibrary/assets/xiaozhan_rate_16000.wav")
    args = parser.parse_args()

    start_time = time.time()
    asyncio.run(asr_test(args.file))
    end_time = time.time()
    print(f"识别时间: {end_time - start_time}秒")