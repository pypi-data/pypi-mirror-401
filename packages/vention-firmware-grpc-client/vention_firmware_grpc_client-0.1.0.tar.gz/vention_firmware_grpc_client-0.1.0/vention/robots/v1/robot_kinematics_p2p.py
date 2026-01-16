# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3.1](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 6.32.1 
# Pydantic Version: 2.11.10 
from .frame_p2p import Frame
from .joint_position_p2p import JointPosition
from enum import IntEnum
from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
import typing

class KinResultCode(IntEnum):
    KIN_RESULT_CODE_UNSPECIFIED = 0
    KIN_RESULT_CODE_ROBOT_NOT_FOUND = 1
    KIN_RESULT_CODE_SUCCESS = 2
    KIN_RESULT_CODE_FAILED = 3
    KIN_RESULT_CODE_BAD_INPUT = 4
    KIN_RESULT_CODE_EXCEEDS_JOINT_LIMITS = 5
    KIN_RESULT_CODE_SINGULARITY = 6
    KIN_RESULT_CODE_SELF_COLLISION = 7
    KIN_RESULT_CODE_IK_NOT_FOUND = 8

class ForwardKinematicsRequest(BaseModel):
    id: str = Field(default="")
    joint_position: JointPosition = Field(default_factory=JointPosition)# Joint positions in radians

class ForwardKinematicsResponse(BaseModel):
    model_config = ConfigDict(validate_default=True)
    cartesian_pose: Frame = Field(default_factory=Frame)# Cartesian pose
    result_code: KinResultCode = Field(default=0)# Result for the FK computation
    error_message: str = Field(default="")# Error message if success is false

class JointRangeConstraints(BaseModel):
    joint_index: int = Field(default=0)# Index of the joint (zero-based indexing from base to end-effector)
    min_position: float = Field(default=0.0)# Minimum joint position in radians
    max_position: float = Field(default=0.0)# Maximum joint position in radians

class InverseKinematicsRequest(BaseModel):
    id: str = Field(default="")
    seed_joint_position: JointPosition = Field(default_factory=JointPosition)
    target_pose: Frame = Field(default_factory=Frame)# Target cartesian pose
    joint_constraints: typing.List[JointRangeConstraints] = Field(default_factory=list)# Optional joint constraints

class InverseKinematicsResponse(BaseModel):
    model_config = ConfigDict(validate_default=True)
    joint_position: JointPosition = Field(default_factory=JointPosition)# Joint positions in radians
    result_code: KinResultCode = Field(default=0)# Result for the IK computation
    error_message: str = Field(default="")# Error message if not success

class InverseKinematicsBatchRequest(BaseModel):
    """
     Request for batch computation of inverse kinematics
    """

    id: str = Field(default="")# Robot ID
    seed_joint_position: JointPosition = Field(default_factory=JointPosition)# Seed joint position vector in radians
    target_poses: typing.List[Frame] = Field(default_factory=list)# List of target cartesian poses with each solution started at the given seed joint position.

class InverseKinematicsBatchResponse(BaseModel):
    """
     Response for batch computation of inverse kinematics
    """

    responses: typing.List[InverseKinematicsResponse] = Field(default_factory=list)# List of responses. Each solution corresponds to the pose at the same index in the request.
