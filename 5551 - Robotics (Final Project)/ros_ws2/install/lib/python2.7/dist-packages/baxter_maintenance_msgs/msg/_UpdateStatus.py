# This Python file uses the following encoding: utf-8
"""autogenerated by genpy from baxter_maintenance_msgs/UpdateStatus.msg. Do not edit."""
import sys
python3 = True if sys.hexversion > 0x03000000 else False
import genpy
import struct


class UpdateStatus(genpy.Message):
  _md5sum = "74e246350421569590252c39e8aa7b85"
  _type = "baxter_maintenance_msgs/UpdateStatus"
  _has_header = False #flag to mark the presence of a Header object
  _full_text = """# See the class UpdateRunner()
# status:           One-word description of the current action being performed
# long_description: Details pertaining to status if any.  Used for verbose error messages.

uint16  status
float32 progress
string  long_description

uint16 STS_IDLE            = 0
uint16 STS_INVALID         = 1
uint16 STS_BUSY            = 2
uint16 STS_CANCELLED       = 3
uint16 STS_ERR             = 4
uint16 STS_MOUNT_UPDATE    = 5
uint16 STS_VERIFY_UPDATE   = 6
uint16 STS_PREP_STAGING    = 7
uint16 STS_MOUNT_STAGING   = 8
uint16 STS_EXTRACT_UPDATE  = 9
uint16 STS_LOAD_KEXEC      = 10

"""
  # Pseudo-constants
  STS_IDLE = 0
  STS_INVALID = 1
  STS_BUSY = 2
  STS_CANCELLED = 3
  STS_ERR = 4
  STS_MOUNT_UPDATE = 5
  STS_VERIFY_UPDATE = 6
  STS_PREP_STAGING = 7
  STS_MOUNT_STAGING = 8
  STS_EXTRACT_UPDATE = 9
  STS_LOAD_KEXEC = 10

  __slots__ = ['status','progress','long_description']
  _slot_types = ['uint16','float32','string']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       status,progress,long_description

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      super(UpdateStatus, self).__init__(*args, **kwds)
      #message fields cannot be None, assign default values for those that are
      if self.status is None:
        self.status = 0
      if self.progress is None:
        self.progress = 0.
      if self.long_description is None:
        self.long_description = ''
    else:
      self.status = 0
      self.progress = 0.
      self.long_description = ''

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types

  def serialize(self, buff):
    """
    serialize message into buffer
    :param buff: buffer, ``StringIO``
    """
    try:
      _x = self
      buff.write(_struct_Hf.pack(_x.status, _x.progress))
      _x = self.long_description
      length = len(_x)
      if python3 or type(_x) == unicode:
        _x = _x.encode('utf-8')
        length = len(_x)
      if python3:
        buff.write(struct.pack('<I%sB'%length, length, *_x))
      else:
        buff.write(struct.pack('<I%ss'%length, length, _x))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize(self, str):
    """
    unpack serialized message in str into this message instance
    :param str: byte array of serialized message, ``str``
    """
    try:
      end = 0
      _x = self
      start = end
      end += 6
      (_x.status, _x.progress,) = _struct_Hf.unpack(str[start:end])
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      if python3:
        self.long_description = str[start:end].decode('utf-8')
      else:
        self.long_description = str[start:end]
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e) #most likely buffer underfill


  def serialize_numpy(self, buff, numpy):
    """
    serialize message with numpy array types into buffer
    :param buff: buffer, ``StringIO``
    :param numpy: numpy python module
    """
    try:
      _x = self
      buff.write(_struct_Hf.pack(_x.status, _x.progress))
      _x = self.long_description
      length = len(_x)
      if python3 or type(_x) == unicode:
        _x = _x.encode('utf-8')
        length = len(_x)
      if python3:
        buff.write(struct.pack('<I%sB'%length, length, *_x))
      else:
        buff.write(struct.pack('<I%ss'%length, length, _x))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize_numpy(self, str, numpy):
    """
    unpack serialized message in str into this message instance using numpy for array types
    :param str: byte array of serialized message, ``str``
    :param numpy: numpy python module
    """
    try:
      end = 0
      _x = self
      start = end
      end += 6
      (_x.status, _x.progress,) = _struct_Hf.unpack(str[start:end])
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      if python3:
        self.long_description = str[start:end].decode('utf-8')
      else:
        self.long_description = str[start:end]
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e) #most likely buffer underfill

_struct_I = genpy.struct_I
_struct_Hf = struct.Struct("<Hf")
