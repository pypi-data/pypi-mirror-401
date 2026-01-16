"""
特征表操作相关工具方法
"""
import re
import json
from typing import Union, List, Dict, Optional, Any

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.streaming import StreamingQuery
from pyspark.sql.types import StructType
import os
from wedata.common.constants.constants import (
    APPEND, DEFAULT_WRITE_STREAM_TRIGGER,
    FEATURE_ENGINEERING_TABLE_PRIMARY_KEY_WEDATA,
    FEATURE_TABLE_BACKUP_PRIMARY_KEY,
    FEATURE_TABLE_TIMESTAMP,
    FEATURE_DLC_TABLE_PRIMARY_KEY,
)
from wedata.common.log import get_logger
from wedata.common.entities.feature_table import FeatureTable
from wedata.common.constants.engine_types import EngineTypes
from wedata.common.spark_client import SparkClient
from wedata.common.utils import common_utils, env_utils
# from wedata.common.feast_client.feast_client import FeastClient  # 已注释：不使用 Feast
from wedata.common.base_table_client import AbstractBaseTableClient
from wedata.common.cloud_sdk_client.client import FeatureServiceClient
from wedata.common.cloud_sdk_client.models import (
    ListComputeResourcesRequest,
    ListConnectionsRequest,
    DeleteOnlineTableRequest,
    CreateOnlineTableRequest,
    SchedulerConfiguration,
    OfflineFeatureTableConfiguration,
    OfflineFeatureTable,
)
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException  # pyright: ignore[reportMissingTypeStubs]


