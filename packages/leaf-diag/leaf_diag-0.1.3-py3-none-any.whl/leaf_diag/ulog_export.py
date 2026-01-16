from enum import unique
from math import log
import os
from unittest.mock import Base
from matplotlib import pyplot as plt
import pandas as pd
import json
import io

from pydantic import BaseModel, Field, ValidationError

from .data_loader import (
    MotorCommandSignal,
    load_rosbag, 
    load_ulg, 
    CartesianSignal,
    OrientationSignal,
    UlogPositionSignal,
    UlogVelocitySignal,
    UlogAccelerationSignal,
    UlogRawAccelerationSignal,
    UlogOrientationSignal,
    UlogSignal,
    RosSignal,
    UlogCartesianSignal,
    UlogGPSVelocitySignal,
    UlogAngularSignal,
    ULogGPSPositionSignal,
    UlogMotorCommandSignal,
    UlogOFVelocity,
    UlogHeading,
    UlogEstimatorOFVelocity,
    UlogGyroHeading
)

import logging

logger = logging.getLogger(__name__)

from .data_sync import SignalSynchronizer, SignalSynchronizerMulti, SignalSynchronizerSingle

from typing import IO, Dict, Tuple, Union, List, Optional, Literal

import rosbag
import rospy

from geometry_msgs.msg import Vector3, Quaternion
from std_msgs.msg import Float32, Float32MultiArray
from tqdm import tqdm

# In ROS, you can write any valid ROS message type to a bag file. Some common message types include:

# 1. Standard primitive messages (`std_msgs`):
#     - `std_msgs/Bool`, `std_msgs/String`
#     - `std_msgs/Int8/16/32/64`, `std_msgs/UInt8/16/32/64`
#     - `std_msgs/Float32`, `std_msgs/Float64`

# 2. Geometry messages:
#     - `geometry_msgs/Point`, `geometry_msgs/Vector3`
#     - `geometry_msgs/Quaternion`, `geometry_msgs/Pose`
#     - `geometry_msgs/PoseStamped`, `geometry_msgs/Transform`
#     - `geometry_msgs/Twist`, `geometry_msgs/Wrench`

# 3. Sensor messages:
#     - `sensor_msgs/Image`, `sensor_msgs/PointCloud2`
#     - `sensor_msgs/Imu`, `sensor_msgs/NavSatFix`
#     - `sensor_msgs/LaserScan`, `sensor_msgs/JointState`

# 4. Navigation messages:
#     - `nav_msgs/Odometry`, `nav_msgs/Path`
#     - `nav_msgs/OccupancyGrid`, `nav_msgs/MapMetaData`

# 5. Custom messages:
#     - Any message type defined in your ROS packages

# Your current function needs to be more flexible to handle different message types based on the data structure.

def add_df_to_bag(
        bag: rosbag.Bag, 
        df: pd.DataFrame,
        topic: str, 
        msg_type_str: str, 
        field_mapping: dict = None
    ):
    """
    Add data from a CSV file to a ROS bag.
    
    Args:
        bag: ROS bag object to write to
        df: DataFrame containing the data to write
        topic: Topic name to publish the data to
        msg_type_str: String identifier for the message type ("vector3", "quaternion", "float32", etc.)
        field_mapping: Dictionary mapping CSV columns to message fields (e.g. {"f_ax": "x", "f_ay": "y", "f_az": "z"})
                     If None, will attempt to match automatically
    Raises:
        Exception: If there is an error writing to the bag or processing the DataFrame
    """
    
    try:
        # Create appropriate message type
        if msg_type_str.lower() == "vector3":
            
            # For acceleration, position, velocity data
            if field_mapping is None:
                # Try to guess mapping based on common patterns
                if all(col in df.columns for col in ['f_ax', 'f_ay', 'f_az']):
                    field_mapping = {'f_ax': 'x', 'f_ay': 'y', 'f_az': 'z'}
                elif all(col in df.columns for col in ['x', 'y', 'z']):
                    field_mapping = {'x': 'x', 'y': 'y', 'z': 'z'}
            
            for _, row in tqdm(df.iterrows(), desc=f"Processing {topic}", total=len(df)):
                msg = Vector3()
                for csv_field, msg_field in field_mapping.items():
                    setattr(msg, msg_field, float(row[csv_field]))
                
                # Convert timestamp to ROS time
                timestamp = rospy.Time.from_sec(float(row['timestamp']))
                bag.write(topic, msg, timestamp)
                
        elif msg_type_str.lower() == "float32_multi_array":
            # For motor commands
            if field_mapping is None:
                # Try to guess mapping based on common patterns
                if all(col in df.columns for col in ['f_control_0_', 'f_control_1_', 'f_control_2_', 'f_control_3_']):
                    field_mapping = {i: f"f_control_{i}_" for i in range(4)}
            
            for _, row in tqdm(df.iterrows(), desc=f"Processing {topic}", total=len(df)):
                msg = Float32MultiArray()
                msg.data = [float(row[col]) for col in field_mapping.keys()]
                
                # Convert timestamp to ROS time
                timestamp = rospy.Time.from_sec(float(row['timestamp']))
                bag.write(topic, msg, timestamp)

        elif msg_type_str.lower() == "float32":
            # For GPS fix type
            if field_mapping is None:
                # Try to guess mapping based on common patterns
                if all(col in df.columns for col in ['f_fix_type']):
                    field_mapping = {'f_fix_type': 'data'}
            
            for _, row in tqdm(df.iterrows(), desc=f"Processing {topic}", total=len(df)):
                msg = Float32()
                for csv_field, msg_field in field_mapping.items():
                    setattr(msg, msg_field, float(row[csv_field]))
                
                # Convert timestamp to ROS time
                timestamp = rospy.Time.from_sec(float(row['timestamp']))
                bag.write(topic, msg, timestamp)

    except Exception as e:
        rospy.logerr(f"Error writing to bag {bag.filename} on topic {topic}: {e}")
        raise e


def get_df_from_bag(
        bag: rosbag.Bag,
        topic: str,
        msg_type_str: str,
        field_mapping: dict = None
    ) -> pd.DataFrame:
    """
    Extract data from a ROS bag topic into a DataFrame.
    
    Args:
        bag: ROS bag object to read from
        topic: Topic name to extract data from
        msg_type_str: String identifier for the message type ("vector3", "quaternion", "float32", etc.)
        field_mapping: Dictionary mapping message fields to DataFrame columns (e.g. {"x": "f_ax", "y": "f_ay", "z": "f_az"})
                     If None, will attempt to match automatically
    Returns:
        df: DataFrame containing the extracted data
    """
    data = []
    for topic, msg, t in bag.read_messages(topics=[topic]):
        row = {"timestamp": t.to_sec()}
        
        if msg_type_str.lower() == "vector3":
            if field_mapping is None:
                field_mapping = {'x': 'x', 'y': 'y', 'z': 'z'}
            for msg_field, df_field in field_mapping.items():
                row[df_field] = getattr(msg, msg_field)
        
        elif msg_type_str.lower() == "float32_multi_array":
            if field_mapping is None:
                field_mapping = {i: f"f_control_{i}_" for i in range(len(msg.data))}
            for i, df_field in field_mapping.items():
                row[df_field] = msg.data[i]
        
        elif msg_type_str.lower() == "float32":
            if field_mapping is None:
                field_mapping = {'data': 'data'}
            for msg_field, df_field in field_mapping.items():
                row[df_field] = getattr(msg, msg_field)
        
        data.append(row)

    df = pd.DataFrame(data)
    return df


