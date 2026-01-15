import grpc
from .rootcert import ROOT_CERTIFICATE
from datetime import datetime, timezone
from typing import Any
from .pb import sl5_api_pb2
from .pb import sl5_api_pb2_grpc

class Config:
  target: str = 'localhost:23505'
  token: str

  def __init__(self, target: str, token: str):
    self.target = target
    self.token = token

class Client:
  __channel: grpc.aio.Channel
  __tag_stub: sl5_api_pb2_grpc.TagServiceStub

  def __init__(self, config: Config):

    call_credentials = grpc.access_token_call_credentials(config.token)

    channel_credentials = grpc.ssl_channel_credentials(
      root_certificates=ROOT_CERTIFICATE,
    )

    composite_credentials = grpc.composite_channel_credentials(
      channel_credentials,
      call_credentials,
    )

    self.__channel = grpc.aio.secure_channel(config.target, composite_credentials)
    self.__tag_stub = sl5_api_pb2_grpc.TagServiceStub(self.__channel)
   
  async def __aenter__(self):
    return self
  
  async def __aexit__(self, exc_type, exc_val, exc_tb):
    await self.close(None)
   
  async def close(self, grace: float | None):
    await self.__channel.close(grace)
    
  async def read_value(self, tag_name: str) -> Any:
    """
    Args:
      tag_name (str): Название тега в вистеме

    Returns:
      Any: Значение тега

    Raises:
      grpc.aio._call.AioRpcError: Ошибка со стороны сервера
    """

    req = sl5_api_pb2.TagReadValueRequest(names=[tag_name])
    res = await self.__tag_stub.ReadValues(req)
    pb_value = res.values[0]
    any_value = pbvalue_to_any(pb_value)
    return any_value
  
  async def write_value(self, tag_name: str, new_value: Any, new_quality: int) -> None:
    pb_value = any_to_pbvalue(new_value)
    wv = sl5_api_pb2.WriteValue(
      tag_name=tag_name,
      quality=new_quality,
      value=pb_value,
    )
    req = sl5_api_pb2.TagWriteValueRequest(wvs=[wv])
    await self.__tag_stub.WriteValues(req)

def pbvalue_to_any(src: sl5_api_pb2.SLValue) -> Any:
  kind = src.WhichOneof("kind")
  match kind:
    case "double_value":
      return src.double_value
    
    case "string_value":
      return src.string_value
    
    case "bool_value":
      return src.bool_value
    
    case "int32_value":
      return src.int32_value
    
    case "int64_value":
      return src.int64_value
    
    case "uint32_value":
      return src.uint32_value
    
    case "uint64_value":
      return src.uint64_value    
    
    case "time_value":
      v = src.time_value.ToDatetime(tzinfo=timezone.utc)
      # map v to localtime timezone
      v = v.astimezone(tz=None)
      return v
    case _:
      raise Exception(f"unsupported type {kind}")
    
def any_to_pbvalue(src: Any) -> sl5_api_pb2.SLValue:

  if isinstance(src, bool):
    return sl5_api_pb2.SLValue(bool_value=src)
  
  if isinstance(src, datetime):
    v = src.astimezone(tz=timezone.utc)
    return sl5_api_pb2.SLValue(time_value=v)

  match src:
    case int(v):
      dst = sl5_api_pb2.SLValue(int64_value=v)

    case float(v):
      dst = sl5_api_pb2.SLValue(double_value=v)

    case str(v):
      dst = sl5_api_pb2.SLValue(string_value=v)

    case _:
      raise ValueError(f"cannot cast {type(src)} to SLValue")

  return dst
    