import os

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

from constants import UPLOAD_USER_ID, UPLOAD_APP_ID

class ClarifaiUploader:
    def __init__(self):
        self.userDataObject = resources_pb2.UserAppIDSet(user_id=UPLOAD_USER_ID, app_id=UPLOAD_APP_ID)
        self.metadata = (('authorization', 'Key ' + os.environ.get("CLARIFAI_PAT_PROD")),)

        channel = ClarifaiChannel.get_grpc_channel()
        self.stub = service_pb2_grpc.V2Stub(channel)

    def upload(self, raw_text: str):
        post_inputs_response = self.stub.PostInputs(
            service_pb2.PostInputsRequest(
                user_app_id=self.userDataObject,
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            text=resources_pb2.Text(
                                raw=raw_text
                            )
                        )
                    )
                ]
            ),
            metadata=self.metadata
        )

        if post_inputs_response.status.code != status_code_pb2.SUCCESS:
            print(post_inputs_response.status)
            raise Exception("Post inputs failed, status: " + post_inputs_response.status.description)
        