class SignalConfigDict(BaseModel):
    signal_key: str = Field(..., description="Key of the signal in the signal dictionary")
    signal_df_key: Optional[str] = Field(None, description="Key of the signal in the DataFrame dictionary")
    signal_df_keys: Optional[List[str]] = Field(None, description="List of keys for multi-instance signals in the DataFrame dictionary")
    signal_source: Literal["ros", "ulog"] = Field(..., description="Source of the signal: 'ros' or 'ulog'")
    is_multi: bool = Field(False, description="Whether the signal is multi-instance")
    n_channels: Optional[int] = Field(None, description="Number of channels for multi-instance signals")
    topic: Optional[str] = Field(None, description="ROS topic name for the signal")
    topics: Optional[List[str]] = Field(None, description="List of ROS topic names for multi-instance signals")
    msg_type: Optional[str] = Field(None, description="ROS message type for the signal")
    field_mapping: Optional[dict] = Field(None, description="Field mapping for the signal")


class BagBuffer(io.BytesIO):
    """BytesIO that looks enough like an open(…, 'wb') file
    for rosbag.Bag to accept it."""
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.mode = "wb+"          # rosbag checks this

    def close(self):
        """
        rosbag calls .close() at the very end.
        We only flush to be safe but leave the buffer alive
        so the rest of the code can still read from it.
        """
        if not self.closed:       # protect against double-close
            self.flush()          # make sure everything is written
            # **do not** call super().close() – that would mark it closed

