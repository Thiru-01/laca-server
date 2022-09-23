import os

from flask import Flask, request, jsonify
from main import *
from PIL import Image
app = Flask(__name__)


@app.route('/g_code', methods=['POST', 'GET'])
def hello_world():
    if request.method == "POST":
        fileName=""
        extension = request.files['media'].filename.split(".")[-1]
        if not request.files['media'].filename.endswith(".jpg"):
            request.files['media'].save(os.getcwd() + '\\' + request.files['media'].filename)
            img = Image.open(request.files['media'].filename)
            rgb_Image = img.convert('RGB')
            fileName=request.files['media'].filename.replace(".{}".format(extension), ".jpg")
            rgb_Image.save(request.files['media'].filename.replace(".{}".format(extension), ".jpg"))
            os.remove(os.getcwd() + '\\' + request.files['media'].filename)
        else:
            fileName = request.files['media'].filename.replace(".{}".format(extension), ".jpg")
            request.files['media'].save(os.getcwd() + '\\' + request.files['media'].filename)
        g_code = MyEffect()

        current_dir = os.getcwd()
        full_path = "{}\{}".format(current_dir, fileName)

        tempFileName = f"{fileName.split('.')[0]}.svg"
        asyncio.set_event_loop(asyncio.ProactorEventLoop())
        try:
            value = asyncio.get_event_loop().run_until_complete(doTrace(full_path.replace("\\", "/"), "posterized1"))
        except ConnectionResetError:
            value = asyncio.get_event_loop().run_until_complete(doTrace(full_path.replace("\\", "/"), "posterized1"))
        except Exception as e:
            
            print(e)
            return jsonify({
                'fileName': 'None',
                'contents': ['something went wrong'],
                'length': 0,
                'svg':'None'
            })
        Path(tempFileName).write_text(value, encoding="utf-8")

        g_code.affect([tempFileName])
        gcodeList = g_code.output()
        os.remove(tempFileName)
        content = gcodeList

        data = {
            'fileName': fileName,
            'contents': content,
            'length': len(content),
            'svg': value
        }
        os.remove(full_path)
        return jsonify(data)
    return jsonify({
        'fileName': 'None',
        'contents': ['something went wrong'],
        'length': 0,
        'svg': 'None'
    })


# main driver function
if __name__ == '__main__':
    app.run()
