import uvicorn
import os
from dotenv import load_dotenv
import sys
import pathlib

load_dotenv()

current_dir = pathlib.Path(__file__).resolve().parent
src_dir = current_dir / 'src'
sys.path.append(str(src_dir))

if __name__ == '__main__':

    PORT = int(os.getenv('PORT', 8000))
    HOST = os.getenv('HOST', '0.0.0.0')

    # print(sys.path)

    uvicorn.run(
        app='src.app:app',
        host=HOST,
        port=PORT,
        log_level="info",
        reload=True
    )