class UlogExporter:
    """
    Class for exporting data from ROS bags and ULog files into a combined format.
    """
    def __init__(self, 
        rosbag_path: Optional[Union[str, bytes]] = None,
        ulog_path: Optional[Union[str, bytes]] = None,
        output_dir="output", 
        filename="combined_data.bag",
        single_instance=False,
        leaf_fc_ros_prefix="dynamo_db"
    ):
        """
        Initialize UlogExporter with paths to ROS bag and ULog files.
        
        Args:
            rosbag_path: Path to the ROS bag file
            ulog_path: Path to the ULog file
        """
        self.ulog_signals : Dict[str, UlogSignal | ULogGPSPositionSignal] = {}
        self.ros_signals : Dict[str, RosSignal] = {}
        self.rosbag_path = rosbag_path
        self.ulog_path = ulog_path
        self.single_instance = single_instance
        self.leaf_fc_ros_prefix = leaf_fc_ros_prefix

        # Open bag for writing
        self.output_dir = output_dir
        self.output_bag_path = os.path.join(output_dir, filename)

        self.synchronizers: Dict[str, Union[SignalSynchronizer, SignalSynchronizerMulti, SignalSynchronizerSingle]] = {
            # "position" : SignalSynchronizerSingle(bag_path=rosbag_path, ulg_path=ulog_path),
            # "velocity" : SignalSynchronizerSingle(bag_path=rosbag_path, ulg_path=ulog_path),
            "acceleration" : SignalSynchronizerSingle(bag_path=rosbag_path, ulg_path=ulog_path),
            "acceleration_raw" : SignalSynchronizerMulti(bag_path=rosbag_path, ulg_path=ulog_path),
        }

        self.ulog_signals : Dict[str, Dict[str,UlogCartesianSignal|str|Dict[str,str]]] = {
            "position" : {
                "signal" : None, 
                "msg_type" : "vector3", 
                "field_mapping" : {"f_x": "x", "f_y": "y", "f_z": "z"},
                "path" : "vehicle_local_position/position",
                "depends": ["t_vehicle_local_position_0",]
            },
            "velocity" : {
                "signal" : None, 
                "msg_type" : "vector3", 
                "field_mapping" : {"f_vx": "x", "f_vy": "y", "f_vz": "z"},
                "path" : "vehicle_local_position/velocity",
                "depends": ["t_vehicle_local_position_0",]
            },
            "acceleration" : {
                "signal" : None, 
                "msg_type" : "vector3", 
                "field_mapping" : {"f_ax": "x", "f_ay": "y", "f_az": "z"},
                "path" : "vehicle_local_position/acceleration",
                "depends": ["t_vehicle_local_position_0",]
            }
        }

        self.ulog_derived_signals : Dict[str, Dict[str,UlogCartesianSignal|str|Dict[str,str]]] = {
            "orientation" : {
                "signal" : None, 
                "msg_type" : "vector3", 
                "field_mapping" : {"roll": "x", "pitch": "y", "yaw": "z"}, 
                "path" : "vehicle_local_position/orientation",
                "depends": ["t_vehicle_attitude_0",]
            },
            "orientation_rate" : {
                "signal" : None, 
                "msg_type" : "vector3", 
                "field_mapping" : {"f_xyz_0_": "x", "f_xyz_1_": "y", "f_xyz_2_": "z"},
                "path" : "vehicle_local_position/orientation_rate",
                "depends": ["t_vehicle_angular_velocity_0",]
            },
            "distance_estimate" : {
                "signal" : None, 
                "msg_type" : "float32", 
                "field_mapping" : {"f_dist_bottom": "data"},
                "path" : "vehicle_local_position/distance_estimate",
                "depends": ["t_vehicle_local_position_0",]
            },
            "motor_cmds" : {
                "signal" : None, 
                "msg_type" : "float32_multi_array", 
                "field_mapping" : {"f_control_0_": 0, "f_control_1_": 1, "f_control_2_": 2, "f_control_3_": 3},
                "path" : "motor_cmds",
                "depends": ["t_actuator_motors_0",]
            },
            "sensor_mag": {
                "signal": None,
                "msg_type": "vector3",
                "field_mapping": {"f_x": "x", "f_y": "y", "f_z": "z"},
                "path": "sensor_mag/raw",
                "depends": ["t_sensor_mag_0",]
            },
            "heading_mag": {
                "signal": None,
                "msg_type": "float32",
                "field_mapping": {"f_heading": "data"},
                "path": "sensor_mag/heading",
                "depends": ["t_sensor_mag_0", "t_vehicle_attitude_0",]
            }
        }

        if not self.single_instance:
            self.ulog_derived_signals.update({
                "estimator_status" : {
                    "signal" : None, 
                    "msg_type" : "float32", 
                    "field_mapping" : {"f_primary_instance": "data"},
                    "path" : "estimator_selector_status/primary_instance",
                    "depends": ["t_estimator_selector_status_0",]
                },
                "n_estimator_instances" : {
                    "signal" : None, 
                    "msg_type" : "float32", 
                    "field_mapping" : {"f_instances_available": "data"},
                    "path" : "estimator_selector_status/num_available_instances",
                    "depends": ["t_estimator_selector_status_0",]
                },
            })

        self.ulog_derived_signals_multi : Dict[str, Dict[str,List[UlogRawAccelerationSignal|str|Dict[str,str]]]] = {
            "acceleration_raw" : {
                "signal": [],
                "msg_type": "vector3",
                "field_mapping" : {"f_x": "x", "f_y": "y", "f_z": "z"},
                "path" : "sensor_accel/acceleration_raw",
                "num_instances": 0,
                "base_topic_name": "t_sensor_accel_"
            }
        }

        self.ros_signals : Dict[str, Dict[str,CartesianSignal|str|Dict[str,str]]] = {
            "position" : {
                "signal" : None, 
                "msg_type" : "vector3", 
                "field_mapping" : {"x": "x", "y": "y", "z": "z"},
                "path" : "position",
                "depends": [f"/{self.leaf_fc_ros_prefix}/estimator/pos",]
            },
            "velocity" : {
                "signal" : None, 
                "msg_type" : "vector3", 
                "field_mapping" : {"x": "x", "y": "y", "z": "z"},
                "path" : "velocity",
                "depends": [f"/{self.leaf_fc_ros_prefix}/estimator/vel",]
            },
            "acceleration" : {
                "signal" : None, 
                "msg_type" : "vector3", 
                "field_mapping" : {"x": "x", "y": "y", "z": "z"},
                "path" : "acceleration",
                "depends": [f"/{self.leaf_fc_ros_prefix}/estimator/acc",]
            },
            "orientation" : {
                "signal" : None, 
                "msg_type" : "vector3", 
                "field_mapping" : {"roll": "x", "pitch": "y", "yaw": "z"},
                "path" : "orientation",
                "depends": [f"/{self.leaf_fc_ros_prefix}/estimator/ori",]
            },
            "orientation_rate" : {
                "signal" : None, 
                "msg_type" : "vector3", 
                "field_mapping" : {"roll": "x", "pitch": "y", "yaw": "z"},
                "path" : "orientation_rate",
                "depends": [f"/{self.leaf_fc_ros_prefix}/estimator/ori_rate",]
            },
        }

        self.num_estimator_instances = 0

        self.custom_synchronizers = {
            "acceleration_raw" : {
                "ros_signal" : {
                    "key": "acceleration",
                    "type": "single"
                },
                "ulog_signal" : {
                    "key": "acceleration_raw",
                    "type": "multi",
                }
            }
        }


    def detect_sensors(self):
        """
        Detect sensors from the ULog file and populate multi-instance derived signals.
        """
        # Count instances of multi-instance topics in ULog file
        with load_ulg(self.ulog_path) as ulog:
            ulog_keys = list(ulog.keys())
            
            # Process each multi-instance signal type
            for signal_key, signal_config in self.ulog_derived_signals_multi.items():
                base_topic = signal_config.get("base_topic_name").rstrip("0123456789")
            
                # Find all instances by counting matching topics
                num_instances = 0
                for key in ulog_keys:
                    if key.startswith(base_topic) and key[len(base_topic):].isdigit():
                        instance_number = int(key[len(base_topic):])
                        num_instances = max(num_instances, instance_number + 1)

                # Update the instance count in the configuration
                self.ulog_derived_signals_multi[signal_key]["num_instances"] = num_instances
                logger.info(f"Found {num_instances} instances of {base_topic}")        

    def verify_log_files(self):
        """
        Verify that the ULog and ROS bag files contain the expected topics.
        
        Returns:
            bool: True if verification is successful, False otherwise
        Raises:
            FileNotFoundError: If the ULog or ROS bag file does not exist or cannot be opened.
            TypeError: If the ULog or ROS bag file is not a valid file or does not contain the expected topics.
            ImportError: If the necessary modules for loading files are not available.
            OSError: If there is an error while reading the files.
            Exception: If there is an unexpected error while verifying the files.
        """
        try:
            # Count instances of multi-instance topics in ULog file
            for signal_key, signal_config in self.ulog_derived_signals_multi.items():
                if "num_instances" not in signal_config:
                    logger.error(f"Multi-instance signal {signal_key} does not have 'num_instances' defined.")
                    return False
                
                if signal_config["num_instances"] == 0:
                    logger.error(f"Multi-instance signal {signal_key} has zero instances defined.")
                    return False
                
            with load_ulg(self.ulog_path) as ulog:
                # get dependancies for ulog_signals and ulog_derived_signals
                required_topics = set()
                for signal_dict in [self.ulog_signals, self.ulog_derived_signals]:
                    for signal_key, signal_config in signal_dict.items():
                        depends = signal_config.get("depends", [])
                        required_topics.update(depends)

                ulog_keys = list(ulog.keys())
                for topic in required_topics:
                    if topic not in ulog_keys:
                        logger.error(f"Required topic {topic} not found in ULog file.")
                        return False
                    
            # verify ros topics
            if self.rosbag_path is not None:
                with load_rosbag(self.rosbag_path) as rosbag:
                    # get dependancies for ros_signals
                    required_ros_topics = set()
                    for signal_key, signal_config in self.ros_signals.items():
                        depends = signal_config.get("depends", [])
                        required_ros_topics.update(depends)

                    for topic in required_ros_topics:
                        if topic not in rosbag.topics:
                            logger.error(f"Required ROS topic {topic} not found in ROS bag.")
                            return False

            return True
        except FileNotFoundError as e:
            logger.error(f"ULog file not found: {e}")
            raise e
        except TypeError as e:
            logger.error(f"Invalid ULog file: {e}")
            raise e
        except ImportError as e:
            logger.error(f"Required module for loading ULog files is not available: {e}")
            raise e
        except OSError as e:
            logger.error(f"Error reading ULog file: {e}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error while verifying ULog file: {e}")
            raise e

    def extract_all_data(self):
        """
        Extract all available data from both sources
        Returns:
            None
        Raises:
            AssertionError: If the number of estimator instances in the ULog file does not match the expected number.
            Exception: If the ULog file does not contain the expected topics for position, velocity, or acceleration data.
            RuntimeError: If the ULog file cannot be loaded or does not contain the expected topics.
            FileNotFoundError: If the ULog file does not exist or cannot be opened.
            TypeError: If the ULog file is not a valid ULog file or does not contain the expected topics.
            ImportError: If the necessary modules for loading ULog files or ROS bags are not available.
            OSError: If there is an error while reading the ULog file or ROS bag.
            Exception: If there is an unexpected error while extracting data from the ULog file or ROS bag.
        """

        with load_ulg(self.ulog_path) as ulog:
            self.ulog_signals["position"]["signal"] = UlogPositionSignal(ulog, "t_vehicle_local_position_0")
            self.ulog_signals["velocity"]["signal"] = UlogVelocitySignal(ulog, "t_vehicle_local_position_0")
            self.ulog_signals["acceleration"]["signal"] = UlogAccelerationSignal(ulog, "t_vehicle_local_position_0")

        if self.rosbag_path is not None:
            with load_rosbag(self.rosbag_path) as rosbag:
                self.ros_signals["position"]["signal"] = CartesianSignal(rosbag, f"/{self.leaf_fc_ros_prefix}/estimator/pos")
                self.ros_signals["velocity"]["signal"] = CartesianSignal(rosbag, f"/{self.leaf_fc_ros_prefix}/estimator/vel")
                self.ros_signals["acceleration"]["signal"] = CartesianSignal(rosbag, f"/{self.leaf_fc_ros_prefix}/estimator/acc")
                self.ros_signals["orientation"]["signal"] = OrientationSignal(rosbag, f"/{self.leaf_fc_ros_prefix}/estimator/ori")
                self.ros_signals["orientation_rate"]["signal"] = OrientationSignal(rosbag, f"/{self.leaf_fc_ros_prefix}/estimator/ori_rate")

        with load_ulg(self.ulog_path) as ulog:
            self.ulog_derived_signals["orientation"]["signal"] = UlogOrientationSignal(ulog, "t_vehicle_attitude_0")
            self.ulog_derived_signals["orientation_rate"]["signal"] = UlogAngularSignal(ulog, "t_vehicle_angular_velocity_0")
            self.ulog_derived_signals["motor_cmds"]["signal"] = UlogMotorCommandSignal(ulog, "t_actuator_motors_0")
            self.ulog_derived_signals["distance_estimate"]["signal"] = UlogSignal(ulog, "t_vehicle_local_position_0", ["f_dist_bottom",])
            self.ulog_derived_signals["sensor_mag"]["signal"] = UlogSignal(ulog, "t_sensor_mag_0", ["f_x", "f_y", "f_z"], dimension=3)
            self.ulog_derived_signals["heading_mag"]["signal"] = UlogHeading(ulog, "t_sensor_mag_0", "t_vehicle_attitude_0")

            if not self.single_instance:
                self.ulog_derived_signals["estimator_status"]["signal"] = UlogSignal(ulog, "t_estimator_selector_status_0", ["f_primary_instance",])
                self.ulog_derived_signals["n_estimator_instances"]["signal"] = UlogSignal(ulog, "t_estimator_selector_status_0", ["f_instances_available",])

                # get number of estimator instances from n_estimator_instances
                self.num_estimator_instances = self.ulog_derived_signals["n_estimator_instances"]["signal"].get_signal_slice(0)[0]
            else:
                self.num_estimator_instances = 1

            n_signals = 0
            num_instances = self.ulog_derived_signals_multi["acceleration_raw"].get("num_instances", 0)
            base_topic_name = self.ulog_derived_signals_multi["acceleration_raw"].get("base_topic_name", "t_sensor_accel_")
            for i in range(num_instances):
                self.ulog_derived_signals_multi["acceleration_raw"]["signal"].append(
                    UlogRawAccelerationSignal(ulog, f"{base_topic_name}{i}")
                )
                n_signals += 1
            self.ulog_derived_signals_multi["acceleration_raw"]["num_instances"] = n_signals

    def _compute_correlations_custom(self, plot_correlation):
        """
        Compute correlations between ROS and ULog signals.
        
        Args:
            plot_correlation: Whether to plot the correlation results
            
        Returns:
            None
        Raises:
            AssertionError: If the number of estimator instances in the ULog file does not match the expected number.
            Exception: If the ULog file does not contain the expected topics for position, velocity, or acceleration data.
            RuntimeError: If the ULog file cannot be loaded or does not contain the expected topics.
            FileNotFoundError: If the ULog file does not exist or cannot be opened.
            TypeError: If the ULog file is not a valid ULog file or does not contain the expected topics.
            ImportError: If the necessary modules for loading ULog files or ROS bags are not available.
            OSError: If there is an error while reading the ULog file or ROS bag.
            Exception: If there is an unexpected error while computing correlations.
        """

        # compute best offset
        for key, sync_settings in self.custom_synchronizers.items():

            if key not in self.synchronizers:
                continue

            ros_signal = self.ros_signals[sync_settings["ros_signal"]["key"]]
            if sync_settings["ulog_signal"]["type"] == "single":
                ulog_signal = self.ulog_signals[sync_settings["ulog_signal"]["key"]]
            elif sync_settings["ulog_signal"]["type"] == "multi":
                ulog_signal = self.ulog_derived_signals_multi[sync_settings["ulog_signal"]["key"]]

            if ros_signal["signal"] is None or ulog_signal["signal"] is None:
                continue
            
            if sync_settings["ulog_signal"]["type"] == "single":
                sync_settings = {
                    "ros_signal_class" : ros_signal["signal"].__class__,
                    "ulog_signal_class" : ulog_signal["signal"].__class__,
                    "ros_topic_name" : ros_signal["signal"].topic,
                    "ulog_msg_key" : ulog_signal["signal"].msg_key,
                    "ros_signal_idx" : None,
                    "ulog_signal_idx" : None
                }
            elif sync_settings["ulog_signal"]["type"] == "multi":
                sync_settings = {
                    "ros_signal_class" : ros_signal["signal"].__class__,
                    "ulog_signal_class" : ulog_signal["signal"][0].__class__,
                    "ros_topic_name" : ros_signal["signal"].topic,
                    "ulog_msg_keys" : [ulog_signal["signal"][i].msg_key for i in range(ulog_signal["num_instances"])],
                    "ros_signal_idx" : None,
                    "ulog_signal_idx" : None
                }

            self.synchronizers[key].compute_best_offset(**sync_settings)

            if plot_correlation:
                self.synchronizers[key].plot_correlation(os.path.join(self.output_dir, f"{key}_correlation.png"))
                self.synchronizers[key].plot_signals(os.path.join(self.output_dir, f"{key}_signals.png"))

    def _compute_correlations(self, plot_correlation):
        """
        Compute correlations between ROS and ULog signals.
        
        Args:
            plot_correlation: Whether to plot the correlation results
            
        Returns:
            None
        Raises:
            AssertionError: If the number of estimator instances in the ULog file does not match the expected number.
            Exception: If the ULog file does not contain the expected topics for position, velocity, or acceleration data.
            RuntimeError: If the ULog file cannot be loaded or does not contain the expected topics.
            FileNotFoundError: If the ULog file does not exist or cannot be opened.
            TypeError: If the ULog file is not a valid ULog file or does not contain the expected topics.
            ImportError: If the necessary modules for loading ULog files or ROS bags are not available.
            OSError: If there is an error while reading the ULog file or ROS bag.
            Exception: If there is an unexpected error while computing correlations.
        """

        # compute best offset
        for key, ulog_signal in self.ulog_signals.items():
            
            if key not in self.synchronizers:
                continue

            ros_signal = self.ros_signals[key]

            if ros_signal["signal"] is None or ulog_signal["signal"] is None:
                continue

            sync_settings = {
                "ros_signal_class" : ros_signal["signal"].__class__,
                "ulog_signal_class" : ulog_signal["signal"].__class__,
                "ros_topic_name" : ros_signal["signal"].topic,
                "ulog_msg_key" : ulog_signal["signal"].msg_key,
                "ros_signal_idx" : None,
                "ulog_signal_idx" : None
            }
            
            self.synchronizers[key].compute_best_offset(**sync_settings)
            if plot_correlation:
                self.synchronizers[key].plot_correlation(os.path.join(self.output_dir, f"{key}_correlation.png"))
                self.synchronizers[key].plot_signals(os.path.join(self.output_dir, f"{key}_signals.png"))

    def _syncronize_signals(self, sync_key:str):

        assert sync_key in self.synchronizers, f"Sync key {sync_key} not found in synchronizers"

        if self.synchronizers[sync_key].best_offset is not None:
            # check shorter signal type
            if self.synchronizers[sync_key].shorter_type == "Ulog":

                if -self.synchronizers[sync_key].best_offset > 0:

                    ulog_start_time = 0.0
                    ros_start_time = self.synchronizers[sync_key].best_offset

                elif -self.synchronizers[sync_key].best_offset < 0:

                    ulog_start_time = -self.synchronizers[sync_key].best_offset
                    ros_start_time = 0.0

                else:
                    
                    ulog_start_time = 0.0
                    ros_start_time = 0.0

            elif self.synchronizers[sync_key].shorter_type == "ROS":

                if -self.synchronizers[sync_key].best_offset > 0:

                    ulog_start_time = self.synchronizers[sync_key].best_offset
                    ros_start_time = 0.0

                elif -self.synchronizers[sync_key].best_offset < 0:

                    ulog_start_time = 0.0
                    ros_start_time = -self.synchronizers[sync_key].best_offset

                else:
                    
                    ulog_start_time = 0.0
                    ros_start_time = 0.0

            for key, ulog_signal in list(self.ulog_signals.items()) + list(self.ulog_derived_signals.items()):
                if ulog_signal["signal"] is not None:
                    ulog_signal["signal"].set_start_time(ulog_start_time)
            for key, ros_signal in self.ros_signals.items():
                if ros_signal["signal"] is not None:
                    ros_signal["signal"].set_start_time(ros_start_time)
            for ulog_signal_key, ulog_signal_config in self.ulog_derived_signals_multi.items():
                for i in range(ulog_signal_config["num_instances"]):
                    self.ulog_derived_signals_multi[ulog_signal_key]["signal"][i].set_start_time(ulog_start_time)

    def export_df(self, output_dir, write_csv=True) -> Tuple[Dict[str, pd.DataFrame], Dict[str, SignalConfigDict]]:
        """
        Export all signals to CSV files
        Args:
            output_dir: Directory to save the CSV files
            write_csv: Whether to write the DataFrame to CSV files
        Returns:
            df_dict: Dictionary containing DataFrames for each signal
            signal_config_dict: Dictionary of signal configuration dictionaries
        Raises:
            OSError: If there is an error creating the output directory or writing the CSV files
            Exception: If there is an error exporting the DataFrame to CSV files
        """
        os.makedirs(output_dir, exist_ok=True)
        
        df_dict = {}
        signal_config_dict: Dict[str, SignalConfigDict] = {}

        for signal_name, signal_dict in dict(self.ulog_signals, **self.ulog_derived_signals).items():
            signal_object = signal_dict["signal"]
            if signal_object is not None:
                df = pd.DataFrame({
                    "timestamp": signal_object.timestamps,
                    **{key: signal_object.get_signal_slice(i) for i, key in enumerate(signal_object.data_keys)}
                })

                if write_csv:
                    csv_path = os.path.join(output_dir, f"px4_{signal_name}.csv")
                    df.to_csv(csv_path, index=False)
                    logger.info(f"Exported {signal_name} to {csv_path}")
                df_dict["px4_" + signal_name] = df

            unique_signal_key = "px4_" + signal_name
            signal_config = SignalConfigDict(
                signal_key=signal_name,
                signal_df_key="px4_" + signal_name,
                signal_source="ulog",
                is_multi=False
            )
            signal_config_dict[unique_signal_key] = signal_config

        for signal_name, signal_dict in self.ulog_derived_signals_multi.items():
            any_signals_none = any(signal_dict["signal"][i] is None for i in range(signal_dict["num_instances"]))
            if any_signals_none:
                continue
            for i in range(signal_dict["num_instances"]):
                signal_object = signal_dict["signal"][i]
                if signal_object is not None:
                    df = pd.DataFrame({
                        "timestamp": signal_object.timestamps,
                        **{key: signal_object.get_signal_slice(i) for i, key in enumerate(signal_object.data_keys)}
                    })
                    if write_csv:
                        csv_path = os.path.join(output_dir, f"px4_{signal_name}_{i}.csv")
                        df.to_csv(csv_path, index=False)
                        logger.info(f"Exported {signal_name}_{i} to {csv_path}")
                    df_dict[f"px4_{signal_name}_{i}"] = df

            unique_signal_key = "px4_" + signal_name
            signal_config = SignalConfigDict(
                signal_key=signal_name,
                signal_df_keys=[f"px4_{signal_name}_{i}" for i in range(signal_dict["num_instances"])],
                signal_source="ulog",
                is_multi=True,
                n_channels=signal_dict["num_instances"]
            )
            signal_config_dict[unique_signal_key] = signal_config

        for signal_name, signal_dict in self.ros_signals.items():
            signal_object = signal_dict["signal"]
            if signal_object is not None:
                df = pd.DataFrame({
                    "timestamp": signal_object.timestamps,
                    **{key: signal_object.get_signal_slice(i) for i, key in enumerate(signal_object.data_keys)}
                })

                if write_csv:
                    csv_path = os.path.join(output_dir, f"ros_{signal_name}.csv")
                    df.to_csv(csv_path, index=False)
                    logger.info(f"Exported {signal_name} to {csv_path}")
                df_dict["ros_" + signal_name] = df

                unique_signal_key = "ros_" + signal_name
                signal_config = SignalConfigDict(
                    signal_key=signal_name,
                    signal_df_key="ros_" + signal_name,
                    signal_source="ros",
                    is_multi=False
                )
                signal_config_dict[unique_signal_key] = signal_config
        signal_list_dump = {}
        for key, signal in signal_config_dict.items():
            signal_list_dump[key] = signal.model_dump()

        return df_dict, signal_list_dump
    
    def create_combined_ulog(self, output_dir=None, write_csv=True, write_bag=True) -> Tuple[bytes, Dict[str, pd.DataFrame], Dict[str, SignalConfigDict]]:
        """
        Create a combined dataset in ULog format
        Note: This is a basic implementation that exports to CSV files 
        with ULog-compatible naming conventions
        Args:
            output_dir: Directory to save the output files
            write_csv: Whether to write the DataFrame to CSV files
            write_bag: Whether to write the combined data to a ROS bag file
        Returns:
            bag_bytes: Bytes of the combined ROS bag
            dfs: Dictionary of DataFrames for each signal
            signal_list_dump: List of signal configuration dictionaries
        Raises:
            OSError: If there is an error creating the output directory or writing the CSV files
            Exception: If there is an error exporting the DataFrame to CSV files or writing the bag
        """
        if output_dir is not None:
            os.makedirs(output_dir, exist_ok=True)
        
        # Create a metadata file with combined information
        metadata = {
            "version": "1.0",
            "description": "Combined ROS and ULog data",
            "timestamp": pd.Timestamp.now().isoformat()
        }
        
        if output_dir is not None:
            with open(os.path.join(output_dir, "metadata.json"), "w") as f:
                json.dump(metadata, f, indent=2)
        
        # create an IO buffer for the output bag
        bag_stream = BagBuffer()

        rospy.loginfo("Creating bag: %s", self.output_bag_path)
        with rosbag.Bag(bag_stream, "w") as bag:
                
            # Export all signals
            dfs, signal_dict_dump = self.export_df(output_dir, write_csv=write_csv)

            # Add all CSV files to the output bag
            for signal_name, signal_dict in dict(self.ulog_signals, **self.ulog_derived_signals).items():
                if signal_dict["signal"] is None:
                    continue
                df = dfs["px4_" + signal_name]
                add_df_to_bag(
                    bag, df, 
                    f"/px4/{signal_dict['path']}", 
                    msg_type_str=signal_dict["msg_type"], 
                    field_mapping=signal_dict["field_mapping"]
                )
                lookup_signal_name = "px4_" + signal_name
                signal_dict_dump[lookup_signal_name]["topic"] = f"/px4/{signal_dict['path']}"
                signal_dict_dump[lookup_signal_name]["msg_type"] = signal_dict["msg_type"]
                signal_dict_dump[lookup_signal_name]["field_mapping"] = signal_dict["field_mapping"]

            for signal_name, signal_dict in self.ulog_derived_signals_multi.items():
                if signal_dict["signal"] is None:
                    continue
                for i in range(signal_dict["num_instances"]):
                    df = dfs[f"px4_{signal_name}_{i}"]
                    add_df_to_bag(
                        bag, df, 
                        f"/px4/{signal_dict['path']}/{i}", 
                        msg_type_str=signal_dict["msg_type"], 
                        field_mapping=signal_dict["field_mapping"]
                    )

                unique_signal_key = "px4_" + signal_name
                signal_dict_dump[unique_signal_key]["topics"] = [f"/px4/{signal_dict['path']}/{i}" for i in range(signal_dict["num_instances"])]
                signal_dict_dump[unique_signal_key]["msg_type"] = signal_dict["msg_type"]
                signal_dict_dump[unique_signal_key]["field_mapping"] = signal_dict["field_mapping"]
            for signal_name, signal_dict in self.ros_signals.items():
                if signal_dict["signal"] is None:
                    continue
                df = dfs["ros_" + signal_name]
                add_df_to_bag(
                    bag, df, 
                    f"/ros/{signal_dict['path']}", 
                    msg_type_str=signal_dict["msg_type"], 
                    field_mapping=signal_dict["field_mapping"]
                )

                unique_signal_key = "ros_" + signal_name
                signal_dict_dump[unique_signal_key]["topic"] = f"/ros/{signal_dict['path']}"
                signal_dict_dump[unique_signal_key]["msg_type"] = signal_dict["msg_type"]
                signal_dict_dump[unique_signal_key]["field_mapping"] = signal_dict["field_mapping"]

        validated_signal_configs = {}

        for signal_name, signal_dict in signal_dict_dump.items():
            try:
                signal_config = SignalConfigDict(**signal_dict)
                validated_signal_configs[signal_name] = signal_config.model_dump()
            except ValidationError as e:
                logger.error(f"Validation error for signal {signal_name}: {e}")

        bag_stream.seek(0)
        bag_bytes = bag_stream.getvalue()

        # Write the bag to the output directory
        if write_bag:
            with open(self.output_bag_path, 'wb') as f:
                f.write(bag_bytes)
            logger.info(f"Combined bag written to {self.output_bag_path}")
            
        return bag_bytes, dfs, validated_signal_configs

    def create_charts(self, output_dir: str = "charts"):
        """
        Create charts for all signals
        """
        chart_dir = os.path.join(self.output_dir, output_dir)
        os.makedirs(chart_dir, exist_ok=True)
        
        for signal_name, signal_dict in dict(self.ulog_signals, **self.ulog_derived_signals).items():
            signal_object = signal_dict["signal"]
            if signal_object is not None:
                fig, ax = signal_object.plot()
                fig.suptitle(signal_name)
                fig.savefig(os.path.join(chart_dir, f"{signal_name}.png"))
                fig.clf()
                plt.close(fig)
                logger.info(f"Created chart for {signal_name}")

        for signal_name, signal_dict in self.ulog_derived_signals_multi.items():
            if signal_dict["num_instances"] == 0:
                continue
            n_dims = len(signal_dict["field_mapping"])
            fig, ax = plt.subplots(n_dims, 1, figsize=(10, 2 * n_dims))
            colors = ['blue', 'red', 'green', 'purple', 'orange', 'brown', 'pink', 'gray', 'olive', 'cyan']
            for i in range(signal_dict["num_instances"]):
                color_idx = i % len(colors)  # Cycle through colors if more dimensions than colors
                signal_object = signal_dict["signal"][i]
                for j in range(n_dims):
                    signal_object.plot(ax=ax[j], idx=j, color=colors[color_idx], label=f"{signal_name}_{j}_i.{i}")
                
            fig.savefig(os.path.join(chart_dir, f"{signal_name}.png"))
            fig.clf()
            plt.close(fig)
            logger.info(f"Created chart for {signal_name}")

        for signal_name, signal_dict in self.ros_signals.items():
            signal_object = signal_dict["signal"]
            if signal_object is not None:
                fig, ax = signal_object.plot()
                fig.suptitle(signal_name)
                fig.savefig(os.path.join(chart_dir, f"{signal_name}.png"))
                fig.clf()
                plt.close(fig)
                logger.info(f"Created chart for {signal_name}")