class FeatureEngineeringTableClient(AbstractBaseTableClient):
    """特征表操作类"""
    def __init__(
            self,
            spark: SparkSession,
            cloud_secret_id: Optional[str] = None,
            cloud_secret_key: Optional[str] = None,
            cloud_secret_token: Optional[str] = None,
    ):
        self._spark = spark
        # self._feast_client = FeastClient(spark)  # 已注释：不使用 Feast
        self._feast_client = None  # 禁用 Feast 客户端
        if cloud_secret_id and cloud_secret_key:
            self.__cloud_secret_id = cloud_secret_id
            self.__cloud_secret_key = cloud_secret_key
            self.__cloud_secret_token = cloud_secret_token
        else:
            self.__cloud_secret_id, self.__cloud_secret_key, self.__cloud_secret_token = env_utils.get_temporary_secret()
        self.__project = env_utils.get_project_id()
        self.__region = env_utils.get_region()
        self.__logger = get_logger()
        self._feature_service_client = FeatureServiceClient(
            self.__cloud_secret_id,
            self.__cloud_secret_key,
            self.__cloud_secret_token,
            self.__region
        )

    @property
    def cloud_secret_id(self) -> str:
        if not self.__cloud_secret_id:
            raise ValueError("cloud_secret_id is empty. please set it first.")
        return self.__cloud_secret_id

    @cloud_secret_id.setter
    def cloud_secret_id(self, cloud_secret_id: str):
        if not cloud_secret_id:
            raise ValueError("cloud_secret_id cannot be None")
        self.__cloud_secret_id = cloud_secret_id

    @property
    def cloud_secret_key(self) -> str:
        if not self.__cloud_secret_key:
            raise ValueError("cloud_secret_key is empty. please set it first.")
        return self.__cloud_secret_key

    @cloud_secret_key.setter
    def cloud_secret_key(self, cloud_secret_key: str):
        if not cloud_secret_key:
            raise ValueError("cloud_secret_key cannot be None")
        self.__cloud_secret_key = cloud_secret_key

    @property
    def cloud_secret_token(self) -> str:
        return self.__cloud_secret_token

    @cloud_secret_token.setter
    def cloud_secret_token(self, cloud_secret_token: str):
        self.__cloud_secret_token = cloud_secret_token

    @property
    def project(self) -> str:
        return self.__project

    @property
    def region(self) -> str:
        return self.__region

    def create_table(
            self,
            name: str,
            primary_keys: Union[str, List[str]],
            timestamp_key: str,
            engine_type: EngineTypes,
            database_name: Optional[str] = None,
            catalog_name: Optional[str] = None,
            df: Optional[DataFrame] = None,
            *,
            partition_columns: Union[str, List[str], None] = None,
            schema: Optional[StructType] = None,
            description: Optional[str] = None,
            tags: Optional[Dict[str, str]] = None
    ) -> FeatureTable:

        """
        创建特征表（支持批流数据写入）

        Args:
            name: 特征表全称（格式：<table>）
            primary_keys: 主键列名（支持复合主键）
            database_name: Optional[str] = None,
            catalog_name: catalog名称（可选）。如果不提供，将使用当前Spark会话的catalog
            df: 初始数据（可选，用于推断schema）
            timestamp_key: 时间戳键（用于时态特征）
            partition_columns: 分区列（优化存储查询）
            schema: 表结构定义（可选，当不提供df时必需）
            description: 业务描述
            tags: 业务标签
        Returns:
            FeatureTable实例

        Raises:
            ValueError: 当schema与数据不匹配时
        """

        # 参数标准化
        primary_keys = self._normalize_params(primary_keys)
        partition_columns = self._normalize_params(partition_columns)

        assert self._check_sequence_element_type(primary_keys, str), "primary_keys must be a list of strings"
        assert self._check_sequence_element_type(partition_columns, str), "partition_columns must be a list of strings"
        assert timestamp_key is None or isinstance(timestamp_key, str), \
            "timestamp_key must be None or a string"

        # 元数据校验
        self._validate_schema(df, schema)

        # 只在 timestamp_key 非空时才校验时间戳列的存在性和冲突
        if timestamp_key:
            self._validate_key_exists(primary_keys, timestamp_key)
            self._validate_key_conflicts(primary_keys, timestamp_key)

        # 表名校验
        common_utils.validate_table_name(name)

        common_utils.validate_database(database_name)

        # 校验PrimaryKey是否有重复
        dup_list = common_utils.get_duplicates(primary_keys)
        if dup_list:
            raise ValueError(f"Primary keys have duplicates: {dup_list}")

        # 构建完整表名（支持catalog）
        spark_client = SparkClient(self._spark)
        table_name = common_utils.build_full_table_name(
            name, database_name, catalog_name=catalog_name, spark_client=spark_client
        )

        # 检查表是否存在
        try:
            if self._check_table_exists(table_name):
                raise ValueError(
                    f"Table '{name}' already exists\n"
                    "Solutions:\n"
                    "1. Use a different table name\n"
                    "2. Drop the existing table: spark.sql(f'DROP TABLE {name}')\n"
                )
        except Exception as e:
            raise ValueError(f"Error checking table existence: {str(e)}") from e

        # 推断表schema
        table_schema = schema or df.schema

        # 构建时间戳键属性

        # 从环境变量获取额外标签
        env_tags = {
            "project_id": os.getenv("WEDATA_PROJECT_ID", ""),  # wedata项目ID
            "engine_name": os.getenv("WEDATA_NOTEBOOK_ENGINE", ""),  # wedata引擎名称
            "user_uin": os.getenv("KERNEL_LOGIN_UIN", "")  # wedata用户UIN
        }
        projectId = os.getenv("WEDATA_PROJECT_ID", "")
        # 构建表属性（通过TBLPROPERTIES）
        tbl_properties = {
            FEATURE_ENGINEERING_TABLE_PRIMARY_KEY_WEDATA: ",".join(primary_keys),
            FEATURE_TABLE_BACKUP_PRIMARY_KEY: ",".join(primary_keys),  # 兼容旧版本读取
            "wedata.feature_project_id": f"{json.dumps([projectId])}",
            "comment": description or "",
            **{f"{k}": v for k, v in (tags or {}).items()},
            **{f"feature_{k}": v for k, v in (env_tags or {}).items()}
        }

        # 只在 timestamp_key 非空时才添加到 TBLPROPERTIES
        if timestamp_key:
            tbl_properties[FEATURE_TABLE_TIMESTAMP] = timestamp_key
        if engine_type == EngineTypes.ICEBERG_ENGINE:
            if partition_columns:
                tbl_properties.update({
                    'format-version': '2',
                    'write.upsert.enabled': 'true',
                    'write.update.mode': 'merge-on-read',
                    'write.merge.mode': 'merge-on-read',
                    'write.parquet.bloom-filter-enabled.column.id': 'true',
                    'dlc.ao.data.govern.sorted.keys': ",".join(primary_keys),
                    # 'write.distribution-mode': 'hash',
                    'write.metadata.delete-after-commit.enabled': 'true',
                    'write.metadata.previous-versions-max': '100',
                    'write.metadata.metrics.default': 'full',
                    'smart-optimizer.inherit': 'default',
                })
            else:
                tbl_properties.update({
                    'format-version': '2',
                    'write.upsert.enabled': 'true',
                    'write.update.mode': 'merge-on-read',
                    'write.merge.mode': 'merge-on-read',
                    'write.parquet.bloom-filter-enabled.column.id': 'true',
                    'dlc.ao.data.govern.sorted.keys': ",".join(primary_keys),
                    # 'write.distribution-mode': 'hash',
                    'write.metadata.delete-after-commit.enabled': 'true',
                    'write.metadata.previous-versions-max': '100',
                    'write.metadata.metrics.default': 'full',
                    'smart-optimizer.inherit': 'default',
                })

        # 构建列定义
        columns_ddl = []
        for field in table_schema.fields:
            data_type = field.dataType.simpleString().upper()
            col_def = f"`{field.name}` {data_type}"
            if not field.nullable:
                col_def += " NOT NULL"
            # 添加字段注释(如果metadata中有comment)
            if field.metadata and "comment" in field.metadata:
                comment = self._escape_sql_value(field.metadata["comment"])
                col_def += f" COMMENT '{comment}'"
            columns_ddl.append(col_def)

        # 构建分区表达式
        partition_expr = (
            f"PARTITIONED BY ({', '.join([f'`{c}`' for c in partition_columns])})"
            if partition_columns else ""
        )
        # 本地调试 iceberg --》PARQUET
        # 核心建表语句
        if engine_type == EngineTypes.ICEBERG_ENGINE:
            ddl = f"""
        CREATE TABLE {table_name} (
            {', '.join(columns_ddl)}
        )
        USING iceberg
        {partition_expr}
        TBLPROPERTIES (
            {', '.join(f"'{k}'='{self._escape_sql_value(v)}'" for k, v in tbl_properties.items())}
        )
            """
        elif engine_type == EngineTypes.HIVE_ENGINE:
            ddl = f"""
            CREATE TABLE {table_name} (
        {', '.join(columns_ddl)}
    )
    {partition_expr}
    TBLPROPERTIES (
        {', '.join(f"'{k}'='{self._escape_sql_value(v)}'" for k, v in tbl_properties.items())}
    )
            """
        else:
            raise ValueError(f"Engine type {engine_type} is not supported")

        # 打印sql
        self.__logger.info(f"create table ddl: {ddl}\n")

        # 执行DDL
        try:
            self._spark.sql(ddl)
            if df is not None:
                df.write.insertInto(table_name)
        except Exception as e:
            raise ValueError(f"Failed to create table: {str(e)}") from e

        # 已注释：不使用 Feast 注册表
        # self._feast_client.create_table(
        #     table_name=table_name,
        #     primary_keys=primary_keys,
        #     timestamp_key=timestamp_key,
        #     df=df,
        #     schema=table_schema,
        #     tags=tags,
        #     description=description
        # )

        # 构建并返回FeatureTable对象
        return FeatureTable(
            name=name,
            table_id=table_name,
            description=description or "",
            primary_keys=primary_keys,
            partition_columns=partition_columns or [],
            features=[field.name for field in table_schema.fields],
            timestamp_keys=timestamp_key or [],
            tags=dict(**tags or {}, **env_tags)
        )

    def write_table(
            self,
            name: str,
            df: DataFrame,
            database_name: Optional[str] = None,
            catalog_name: Optional[str] = None,
            mode: Optional[str] = APPEND,
            checkpoint_location: Optional[str] = None,
            trigger: Optional[Dict[str, Any]] = DEFAULT_WRITE_STREAM_TRIGGER
    ) -> Optional[StreamingQuery]:

        """
        写入特征表数据（支持批处理和流式写入）

        Args:
            name: 特征表名称（格式：<table>）
            df: 要写入的数据（DataFrame）
            database_name: 数据库名
            catalog_name: catalog名称（可选）。如果不提供，将使用当前Spark会话的catalog
            mode: 写入模式（append/overwrite）
            checkpoint_location: 流式写入的检查点位置（仅流式写入需要）
            trigger: 流式写入触发条件（仅流式写入需要）

        Returns:
            如果是流式写入返回StreamingQuery对象，否则返回None

        Raises:
            ValueError: 当参数不合法时抛出
        """

        # 验证写入模式
        valid_modes = ["append", "overwrite"]
        if mode not in valid_modes:
            raise ValueError(f"Invalid write mode '{mode}', valid options: {valid_modes}")

        # 表名校验
        common_utils.validate_table_name(name)

        common_utils.validate_database(database_name)

        # 构建完整表名（支持catalog）
        spark_client = SparkClient(self._spark)
        table_name = common_utils.build_full_table_name(
            name, database_name, catalog_name=catalog_name, spark_client=spark_client
        )

        # 检查表是否存在
        if not self._check_table_exists(table_name):
            raise ValueError(f"table '{name}' not exists")

        # 判断是否是流式DataFrame
        is_streaming = df.isStreaming

        try:
            if is_streaming:
                # 流式写入
                if not checkpoint_location:
                    raise ValueError("Streaming write requires checkpoint_location parameter")

                writer = df.writeStream \
                    .format("parquet") \
                    .outputMode(mode) \
                    .option("checkpointLocation", checkpoint_location) \
                    # .foreachBatch(process_batch)

                if trigger:
                    writer = writer.trigger(**trigger)

                return writer.toTable(table_name)
            else:
                # 批处理写入
                df.write \
                    .mode(mode) \
                    .insertInto(table_name)
                # self._feast_client.client.write_to_offline_store(feature_view_name=table_name, df=df.toPandas(), allow_registry_cache=False,)
                return None

        except Exception:
            raise
            # raise ValueError(f"Failed to write to table '{table_name}': {str(e)}") from e

    def read_table(
            self,
            name: str,
            database_name: Optional[str] = None,
            catalog_name: Optional[str] = None,
    ) -> DataFrame:

        """
        从特征表中读取数据
        Args:
            name: 特征表名称（格式：<table>）
            database_name: 特征库名称
            catalog_name: catalog名称（可选）。如果不提供，将使用当前Spark会话的catalog
        Returns:
            包含表数据的DataFrame

        Raises:
            ValueError: 当表不存在或读取失败时抛出
        """

        # 表名校验
        common_utils.validate_table_name(name)

        common_utils.validate_database(database_name)

        # 构建完整表名（支持catalog）
        spark_client = SparkClient(self._spark)
        table_name = common_utils.build_full_table_name(
            name, database_name, catalog_name=catalog_name, spark_client=spark_client
        )

        try:
            # 检查表是否存在
            if not self._check_table_exists(table_name):
                raise ValueError(f"Table '{name}' does not exist. full_table_name:{table_name}")

            # 读取表数据
            return self._spark.read.table(table_name)

        except Exception as e:
            raise

    def drop_table(self, name: str, database_name: Optional[str] = None, catalog_name: Optional[str] = None) -> None:

        """
        删除特征表（表不存在时抛出异常）

        Args:
            name: 特征表名称（格式：<table>）
            database_name: 特征库名称
            catalog_name: catalog名称（可选）。如果不提供，将使用当前Spark会话的catalog
        Raises:
            ValueError: 当表不存在时抛出
            RuntimeError: 当删除操作失败时抛出

        示例:
            # 基本删除
            drop_table("user_features")
        """

        # 表名校验
        common_utils.validate_table_name(name)

        # 构建完整表名（支持catalog）
        spark_client = SparkClient(self._spark)
        table_name = common_utils.build_full_table_name(
            name, database_name, catalog_name=catalog_name, spark_client=spark_client
        )
        try:
            # 检查表是否存在
            if not self._check_table_exists(table_name):
                self.__logger.error(f"Table '{name}' does not exist")
                return

            # 已注释：不使用 Feast 检查在线表
            # try:
            #     feature_view = self._feast_client.get_feature_view(table_name)
            # except Exception:
            #     pass
            #     # self.__logger.warning(f"Table '{name}' is not a feature table, skip delete. {str(e)}")
            # else:
            #     if feature_view.online:
            #         raise ValueError(f"Table '{name}' has a online table, please call drop_online_table first")

            # 执行删除
            self._spark.sql(f"DROP TABLE {table_name}")
            self.__logger.info(f"Table '{name}' dropped")

            # 已注释：不使用 Feast 删除
            # try:
            #     self._feast_client.remove_offline_table(table_name=table_name)
            # except Exception:
            #     raise
            # else:
            #     self.__logger.info(f"Table '{name}' removed from feast")
        except ValueError:
            raise  # 直接抛出已知的ValueError
        except Exception as e:
            raise RuntimeError(f"Failed to delete table '{name}': {str(e)}") from e

    def get_table(
            self,
            name: str,
            spark_client: SparkClient,
            database_name: Optional[str] = None,
            catalog_name: Optional[str] = None,
    ) -> FeatureTable:

        """
        获取特征表元数据信息

        参数:
            name: 特征表名称
            spark_client: Spark客户端
            database_name: 数据库名称
            catalog_name: catalog名称（可选）。如果不提供，将使用当前Spark会话的catalog

        返回:
            FeatureTable对象

        异常:
            ValueError: 当表不存在或获取失败时抛出
        """

        # 表名校验
        common_utils.validate_table_name(name)
        common_utils.validate_database(database_name)

        # 构建完整表名（支持catalog）
        table_name = common_utils.build_full_table_name(
            name, database_name, catalog_name=catalog_name, spark_client=spark_client
        )
        if not self._check_table_exists(full_table_name=table_name):
            raise ValueError(f"Table '{name}' does not exist")
        try:
            return spark_client.get_feature_table(table_name)
        except Exception as e:
            raise
            # raise ValueError(f"Failed to get metadata for table '{name}': {str(e)}") from e

    def alter_table_tag(
            self,
            name: str,
            properties: Dict[str, str],
            database_name: Optional[str] = None,
            catalog_name: Optional[str] = None,
            mode: str = "add"
    ):
        """
        修改表的TBLPROPERTIES属性（有则修改，无则新增）

        Args:
            name: 表名（格式：<table>）
            properties: 要修改/新增的属性字典
            database_name: 特征库名称
            catalog_name: catalog名称（可选）。如果不提供，将使用当前Spark会话的catalog
            mode: 模式  add / delete

        Raises:
            ValueError: 当表不存在或参数无效时抛出
            RuntimeError: 当修改操作失败时抛出

        示例:
            # 修改表属性
            client.alter_tables_tag("user_features", {
                "comment": "更新后的描述",
                "owner": "data_team"
            })
        """
        # 参数校验
        if not properties:
            raise ValueError("properties must be a non-empty dictionary")

        # 表名校验
        common_utils.validate_table_name(name)
        common_utils.validate_database(database_name)

        # 构建完整表名（支持catalog）
        spark_client = SparkClient(self._spark)
        table_name = common_utils.build_full_table_name(
            name, database_name, catalog_name=catalog_name, spark_client=spark_client
        )

        try:
            # 检查表是否存在
            if not self._check_table_exists(table_name):
                raise ValueError(f"table '{name}' not exists")

            if mode == "add":
                # Spark SQL 保留的表属性（不能手动设置）
                RESERVED_TABLE_PROPERTIES = {'owner', 'last_modified_time', 'last_modified_by', 'created_time', 'created_by'}

                # 过滤掉保留属性
                filtered_properties = {k: v for k, v in properties.items() if k.lower() not in RESERVED_TABLE_PROPERTIES}

                if not filtered_properties:
                    raise ValueError(f"All properties are reserved and cannot be set: {list(properties.keys())}")

                # 构建属性设置语句
                props_str = ", ".join(
                    f"'{k}'='{self._escape_sql_value(v)}'"
                    for k, v in filtered_properties.items()
                )

                alter_sql = f"ALTER TABLE {table_name} SET TBLPROPERTIES ({props_str})"
            elif mode == "delete":
                props_str = ", ".join(f"'{k}'" for k in properties.keys())
                alter_sql = f"ALTER TABLE {table_name} UNSET TBLPROPERTIES ({props_str})"
            else:
                raise ValueError(f"Invalid mode '{mode}', valid options: {['add', 'delete']}")

            # 执行修改
            self._spark.sql(alter_sql)

            # 已注释：不使用 Feast 同步标签
            # # 执行结果回写feast
            # tbl_pro = self._spark.sql(f"SHOW TBLPROPERTIES {table_name}").collect()
            # props = {row['key']: row['value'] for row in tbl_pro}
            # self._feast_client.modify_tags(table_name=table_name, tags=props)

            print(f"Successfully updated properties for table '{name}': {list(properties.keys())}")

        except ValueError as e:
            raise  # 直接抛出已知的ValueError
        except Exception as e:
            raise RuntimeError(f"Failed to modify properties for table '{name}': {str(e)}") from e

    def _check_table_exists(self, full_table_name: str) -> bool:
        return common_utils.check_spark_table_exists(self._spark, full_table_name)

    def _get_table_primary_keys_and_timestamp_key(self, full_table_name: str) -> tuple[list[str], str]:

        tbl_pro = self._spark.sql(f"SHOW TBLPROPERTIES {full_table_name}")  # pyright: ignore[reportUnknownMemberType]
        props = {row['key']: row['value'] for row in tbl_pro.collect()}

        if props.get(FEATURE_DLC_TABLE_PRIMARY_KEY, ""):
            primary_keys = props.get(FEATURE_DLC_TABLE_PRIMARY_KEY, "")
        else:
            primary_keys = props.get(FEATURE_TABLE_BACKUP_PRIMARY_KEY, "")
        primary_keys = primary_keys.split(",")
        timestamp_key = props.get(FEATURE_TABLE_TIMESTAMP, "")
        return primary_keys, timestamp_key

    def _isvalid_crontab_expression(self, crontab_expression: str) -> bool:
        """仅判断字符串是否符合crontab表达式格式,不判断字段取值的合法性"""

        # 用于匹配和解析标准5字段crontab表达式
        itemr_ex = re.compile(r'^([^@#\s]+)\s+([^@#\s]+)\s+([^@#\s]+)\s+([^@#\s]+)\s+([^@#\s]+)$')
        # 精准匹配以 @ 开头的crontab快捷指令
        specr_ex = re.compile(r'^@(\w+)$')

        if specr_ex.match(crontab_expression) or itemr_ex.match(crontab_expression):
            return True

        return False

    def publish_table(self, source_catalog_name: str, source_schema_name: str, source_table_name: str,
                      online_catalog_name: str, online_schema_name: str, online_table_name: str,
                      is_cycle: bool = False, trigger: Optional[SchedulerConfiguration] = None,
                      ):
        """
        将离线特征表发布为在线特征表
        Args:
            catalog_name: 数据目录名称
            schema_name: 数据库名称
            table_name: 表名称
            is_cycle: 是否周期性发布, 默认False
            trigger: 周期性任务的调度配置, 仅在is_cycle为True时生效
        Raises:
            ValueError: 当参数无效时抛出
            RuntimeError: 当发布操作失败时抛出
        """
        # 构建完整表名
        full_table_name = common_utils.build_full_table_name(source_table_name, source_schema_name, source_catalog_name, self._spark)

        # 检查表是否存在
        if not self._check_table_exists(full_table_name):
            raise ValueError(f"Table '{full_table_name}' does not exist")

        # 获取计算资源列表
        list_compute_resources_request = ListComputeResourcesRequest()
        list_compute_resources_request.WorkspaceId = self.project
        list_compute_resources_request.ResourceTypes = [2]  # 获取数据计算型资源组
        list_compute_resources_request.ResourceStatuses = [3]  # 获取运行中的资源组
        try:
            list_compute_resources_response = self._feature_service_client.ListComputeResources(list_compute_resources_request)
        except TencentCloudSDKException as e:
            raise RuntimeError(f"Failed to list compute resources: {e.get_message()}, request_id: {e.get_request_id()}")
        if len(list_compute_resources_response.Data.Resources) == 0:
            raise RuntimeError(f"Failed to list compute resources: no compute resources found")
        if not list_compute_resources_response.Data.Resources[0].BasicInfo:
            raise RuntimeError(f"Unable to get compute resource basic info")
        resource_group_id = list_compute_resources_response.Data.Resources[0].BasicInfo.ResourceId

        # 获取连接信息
        list_conn_request = ListConnectionsRequest()
        list_conn_request.WorkspaceId = self.project
        list_conn_request.ConnectionType = ["postgresql"]  # TODO: 参数值需要根据实际情况调整
        list_conn_request.Status = ["2"]  # 测试连通成功的连接
        try:
            list_conn_response = self._feature_service_client.ListConnections(list_conn_request)
        except TencentCloudSDKException as e:
            raise RuntimeError(f"Failed to list connections: {e.get_message()}, request_id: {e.get_request_id()}")
        if len(list_conn_response.Data.Items) == 0:
            raise RuntimeError(f"Failed to list connections: no connections found")

        primary_keys, timestamp_key = self._get_table_primary_keys_and_timestamp_key(full_table_name)

        offline_table_info = OfflineFeatureTable()
        offline_table_info.CatalogName = source_catalog_name
        offline_table_info.SchemaName = source_schema_name
        offline_table_info.TableName = source_table_name
        offline_feature_configuration = OfflineFeatureTableConfiguration()
        offline_feature_configuration.PrimaryKeys = primary_keys
        offline_feature_configuration.TimestampColumn = timestamp_key
        offline_feature_configuration.TableNameInfo = offline_table_info

        target_path = OfflineFeatureTable()
        target_path.CatalogName = online_catalog_name
        target_path.SchemaName = online_schema_name
        target_path.TableName = online_table_name

        request = CreateOnlineTableRequest()
        request.WorkspaceId = self.project
        request.ResourceGroupId = resource_group_id
        request.ConnectionId = list_conn_response.Data.Items[0].ConnectionId
        request.OfflineFeatureConfiguration = offline_feature_configuration
        request.TargetPath = target_path
        if is_cycle:
            if not isinstance(trigger, SchedulerConfiguration):
                raise ValueError(f"trigger must be a TaskSchedulerConfiguration object, got {type(trigger)}")
            if not trigger.Trigger:
                raise ValueError(f"trigger.Trigger must be a WorkflowTriggerConfig object, got {type(trigger.Trigger)}")
            if not self._isvalid_crontab_expression(trigger.Trigger.CrontabExpression):
                raise ValueError(f"Trigger.CrontabExpression is not a valid crontab expression, got "
                                 "{trigger.Trigger.CrontabExpression}")
            if trigger.Trigger.TriggerMode not in ["TIME_TRIGGER", "FILE_REACH", "CONTINUE_RUN"]:
                raise ValueError(f"Trigger.TriggerMode must be one of ['TIME_TRIGGER', 'FILE_REACH', 'CONTINUE_RUN'], "
                                 "got {trigger.Trigger.TriggerMode}")
            if trigger.Trigger.ConfigMode not in ["COMMON", "CRON_EXPRESSION"]:
                raise ValueError(f"Trigger.ConfigMode must be one of ['COMMON', 'CRON_EXPRESSION'], got {trigger.Trigger.ConfigMode}")
            if trigger.Trigger.CycleType not in ["ONEOFF_CYCLE", "HOUR_CYCLE", "DAY_CYCLE", "WEEK_CYCLE",
                                                 "MONTH_CYCLE", "YEAR_CYCLE", "MINUTE_CYCLE", "CRONTAB_CYCLE"]:
                raise ValueError(f"Trigger.CycleType must be one of ['ONEOFF_CYCLE', 'HOUR_CYCLE', 'DAY_CYCLE', 'WEEK_CYCLE', "
                                 "'MONTH_CYCLE', 'YEAR_CYCLE', 'MINUTE_CYCLE', 'CRONTAB_CYCLE'], got {trigger.Trigger.CycleType}")
            if trigger.AdvanceConfig:
                if trigger.AdvanceConfig.QueuingMode not in ["ON", "OFF"]:
                    raise ValueError(f"AdvanceConfig.QueuingMode must be one of ['ON', 'OFF'], got {trigger.AdvanceConfig.QueuingMode}")
                if trigger.AdvanceConfig.MaxConcurrentNum < 1:
                    raise ValueError(f"AdvanceConfig.MaxConcurrentNum must be greater than 0, got {trigger.AdvanceConfig.MaxConcurrentNum}")
            request.TaskSchedulerConfiguration = trigger
        try:
            resp = self._feature_service_client.CreateOnlineTable(request)
        except TencentCloudSDKException as e:
            raise RuntimeError(f"Failed to create online table '{online_table_name}': {e.get_message()}, request_id: {e.get_request_id()}")
        if not resp.Data.Status:
            raise RuntimeError(f"Failed to create online table '{online_table_name}', request_id: {resp.RequestId}")
        self.__logger.info(f"Successfully created online table '{online_table_name}'")

    def drop_online_table(self, catalog_name: str, schema_name: str, table_name: str):
        """
        删除在线特征表
        Args:
            catalog_name: 数据目录名称
            schema_name: 数据库名称
            table_name: 表名
        Raises:
            RuntimeError: 当删除操作失败时抛出
        """
        request = DeleteOnlineTableRequest()
        request.WorkspaceId = self.project
        request.CatalogName = catalog_name
        request.SchemaName = schema_name
        request.TableName = table_name
        try:
            resp = self._feature_service_client.DeleteOnlineTable(request)
        except TencentCloudSDKException as e:
            raise RuntimeError(f"Failed to delete online table '{table_name}': {e.get_message()}, request_id: {e.get_request_id()}")

        if not resp.Data.Status:
            raise RuntimeError(f"Failed to delete online table '{table_name}', request_id: {resp.RequestId}")

        self.__logger.info(f"Successfully deleted online table '{table_name}'")
