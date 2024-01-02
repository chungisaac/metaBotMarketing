
import requests
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from tqdm import tqdm

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

from constants import UPLOAD_USER_ID, UPLOAD_APP_ID

userDataObject = resources_pb2.UserAppIDSet(user_id=UPLOAD_USER_ID, app_id=UPLOAD_APP_ID)
metadata = (('authorization', 'Key '),)

channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)


def stream_inputs(stub, metadata, per_page=1000):
  last_id = ''
  input_success_status = {
      status_code_pb2.INPUT_DOWNLOAD_SUCCESS, status_code_pb2.INPUT_DOWNLOAD_PENDING,
      status_code_pb2.INPUT_DOWNLOAD_IN_PROGRESS
  }

  while True:
    req = service_pb2.StreamInputsRequest(user_app_id=userDataObject, per_page=per_page, last_id=last_id)
    response = stub.StreamInputs(req, metadata=metadata)
    if not response.status.code not in input_success_status:
        raise Exception("Stream inputs failed with response %r" % response)
    if len(response.inputs) == 0:
        break
    else:
        for inp in response.inputs:
            last_id = inp.id
            yield inp

def get_raw_text(url):
    r = requests.get(url=url, headers={"Authorization": "Key ", "Content-Type": "text/plain; charset=utf-8"})
    # print(r.status_code, r.text, r.url, r.raw)
    return r.text
   

def main():
    input_stream = stream_inputs(stub, metadata, per_page=1000)
    inps = []
    for inp in tqdm(input_stream, desc='Getting input urls'):
        temp_dict = {'id': inp.id}
        temp_dict['url'] = inp.data.text.url
        inps.append(temp_dict)
    df = pd.DataFrame(inps)

    threads = []
    all_texts = []
    inp_urls = [x['url'] for x in inps]

    with ThreadPoolExecutor(max_workers=3) as executor:
        for chunk in tqdm(
            inp_urls,
            total=len(inp_urls),
            desc='Sending reqs'):
            threads.append(
                executor.submit(get_raw_text, chunk))
            time.sleep(0.01)

        for task in tqdm(
            as_completed(threads), total=len(inp_urls), desc='Getting responses'):
            all_texts.append(task.result())

    df['text'] = all_texts
    df.to_csv("links.csv", index=False, encoding='utf8')

if __name__ == '__main__':
    main()