class UlogExporterOutdoor(UlogExporter):
    """
    Class for exporting data from ROS bags and ULog files into a combined format.
    """
    def __init__(self, 
        rosbag_path=None, 
        ulog_path=None, 
        output_dir="output", 
        filename="combined_data.bag",
        single_instance=False,
        sensor_config=None,
        leaf_fc_ros_prefix="dynamo_db"

    ):
        
        super().__init__(rosbag_path, ulog_path, output_dir, filename, single_instance, leaf_fc_ros_prefix)

        self.sensor_config = sensor_config.copy() if sensor_config is not None else {}

        if self.sensor_config.get("gps", False):
            self.ulog_derived_signals.update({
                "gps" : {
                    "signal" : None, 
                    "msg_type" : "vector3", 
                    "field_mapping" : {"f_lat": "x", "f_lon": "y", "f_alt": "z"},
                    "path" : "vehicle_global_position/gps",
                    "depends": ["t_vehicle_global_position_0",]
                },
                "gps_vel" : {
                    "signal" : None, 
                    "msg_type" : "vector3", 
                    "field_mapping" : {"f_vel_e_m_s": "x", "f_vel_n_m_s": "y", "f_vel_d_m_s": "z"},
                    "path" : "sensor_gps/gps_vel",
                    "depends": ["t_sensor_gps_0",]
                },
                "gps_fix" : {
                    "signal" : None, 
                    "msg_type" : "float32", 
                    "field_mapping" : {"f_fix_type": "data"},
                    "path" : "sensor_gps/gps_fix",
                    "depends": ["t_vehicle_gps_position_0",]
                },
                "gps_heading": {
                    "signal": None,
                    "msg_type": "float32",
                    "field_mapping": {"f_heading": "data"},
                    "path": "sensor_gps/heading",
                    "depends": ["t_sensor_gps_0",]
                },
                "gps_heading_accuracy": {
                    "signal": None,
                    "msg_type": "float32",
                    "field_mapping": {"f_heading_accuracy": "data"},
                    "path": "sensor_gps/heading_accuracy",
                    "depends": ["t_sensor_gps_0",]
                },
                "gps_satellites_used": {
                    "signal": None,
                    "msg_type": "float32",
                    "field_mapping": {"f_satellites_used": "data"},
                    "path": "sensor_gps/satellites_used",
                    "depends": ["t_sensor_gps_0",]
                },
                "gps_alt": {
                    "signal": None,
                    "msg_type": "float32",
                    "field_mapping": {"f_alt": "data"},
                    "path": "sensor_gps/alt",
                    "depends": ["t_sensor_gps_0",]
                },
                "gps_hdop": {
                    "signal": None,
                    "msg_type": "float32",
                    "field_mapping": {"f_hdop": "data"},
                    "path": "sensor_gps/hdop",
                    "depends": ["t_sensor_gps_0",]
                },
                "gps_vdop": {
                    "signal": None,
                    "msg_type": "float32",
                    "field_mapping": {"f_vdop": "data"},
                    "path": "sensor_gps/vdop",
                    "depends": ["t_sensor_gps_0",]
                },
                "gps_eph": {
                    "signal": None,
                    "msg_type": "float32",
                    "field_mapping": {"f_eph": "data"},
                    "path": "sensor_gps/eph",
                    "depends": ["t_sensor_gps_0",]
                },
                "gps_epv": {
                    "signal": None,
                    "msg_type": "float32",
                    "field_mapping": {"f_epv": "data"},
                    "path": "sensor_gps/epv",
                    "depends": ["t_sensor_gps_0",]
                },
                "gps_vpos": {
                    "signal": None,
                    "msg_type": "float32",
                    "field_mapping": {"f_gps_vpos": "data"},
                    "path": "estimator_status/innovation_test_ratios/vpos",
                    "depends": ["t_estimator_innovation_test_ratios_0",]
                },
                "gps_vvel": {
                    "signal": None,
                    "msg_type": "float32",
                    "field_mapping": {"f_gps_vvel": "data"},
                    "path": "estimator_status/innovation_test_ratios/vvel",
                    "depends": ["t_estimator_innovation_test_ratios_0",]
                },
            })

        if self.sensor_config.get("distance_sensor", False):
            self.ulog_derived_signals.update({
                "distance_sensor" : {
                    "signal" : None, 
                    "msg_type" : "float32", 
                    "field_mapping" : {"f_current_distance": "data"},
                    "path" : "sensor_distance/current_distance",
                    "depends": ["t_distance_sensor_0",]
                },
            })

        if self.sensor_config.get("optical_flow", False):
            self.ulog_derived_signals.update({
                "of_flow" : {
                    "signal": None, 
                    "msg_type": "vector3", 
                    "field_mapping": {"f_vx": "x", "f_vy": "y", "f_vz": "z"},
                    "path" : "leaf_signals/of_flow",
                    "depends": [
                        "t_sensor_optical_flow_0",
                        "t_vehicle_local_position_0",
                        "t_vehicle_attitude_0",
                        "t_distance_sensor_0"
                    ]
                }
            })
            self.ulog_derived_signals_multi.update({
                "of_flow_estimator" : {
                    "signal": [],
                    "msg_type": "float32_multi_array",
                    "field_mapping" : {"f_vel_ne_0_": 0, "f_vel_ne_1_": 1},
                    "path" : "estimator_signals/of_flow_estimator",
                    "num_instances": 0,
                    "base_topic_name": "t_estimator_optical_flow_vel_"
                },
            })

        self.ulog_derived_signals_multi.update({
            "vehicle_magnetometer": {
                "signal": [],
                "msg_type": "vector3",
                "field_mapping": {
                    "f_magnetometer_ga_0_": "x",
                    "f_magnetometer_ga_1_": "y",
                    "f_magnetometer_ga_2_": "z"
                },
                "path": "vehicle_magnetometer",
                "num_instances": 0,
                "base_topic_name": "t_vehicle_magnetometer_"
            },
            "innovation_test_ratios_hpos" : {
                "signal": [],
                "msg_type": "float32_multi_array",
                "field_mapping" : {
                    "f_gps_hpos_0_": 0, 
                    "f_gps_hpos_1_": 1
                },
                "path" : "estimator_status/innovation_test_ratios/hpos",
                "num_instances": 0,
                "base_topic_name": "t_estimator_innovation_test_ratios_"
            },
            "innovation_test_ratios_hvel" : {
                "signal": [],
                "msg_type": "float32_multi_array",
                "field_mapping" : {
                    "f_gps_hvel_0_": 0, 
                    "f_gps_hvel_1_": 1
                },
                "path" : "estimator_status/innovation_test_ratios/hvel",
                "num_instances": 0,
                "base_topic_name": "t_estimator_innovation_test_ratios_"
            },
            "innovation_test_ratios_flow" : {
                "signal": [],
                "msg_type": "float32_multi_array",
                "field_mapping" : {
                    "f_flow_0_": 0, 
                    "f_flow_1_": 1
                },
                "path" : "estimator_status/innovation_test_ratios/flow",
                "num_instances": 0,
                "base_topic_name": "t_estimator_innovation_test_ratios_"
            },
            "sensor_gyro": {
                "signal": [],
                "msg_type": "vector3",
                "field_mapping": {
                    "f_x": "x",
                    "f_y": "y",
                    "f_z": "z"
                },
                "path": "sensor_gyro/angular_velocity",
                "num_instances": 0,
                "base_topic_name": "t_sensor_gyro_"
            },
            "sensor_gyro_integrated": {
                "signal": [],
                "msg_type": "vector3",
                "field_mapping": {
                    "angle_x": "x",
                    "angle_y": "y",
                    "angle_z": "z"
                },
                "path": "sensor_gyro/angular_position",
                "num_instances": 0,
                "base_topic_name": "t_sensor_gyro_"
            }
        })

    def extract_all_data(self, sync_key:str, plot_correlation:bool = False):
        """
        Extract all available data from both sources
        This method overrides the base class method to include GPS and optical flow data extraction.
        It also initializes derived signals for GPS, optical flow, and innovation test ratios.
        It assumes that the ULog file contains the necessary topics for GPS and optical flow data.
        It also checks the sensor configuration to determine which signals to extract.
        Args:
            plot_correlation: Whether to plot correlation charts for the signals
            sync_key: The key for the synchronizer to use for signal synchronization
        Returns:
            None
        Raises:
            AssertionError: If the number of estimator instances in the ULog file does not match the expected number.
            Exception: If the ULog file does not contain the expected topics for GPS or optical flow data.
            KeyError: If the sensor configuration does not contain the expected keys for GPS or optical flow.
            ValueError: If the ULog file does not contain the expected topics for GPS or optical flow data.
            RuntimeError: If the ULog file cannot be loaded or does not contain the expected topics.
            FileNotFoundError: If the ULog file does not exist or cannot be opened.
            TypeError: If the sensor configuration is not a dictionary or does not contain the expected keys.
            ImportError: If the necessary modules for loading ULog files or ROS bags are not available.
            OSError: If there is an error while reading the ULog file or ROS bag.
            Exception: If there is an unexpected error while extracting data from the ULog file or ROS bag.
        """

        super().extract_all_data() # <- calculates and sets num_instances for each ulog_derived_signals_multi

        with load_ulg(self.ulog_path) as ulog:
            if self.sensor_config.get("gps", False):
                self.ulog_derived_signals["gps"]["signal"] = ULogGPSPositionSignal(ulog, "t_vehicle_global_position_0")
                self.ulog_derived_signals["gps_vel"]["signal"] = UlogGPSVelocitySignal(ulog, "t_sensor_gps_0")
                self.ulog_derived_signals["gps_fix"]["signal"] = UlogSignal(ulog, "t_vehicle_gps_position_0", ["f_fix_type",])
                self.ulog_derived_signals["gps_heading"]["signal"] = UlogSignal(ulog, "t_sensor_gps_0", ["f_heading",])
                self.ulog_derived_signals["gps_heading_accuracy"]["signal"] = UlogSignal(ulog, "t_sensor_gps_0", ["f_heading_accuracy",])
                self.ulog_derived_signals["gps_satellites_used"]["signal"] = UlogSignal(ulog, "t_sensor_gps_0", ["f_satellites_used",])
                self.ulog_derived_signals["gps_alt"]["signal"] = UlogSignal(ulog, "t_sensor_gps_0", ["f_alt",])
                self.ulog_derived_signals["gps_hdop"]["signal"] = UlogSignal(ulog, "t_sensor_gps_0", ["f_hdop",])
                self.ulog_derived_signals["gps_vdop"]["signal"] = UlogSignal(ulog, "t_sensor_gps_0", ["f_vdop",])
                self.ulog_derived_signals["gps_eph"]["signal"] = UlogSignal(ulog, "t_sensor_gps_0", ["f_eph",])
                self.ulog_derived_signals["gps_epv"]["signal"] = UlogSignal(ulog, "t_sensor_gps_0", ["f_epv",])
                self.ulog_derived_signals["gps_vpos"]["signal"] = UlogSignal(ulog, "t_estimator_innovation_test_ratios_0", ["f_gps_vpos"])
                self.ulog_derived_signals["gps_vvel"]["signal"] = UlogSignal(ulog, "t_estimator_innovation_test_ratios_0", ["f_gps_vvel"])

            if self.sensor_config.get("optical_flow", False):
                self.ulog_derived_signals["of_flow"]["signal"] = UlogOFVelocity(
                    ulog, "t_sensor_optical_flow_0", "t_vehicle_local_position_0", "t_vehicle_attitude_0", "t_distance_sensor_0"
                )

            if self.sensor_config.get("distance_sensor", False):
                try:
                    self.ulog_derived_signals["distance_sensor"]["signal"] = UlogSignal(ulog, "t_distance_sensor_0", ["f_current_distance",])
                except KeyError:
                    logger.warning("Warning: t_distance_sensor_0 not found in ULog file.")

            n_signals = 0
            if self.sensor_config.get("optical_flow", False):
                num_instances = self.ulog_derived_signals_multi["of_flow_estimator"].get("num_instances", 0)
                base_topic_name = self.ulog_derived_signals_multi["of_flow_estimator"].get("base_topic_name", "t_estimator_optical_flow_vel_")
                for i in range(num_instances):
                    self.ulog_derived_signals_multi["of_flow_estimator"]["signal"].append(
                        UlogEstimatorOFVelocity(ulog, f"{base_topic_name}{i}")
                    )
                    n_signals += 1
                self.ulog_derived_signals_multi["of_flow_estimator"]["num_instances"] = n_signals

            n_signals = 0
            num_instances = self.ulog_derived_signals_multi["vehicle_magnetometer"].get("num_instances", 0)
            base_topic_name = self.ulog_derived_signals_multi["vehicle_magnetometer"].get("base_topic_name", "t_vehicle_magnetometer_")
            data_keys = list(self.ulog_derived_signals_multi["vehicle_magnetometer"]["field_mapping"].keys())
            dimension = len(data_keys)
            for i in range(num_instances):
                self.ulog_derived_signals_multi["vehicle_magnetometer"]["signal"].append(
                    UlogSignal(
                        ulog,
                        f"{base_topic_name}{i}",
                        data_keys=data_keys,
                        dimension=dimension
                    )
                )
                n_signals += 1
            self.ulog_derived_signals_multi["vehicle_magnetometer"]["num_instances"] = n_signals

            n_signals = 0
            num_instances = self.ulog_derived_signals_multi["innovation_test_ratios_hpos"].get("num_instances", 0)
            base_topic_name = self.ulog_derived_signals_multi["innovation_test_ratios_hpos"].get("base_topic_name", "t_estimator_innovation_test_ratios_")
            data_keys = list(self.ulog_derived_signals_multi["innovation_test_ratios_hpos"]["field_mapping"].keys())
            dimension = len(data_keys)
            for i in range(num_instances):
                self.ulog_derived_signals_multi["innovation_test_ratios_hpos"]["signal"].append(
                    UlogSignal(
                        ulog, 
                        f"{base_topic_name}{i}", 
                        data_keys=data_keys,
                        dimension=dimension
                    )
                )
                n_signals += 1
            self.ulog_derived_signals_multi["innovation_test_ratios_hpos"]["num_instances"] = n_signals

            n_signals = 0
            num_instances = self.ulog_derived_signals_multi["innovation_test_ratios_hvel"].get("num_instances", 0)
            base_topic_name = self.ulog_derived_signals_multi["innovation_test_ratios_hvel"].get("base_topic_name", "t_estimator_innovation_test_ratios_")
            data_keys = list(self.ulog_derived_signals_multi["innovation_test_ratios_hvel"]["field_mapping"].keys())
            dimension = len(data_keys)
            for i in range(num_instances):
                self.ulog_derived_signals_multi["innovation_test_ratios_hvel"]["signal"].append(
                    UlogSignal(ulog, f"{base_topic_name}{i}", data_keys=data_keys, dimension=dimension)
                )
                n_signals += 1
            self.ulog_derived_signals_multi["innovation_test_ratios_hvel"]["num_instances"] = n_signals

            n_signals = 0
            num_instances = self.ulog_derived_signals_multi["innovation_test_ratios_flow"].get("num_instances", 0)
            base_topic_name = self.ulog_derived_signals_multi["innovation_test_ratios_flow"].get("base_topic_name", "t_estimator_innovation_test_ratios_")
            data_keys = list(self.ulog_derived_signals_multi["innovation_test_ratios_flow"]["field_mapping"].keys())
            dimension = len(data_keys)
            for i in range(num_instances):
                self.ulog_derived_signals_multi["innovation_test_ratios_flow"]["signal"].append(
                    UlogSignal(ulog, f"{base_topic_name}{i}", data_keys=data_keys, dimension=dimension)
                )
                n_signals += 1
            self.ulog_derived_signals_multi["innovation_test_ratios_flow"]["num_instances"] = n_signals

            n_signals = 0
            num_instances = self.ulog_derived_signals_multi["sensor_gyro"].get("num_instances", 0)
            base_topic_name = self.ulog_derived_signals_multi["sensor_gyro"].get("base_topic_name", "t_sensor_gyro_")
            data_keys = list(self.ulog_derived_signals_multi["sensor_gyro"]["field_mapping"].keys())
            dimension = len(data_keys)
            for i in range(num_instances):
                self.ulog_derived_signals_multi["sensor_gyro"]["signal"].append(
                    UlogSignal(
                        ulog,
                        f"{base_topic_name}{i}",
                        data_keys=data_keys,
                        dimension=dimension
                    )
                )
                n_signals += 1
            self.ulog_derived_signals_multi["sensor_gyro"]["num_instances"] = n_signals

            n_signals = 0
            num_instances = self.ulog_derived_signals_multi["sensor_gyro_integrated"].get("num_instances", 0)
            base_topic_name = self.ulog_derived_signals_multi["sensor_gyro_integrated"].get("base_topic_name", "t_sensor_gyro_")
            for i in range(num_instances):
                self.ulog_derived_signals_multi["sensor_gyro_integrated"]["signal"].append(
                    UlogGyroHeading(ulog, f"{base_topic_name}{i}", "t_vehicle_attitude_0")
                )
                n_signals += 1
            self.ulog_derived_signals_multi["sensor_gyro_integrated"]["num_instances"] = n_signals

        # apply GPS calibration based on initial x,y,z position 
        if self.sensor_config.get("gps", False):
            if self.ulog_derived_signals["gps"]["signal"] is not None:
                self.ulog_derived_signals["gps"]["signal"].apply_calibration_offset(
                    calibration_offset=self.ulog_signals["position"]["signal"].get_initial_coords()
                )

        self._compute_correlations(plot_correlation)
        self._compute_correlations_custom(plot_correlation)
        self._syncronize_signals(sync_key=sync_key)

class UlogExporterIndoor(UlogExporter):
    """
    Class for exporting data from ROS bags and ULog files into a combined format.
    """
    def __init__(self, 
        rosbag_path=None, 
        ulog_path=None, 
        output_dir="output", 
        filename="combined_data.bag",
        single_instance=False,
        leaf_fc_ros_prefix="dynamo_db"
    ):
        
        super().__init__(rosbag_path, ulog_path, output_dir, filename, single_instance, leaf_fc_ros_prefix)

    def extract_all_data(self, sync_key:str, plot_correlation:bool=False):
        """
        Extract all available data from both sources
        This method overrides the base class method to include indoor-specific signal extraction.
        It assumes that the ULog file contains the necessary topics for indoor navigation data.
        Args:
            plot_correlation: Whether to plot correlation charts for the signals
            sync_key: Key for the synchronizer to use for signal synchronization
        Returns:
            None
        Raises:
            AssertionError: If the number of estimator instances in the ULog file does not match the expected number.
            Exception: If the ULog file does not contain the expected topics for indoor navigation data.
            KeyError: If the sensor configuration does not contain the expected keys for indoor navigation data.
            ValueError: If the ULog file does not contain the expected topics for indoor navigation data.
            RuntimeError: If the ULog file cannot be loaded or does not contain the expected topics.
            FileNotFoundError: If the ULog file does not exist or cannot be opened.
            TypeError: If the sensor configuration is not a dictionary or does not contain the expected keys.
            ImportError: If the necessary modules for loading ULog files or ROS bags are not available.
            OSError: If there is an error while reading the ULog file or ROS bag.
            Exception: If there is an unexpected error while extracting data from the ULog file or ROS bag.
        """
        super().extract_all_data()

        self._compute_correlations(plot_correlation)
        self._compute_correlations_custom(plot_correlation)
        self._syncronize_signals(sync_key=sync_key)