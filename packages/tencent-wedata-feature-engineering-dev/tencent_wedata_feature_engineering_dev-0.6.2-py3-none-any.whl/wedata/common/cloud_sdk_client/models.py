
from tencentcloud.common.abstract_model import AbstractModel
import typing
import warnings
from wedata.common.cloud_sdk_client.utils import is_warning


class OfflineFeatureConfiguration(AbstractModel):
    """
    创建在线表时的离线特征部分描述
    """

    def __init__(self):
        self._DatasourceName = None
        self._TableName = None
        self._DatasourceType = None
        self._PrimaryKeys = None
        self._TimestampColumn = None
        self._DatabaseName = None
        self._EngineName = None

    @property
    def DatasourceName(self):
        return self._DatasourceName

    @DatasourceName.setter
    def DatasourceName(self, DatasourceName):
        self._DatasourceName = DatasourceName

    @property
    def TableName(self):
        return self._TableName

    @TableName.setter
    def TableName(self, TableName):
        self._TableName = TableName

    @property
    def DatasourceType(self):
        return self._DatasourceType

    @DatasourceType.setter
    def DatasourceType(self, DatasourceType):
        self._DatasourceType = DatasourceType

    @property
    def PrimaryKeys(self):
        return self._PrimaryKeys

    @PrimaryKeys.setter
    def PrimaryKeys(self, PrimaryKeys):
        self._PrimaryKeys = PrimaryKeys

    @property
    def TimestampColumn(self):
        return self._TimestampColumn

    @TimestampColumn.setter
    def TimestampColumn(self, TimestampColumn):
        self._TimestampColumn = TimestampColumn

    @property
    def DatabaseName(self):
        return self._DatabaseName

    @DatabaseName.setter
    def DatabaseName(self, DatabaseName):
        self._DatabaseName = DatabaseName

    @property
    def EngineName(self):
        return self._EngineName

    @EngineName.setter
    def EngineName(self, EngineName):
        self._EngineName = EngineName

    def _deserialize(self, params):
        self._DatasourceName = params.get("DatasourceName")
        self._TableName = params.get("TableName")
        self._DatasourceType = params.get("DatasourceType")
        self._PrimaryKeys = params.get("PrimaryKeys")
        self._TimestampColumn = params.get("TimestampColumn")
        self._DatabaseName = params.get("DatabaseName")
        self._EngineName = params.get("EngineName")
        member_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in member_set:
                member_set.remove(property_name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class TaskSchedulerConfiguration(AbstractModel):
    """
    创建在线特征表时的调度信息描述
    CycleType: 调度周期类型
    ScheduleTimeZone: 调度时区
    StartTime: 调度开始时间
    EndTime: 调度结束时间
    ExecutionStartTime: 执行开始时间
    ExecutionEndTime: 执行结束时间
    RunPriority: 运行优先级
    CrontabExpression: cron表达式
    """

    def __init__(self):
        self._CycleType = None
        self._ScheduleTimeZone = None
        self._StartTime = None
        self._EndTime = None
        self._ExecutionStartTime = None
        self._ExecutionEndTime = None
        self._RunPriority = None
        self._CrontabExpression = None

    @property
    def CycleType(self):
        return self._CycleType

    @CycleType.setter
    def CycleType(self, CycleType):
        self._CycleType = CycleType

    @property
    def ScheduleTimeZone(self):
        return self._ScheduleTimeZone

    @ScheduleTimeZone.setter
    def ScheduleTimeZone(self, ScheduleTimeZone):
        self._ScheduleTimeZone = ScheduleTimeZone

    @property
    def StartTime(self):
        return self._StartTime

    @StartTime.setter
    def StartTime(self, StartTime):
        self._StartTime = StartTime

    @property
    def EndTime(self):
        return self._EndTime

    @EndTime.setter
    def EndTime(self, EndTime):
        self._EndTime = EndTime

    @property
    def ExecutionStartTime(self):
        return self._ExecutionStartTime

    @ExecutionStartTime.setter
    def ExecutionStartTime(self, ExecutionStartTime):
        self._ExecutionStartTime = ExecutionStartTime

    @property
    def ExecutionEndTime(self):
        return self._ExecutionEndTime

    @ExecutionEndTime.setter
    def ExecutionEndTime(self, ExecutionEndTime):
        self._ExecutionEndTime = ExecutionEndTime

    @property
    def RunPriority(self):
        return self._RunPriority

    @RunPriority.setter
    def RunPriority(self, RunPriority):
        self._RunPriority = RunPriority

    @property
    def CrontabExpression(self):
        return self._CrontabExpression

    @CrontabExpression.setter
    def CrontabExpression(self, CrontabExpression):
        self._CrontabExpression = CrontabExpression

    def _deserialize(self, params):
        self.CycleType = params.get("CycleType")
        self.ScheduleTimeZone = params.get("ScheduleTimeZone")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.ExecutionStartTime = params.get("ExecutionStartTime")
        self.ExecutionEndTime = params.get("ExecutionEndTime")
        self.RunPriority = params.get("RunPriority")
        self.CrontabExpression = params.get("CrontabExpression")
        member_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in member_set:
                member_set.remove(property_name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class OnlineFeatureConfiguration(AbstractModel):
    """
    在线特征信息
    """

    def __init__(self):
        self._UseDefault = None
        self._DatasourceName = None
        self._DB = None
        self._Host = None
        self._Port = None

    @property
    def UserDefault(self):
        return self._UseDefault

    @UserDefault.setter
    def UserDefault(self, UseDefault):
        self._UseDefault = UseDefault

    @property
    def DataSourceName(self):
        return self._DataSourceName

    @DataSourceName.setter
    def DataSourceName(self, DataSourceName):
        self._DataSourceName = DataSourceName

    @property
    def DB(self):
        return self._DB

    @DB.setter
    def DB(self, DB):
        self._DB = DB

    @property
    def Host(self):
        return self._Host

    @Host.setter
    def Host(self, Host: str):
        self._Host = Host

    @property
    def Port(self):
        return self._Port

    @Port.setter
    def Port(self, Port: int):
        self._Port = Port

    def _deserialize(self, params):
        self.UseDefault = params.get("UseDefault")
        self.DataSourceName = params.get("DataSourceName")
        self.DB = params.get("DB")
        self.Host = params.get("Host")
        self.Port = params.get("Port")
        member_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in member_set:
                member_set.remove(property_name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class CreateOnlineFeatureTableRequest(AbstractModel):
    """
    创建在线特征表
    ProjectId
    ResourceGroupId
    OfflineFeatureConfiguration
    TaskSchedulerConfiguration
    OnlineFeatureConfiguration
    RequestFromSource
    """

    def __init__(self):
        self._ProjectId = None
        self._ResourceGroupId = None
        self._OfflineFeatureConfiguration = None
        self._TaskSchedulerConfiguration = None
        self._OnlineFeatureConfiguration = None
        self._RequestSource = None

    @property
    def ProjectId(self):
        return self._ProjectId

    @ProjectId.setter
    def ProjectId(self, ProjectId):
        self._ProjectId = ProjectId

    @property
    def ResourceGroupId(self):
        return self._ResourceGroupId

    @ResourceGroupId.setter
    def ResourceGroupId(self, ResourceGroupId):
        self._ResourceGroupId = ResourceGroupId

    @property
    def OfflineFeatureConfiguration(self):
        return self._OfflineFeatureConfiguration

    @OfflineFeatureConfiguration.setter
    def OfflineFeatureConfiguration(self, OfflineFeatureConfiguration):
        self._OfflineFeatureConfiguration = OfflineFeatureConfiguration

    @property
    def TaskSchedulerConfiguration(self):
        return self._TaskSchedulerConfiguration

    @TaskSchedulerConfiguration.setter
    def TaskSchedulerConfiguration(self, TaskSchedulerConfiguration):
        self._TaskSchedulerConfiguration = TaskSchedulerConfiguration

    @property
    def OnlineFeatureConfiguration(self):
        return self._OnlineFeatureConfiguration

    @OnlineFeatureConfiguration.setter
    def OnlineFeatureConfiguration(self, OnlineFeatureConfiguration):
        self._OnlineFeatureConfiguration = OnlineFeatureConfiguration

    def _deserialize(self, params):
        self.ProjectId = params.get("ProjectId")
        self.ResourceGroupId = params.get("ResourceGroupId")
        if params.get("OfflineFeatureConfiguration") is not None:
            self.OfflineFeatureConfiguration = OfflineFeatureConfiguration()
            self.OfflineFeatureConfiguration._deserialize(params.get("OfflineFeatureConfiguration"))
        if params.get("TaskSchedulerConfiguration") is not None:
            self.TaskSchedulerConfiguration = TaskSchedulerConfiguration()
            self.TaskSchedulerConfiguration._deserialize(params.get("TaskSchedulerConfiguration"))
        if params.get("OnlineFeatureConfiguration") is not None:
            self._OnlineFeatureConfiguration = OnlineFeatureConfiguration()
            self._OnlineFeatureConfiguration._deserialize(params.get("OnlineFeatureConfiguration"))
        member_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in member_set:
                member_set.remove(property_name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class CreateOnlineFeatureTableRsp(AbstractModel):
    """
    创建在线特征表返回包
    """

    def __init__(self):
        self._OfflineTableId = None
        self._OnlineTableId = None

    @property
    def OfflineTableId(self):
        return self._OfflineTableId

    @OfflineTableId.setter
    def OfflineTableId(self, OfflineTableId):
        self._OfflineTableId = OfflineTableId

    @property
    def OnlineTableId(self):
        return self._OnlineTableId

    @OnlineTableId.setter
    def OnlineTableId(self, OnlineTableId):
        self._OnlineTableId = OnlineTableId

    def _deserialize(self, params):
        self._OfflineTableId = params.get("OfflineTableId")
        self._OnlineTableId = params.get("OnlineTableId")
        member_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in member_set:
                member_set.remove(property_name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class CreateOnlineFeatureTableResponse(AbstractModel):
    """
    创建在线特征表返回包
    """

    def __init__(self):
        self._Data = None

    @property
    def Data(self) -> CreateOnlineFeatureTableRsp:
        return self._Data

    @Data.setter
    def Data(self, Data):
        self._Data = Data

    def _deserialize(self, params):
        self.Data = CreateOnlineFeatureTableRsp()
        self.Data._deserialize(params.get("Data"))
        member_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in member_set:
                member_set.remove(property_name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class DescribeNormalSchedulerExecutorGroupsData(AbstractModel):
    """
    执行资源组管理-可用的调度资源组列表
    ExecutorGroupId
    ExecutorGroupName
    ExecutorGroupDesc
    Available
    PythonSubVersions
    EnvJson
    """

    def __init__(self):
        self._ExecutorGroupId = None
        self._ExecutorGroupName = None
        self._ExecutorGroupDesc = None
        self._Available = None
        self._PythonSubVersions = None
        self._EnvJson = None

    @property
    def ExecutorGroupId(self):
        return self._ExecutorGroupId

    @ExecutorGroupId.setter
    def ExecutorGroupId(self, ExecutorGroupId):
        self._ExecutorGroupId = ExecutorGroupId

    @property
    def ExecutorGroupName(self):
        return self._ExecutorGroupName

    @ExecutorGroupName.setter
    def ExecutorGroupName(self, ExecutorGroupName):
        self._ExecutorGroupName = ExecutorGroupName

    @property
    def ExecutorGroupDesc(self):
        return self._ExecutorGroupDesc

    @ExecutorGroupDesc.setter
    def ExecutorGroupDesc(self, ExecutorGroupDesc):
        self._ExecutorGroupDesc = ExecutorGroupDesc

    @property
    def Available(self):
        return self._Available

    @Available.setter
    def Available(self, Available):
        self._Available = Available

    @property
    def PythonSubVersions(self):
        return self._PythonSubVersions

    @PythonSubVersions.setter
    def PythonSubVersions(self, PythonSubVersions):
        self._PythonSubVersions = PythonSubVersions

    @property
    def EnvJson(self):
        return self._EnvJson

    @EnvJson.setter
    def EnvJson(self, EnvJson):
        self._EnvJson = EnvJson

    def _deserialize(self, params):
        self._ExecutorGroupId = params.get("ExecutorGroupId")
        self._ExecutorGroupName = params.get("ExecutorGroupName")
        self._ExecutorGroupDesc = params.get("ExecutorGroupDesc")
        self._Available = params.get("Available")
        self._PythonSubVersions = params.get("PythonSubVersions")
        self._EnvJson = params.get("EnvJson")
        member_set = set(params.keys())
        for name, value in vars(self).items():
            if name in member_set:
                member_set.remove(name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class DescribeNormalSchedulerExecutorGroupsResponse(AbstractModel):
    """
    查询可用的调度执行资源
    """

    def __init__(self):
        self._Data = None

    @property
    def Data(self) -> list[DescribeNormalSchedulerExecutorGroupsData]:
        return self._Data

    @Data.setter
    def Data(self, Data):
        self._Data = Data

    def _deserialize(self, params):
        if params.get("Data") is not None:
            self._Data = []
            for item in params.get("Data", []):
                obj = DescribeNormalSchedulerExecutorGroupsData()
                obj._deserialize(item)
                self._Data.append(obj)
        member_set = set(params.keys())
        for name, value in vars(self).items():
            if name in member_set:
                member_set.remove(name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class DescribeNormalSchedulerExecutorGroupsRequest(AbstractModel):
    """
    查询可用的调度执行资源
    """

    def __init__(self):
        self._ProjectId = None
        self._OnlyAvailable = None

    @property
    def ProjectId(self):
        return self._ProjectId

    @ProjectId.setter
    def ProjectId(self, ProjectId: str):
        self._ProjectId = ProjectId

    @property
    def OnlyAvailable(self):
        return self._OnlyAvailable

    @OnlyAvailable.setter
    def OnlyAvailable(self, OnlyAvailable: bool):
        self._OnlyAvailable = OnlyAvailable

    def _deserialize(self, params):
        self._ProjectId = params.get("ProjectId")
        self._OnlyAvailable = params.get("OnlyAvailable")
        member_set = set(params.keys())
        for name, value in vars(self).items():
            if name in member_set:
                member_set.remove(name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class RefreshFeatureTableRequest(AbstractModel):
    """
    刷新特征表
    Property:
        ProjectId: 项目ID
        ActionName: 行为:Create-创建;Delete-删除
        DatabaseName: 特征库名称
        TableName: 特征表名称
        DatasourceName: 数据源名称
        DatasourceType: 数据源类型: EMR/DLC
        EngineName: 引擎名称
        IsTry: 是否尝试操作
    """
    def __init__(self):
        self._ProjectId = None
        self._ActionName = None
        self._DatabaseName = None
        self._TableName = None
        self._DatasourceName = None
        self._DatasourceType = None
        self._EngineName = None
        self._IsTry = None

    @property
    def ProjectId(self):
        return self._ProjectId

    @ProjectId.setter
    def ProjectId(self, ProjectId):
        self._ProjectId = ProjectId

    @property
    def ActionName(self):
        return self._ActionName

    @ActionName.setter
    def ActionName(self, ActionName):
        self._ActionName = ActionName

    @property
    def DatabaseName(self):
        return self._DatabaseName

    @DatabaseName.setter
    def DatabaseName(self, DatabaseName):
        self._DatabaseName = DatabaseName

    @property
    def TableName(self):
        return self._TableName

    @TableName.setter
    def TableName(self, TableName):
        self._TableName = TableName

    @property
    def DatasourceName(self):
        return self._DatasourceName

    @DatasourceName.setter
    def DatasourceName(self, DatasourceName):
        self._DatasourceName = DatasourceName

    @property
    def DatasourceType(self):
        return self._DatasourceType

    @DatasourceType.setter
    def DatasourceType(self, DatasourceType):
        self._DatasourceType = DatasourceType

    @property
    def EngineName(self):
        return self._EngineName

    @EngineName.setter
    def EngineName(self, EngineName):
        self._EngineName = EngineName

    @property
    def IsTry(self):
        return self._IsTry

    @IsTry.setter
    def IsTry(self, IsTry):
        self._IsTry = IsTry

    def _deserialize(self, params):
        self._ProjectId = params.get("ProjectId")
        self._ActionName = params.get("ActionName")
        self._DatabaseName = params.get("DatabaseName")
        self._TableName = params.get("TableName")
        self._DatasourceName = params.get("DatasourceName")
        self._DatasourceType = params.get("DatasourceType")
        self._EngineName = params.get("EngineName")
        self._IsTry = params.get("IsTry")
        member_set = set(params.keys())
        for name, value in vars(self).items():
            if name in member_set:
                member_set.remove(name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class RefreshFeatureTableResponse(AbstractModel):
    """
    刷新特征表
    Property:
        Data: 结果
    """
    def __init__(self):
        self._Data = None

    @property
    def Data(self):
        return self._Data

    @Data.setter
    def Data(self, Data):
        self._Data = Data

    def _deserialize(self, params):
        self._Data = params.get("Data")
        member_set = set(params.keys())
        for name, value in vars(self).items():
            if name in member_set:
                member_set.remove(name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class FeatureStoreDatabase(AbstractModel):
    """
    特征存储库
    Property:
        DatabaseName: 特征库名称
        DatasourceType: 数据源类型: EMR/DLC
        EngineName: 引擎名称
        ProjectId: 项目ID
        IsDefault: 是否默认库
        IsExistDatabase: 是否存在库
        DatasourceId: 数据源ID
        OnlineMode: 在线模式: 0-离线; 1-在线
        DatasourceName: 数据源名称
    """
    def __init__(self):
        self._DatabaseName = None
        self._DatasourceType = None
        self._EngineName = None
        self._ProjectId = None
        self._IsDefault = None
        self._IsExistDatabase = None
        self._DatasourceId = None
        self._OnlineMode = None
        self._DatasourceName = None

    @property
    def DatabaseName(self):
        return self._DatabaseName

    @DatabaseName.setter
    def DatabaseName(self, DatabaseName):
        self._DatabaseName = DatabaseName

    @property
    def DatasourceType(self):
        return self._DatasourceType

    @DatasourceType.setter
    def DatasourceType(self, DatasourceType):
        self._DatasourceType = DatasourceType

    @property
    def EngineName(self):
        return self._EngineName

    @EngineName.setter
    def EngineName(self, EngineName):
        self._EngineName = EngineName

    @property
    def ProjectId(self):
        return self._ProjectId

    @ProjectId.setter
    def ProjectId(self, ProjectId):
        self._ProjectId = ProjectId

    @property
    def IsDefault(self):
        return self._IsDefault

    @IsDefault.setter
    def IsDefault(self, IsDefault):
        self._IsDefault = IsDefault

    @property
    def IsExistDatabase(self):
        return self._IsExistDatabase

    @IsExistDatabase.setter
    def IsExistDatabase(self, IsExistDatabase):
        self._IsExistDatabase = IsExistDatabase

    @property
    def DatasourceId(self):
        return self._DatasourceId

    @DatasourceId.setter
    def DatasourceId(self, DatasourceId):
        self._DatasourceId = DatasourceId

    @property
    def OnlineMode(self):
        return self._OnlineMode

    @OnlineMode.setter
    def OnlineMode(self, OnlineMode):
        self._OnlineMode = OnlineMode

    @property
    def DatasourceName(self):
        return self._DatasourceName

    @DatasourceName.setter
    def DatasourceName(self, DatasourceName):
        self._DatasourceName = DatasourceName

    def _deserialize(self, params):
        self._DatabaseName = params.get("DatabaseName")
        self._DatasourceType = params.get("DatasourceType")
        self._EngineName = params.get("EngineName")
        self._ProjectId = params.get("ProjectId")
        self._IsDefault = params.get("IsDefault")
        self._IsExistDatabase = params.get("IsExistDatabase")
        self._DatasourceId = params.get("DatasourceId")
        self._OnlineMode = params.get("OnlineMode")
        self._DatasourceName = params.get("DatasourceName")
        member_set = set(params.keys())
        for name, value in vars(self).items():
            if name in member_set:
                member_set.remove(name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class DescribeFeatureStoreDatabasesResponse(AbstractModel):
    """
    描述特征库
    Property:
        Data: 结果
    """
    def __init__(self):
        self._Data = None

    @property
    def Data(self) -> typing.List[FeatureStoreDatabase]:
        return self._Data

    @Data.setter
    def Data(self, Data):
        self._Data = Data

    def _deserialize(self, params):
        self._Data = []
        for item in params.get("Data", []):
            obj = FeatureStoreDatabase()
            obj._deserialize(item)
            self._Data.append(obj)
        member_set = set(params.keys())
        for name, value in vars(self).items():
            if name in member_set:
                member_set.remove(name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class DescribeFeatureStoreDatabasesRequest(AbstractModel):
    """
    Property:
       ProjectId: 项目ID
    """
    def __init__(self):
        self._ProjectId = None

    @property
    def ProjectId(self):
        return self._ProjectId

    @ProjectId.setter
    def ProjectId(self, ProjectId):
        self._ProjectId = ProjectId

    def _deserialize(self, params):
        self._ProjectId = params.get("ProjectId")
        member_set = set(params.keys())
        for name, value in vars(self).items():
            if name in member_set:
                member_set.remove(name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class OfflineFeatureTable(AbstractModel):
    """
    WeData3.0 表名信息
    Property:
        CatalogName: 数据目录名称
        SchemaName: 数据库名称
        TableName: 表名
    """
    def __init__(self) -> None:
        self._CatalogName = None
        self._SchemaName = None
        self._TableName = None

    @property
    def CatalogName(self) -> str:
        return self._CatalogName

    @CatalogName.setter
    def CatalogName(self, CatalogName: str):
        self._CatalogName = CatalogName

    @property
    def SchemaName(self) -> str:
        return self._SchemaName

    @SchemaName.setter
    def SchemaName(self, SchemaName: str):
        self._SchemaName = SchemaName

    @property
    def TableName(self) -> str:
        return self._TableName

    @TableName.setter
    def TableName(self, TableName: str):
        self._TableName = TableName

    def _deserialize(self,
                     params: typing.Dict[str, typing.Any]) -> None:
        self._CatalogName = params.get("CatalogName")
        self._SchemaName = params.get("SchemaName")
        self._TableName = params.get("TableName")
        member_set = set(params.keys())
        for name, value in vars(self).items():
            if name in member_set:
                member_set.remove(name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class OfflineFeatureTableConfiguration(AbstractModel):
    """
    WeData3.0 离线特征配置
    Property:
        TableNameInfo: 表名信息
        PrimaryKeys: 主键列表
        TimestampColumn: 时间戳列名
    """
    def __init__(self) -> None:
        self._TableNameInfo = None
        self._PrimaryKeys = None
        self._TimestampColumn = None

    @property
    def TableNameInfo(self) -> OfflineFeatureTable:
        return self._TableNameInfo

    @TableNameInfo.setter
    def TableNameInfo(self, TableNameInfo: OfflineFeatureTable):
        self._TableNameInfo = TableNameInfo

    @property
    def PrimaryKeys(self) -> typing.List[str]:
        return self._PrimaryKeys

    @PrimaryKeys.setter
    def PrimaryKeys(self, PrimaryKeys: typing.List[str]):
        self._PrimaryKeys = PrimaryKeys

    @property
    def TimestampColumn(self) -> str:
        return self._TimestampColumn

    @TimestampColumn.setter
    def TimestampColumn(self, TimestampColumn: str):
        self._TimestampColumn = TimestampColumn

    def _deserialize(self,
                     params: typing.Dict[str, typing.Any]) -> None:
        if params.get("TableNameInfo") is not None:
            self._TableNameInfo = OfflineFeatureTable()
            self._TableNameInfo._deserialize(params.get("TableNameInfo"))
        self._PrimaryKeys = params.get("PrimaryKeys")
        self._TimestampColumn = params.get("TimestampColumn")
        member_set = set(params.keys())
        for name, value in vars(self).items():
            if name in member_set:
                member_set.remove(name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class WorkflowTriggerConfiguration(AbstractModel):
    """
    WeData3.0 工作流调度配置
    Property:
        TriggerMode: 触发方式:
            定时触发: TIME_TRIGGER;
            文件到达: FILE_REACH;
            持续运行: CONTINUE_RUN
        SchedulerTimeZone: 调度时区
        StartTime: 调度生效时间
        EndTime: 调度结束时间
        ConfigMode: 配置方式:
            常规: COMMON;
            CRON表达式: CRON_EXPRESSION
        CycleType: 周期类型, 支持的类型为:
            ONEOFF_CYCLE: 一次性
            YEAR_CYCLE: 年
            MONTH_CYCLE: 月
            WEEK_CYCLE: 周
            DAY_CYCLE: 天
            HOUR_CYCLE: 小时
            MINUTE_CYCLE: 分钟
            CRONTAB_CYCLE: crontab表达式类型
        CrontabExpression: crontab表达式
    """
    def __init__(self) -> None:
        self._TriggerMode = None
        self._SchedulerTimeZone = None
        self._StartTime = None
        self._EndTime = None
        self._ConfigMode = None
        self._CycleType = None
        self._CrontabExpression = None

    @property
    def TriggerMode(self) -> str:
        return self._TriggerMode

    @TriggerMode.setter
    def TriggerMode(self, TriggerMode: str):
        self._TriggerMode = TriggerMode

    @property
    def SchedulerTimeZone(self) -> str:
        return self._SchedulerTimeZone

    @SchedulerTimeZone.setter
    def SchedulerTimeZone(self, SchedulerTimeZone: str):
        self._SchedulerTimeZone = SchedulerTimeZone

    @property
    def StartTime(self) -> str:
        return self._StartTime

    @StartTime.setter
    def StartTime(self, StartTime: str):
        self._StartTime = StartTime

    @property
    def EndTime(self) -> str:
        return self._EndTime

    @EndTime.setter
    def EndTime(self, EndTime: str):
        self._EndTime = EndTime

    @property
    def ConfigMode(self) -> str:
        return self._ConfigMode

    @ConfigMode.setter
    def ConfigMode(self, ConfigMode: str):
        self._ConfigMode = ConfigMode

    @property
    def CycleType(self) -> str:
        return self._CycleType

    @CycleType.setter
    def CycleType(self, CycleType: str):
        self._CycleType = CycleType

    @property
    def CrontabExpression(self) -> str:
        return self._CrontabExpression

    @CrontabExpression.setter
    def CrontabExpression(self, CrontabExpression: str):
        self._CrontabExpression = CrontabExpression

    def _deserialize(self,
                     params: typing.Dict[str, typing.Any]) -> None:
        self._TriggerMode = params.get("TriggerMode")
        self._SchedulerTimeZone = params.get("SchedulerTimeZone")
        self._StartTime = params.get("StartTime")
        self._EndTime = params.get("EndTime")
        self._ConfigMode = params.get("ConfigMode")
        self._CycleType = params.get("CycleType")
        self._CrontabExpression = params.get("CrontabExpression")
        member_set = set(params.keys())
        for name, value in vars(self).items():
            if name in member_set:
                member_set.remove(name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class WorkflowAdvanceConfiguration(AbstractModel):
    """
    WeData3.0 工作流高级设置
    Property:
        QueuingMode: 排队模式: ON(默认), OFF
        MaxConcurrentNum: 最大并发数
    """
    def __init__(self) -> None:
        self._QueuingMode = None
        self._MaxConcurrentNum = None

    @property
    def QueuingMode(self) -> str:
        return self._QueuingMode

    @QueuingMode.setter
    def QueuingMode(self, QueuingMode: str):
        self._QueuingMode = QueuingMode

    @property
    def MaxConcurrentNum(self) -> int:
        return self._MaxConcurrentNum

    @MaxConcurrentNum.setter
    def MaxConcurrentNum(self, MaxConcurrentNum: int):
        self._MaxConcurrentNum = MaxConcurrentNum

    def _deserialize(self,
                     params: typing.Dict[str, typing.Any]) -> None:
        self._QueuingMode = params.get("QueuingMode")
        self._MaxConcurrentNum = params.get("MaxConcurrentNum")
        member_set = set(params.keys())
        for name, value in vars(self).items():
            if name in member_set:
                member_set.remove(name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class SchedulerConfiguration(AbstractModel):
    """
    WeData3.0 任务调度配置
    Property:
        Trigger: 触发配置
        AdvanceConfig: 高级配置
    """
    def __init__(self) -> None:
        self._Trigger = None
        self._AdvanceConfig = None

    @property
    def Trigger(self) -> WorkflowTriggerConfiguration:
        return self._Trigger

    @Trigger.setter
    def Trigger(self, Trigger: WorkflowTriggerConfiguration):
        self._Trigger = Trigger

    @property
    def AdvanceConfig(self) -> WorkflowAdvanceConfiguration:
        return self._AdvanceConfig

    @AdvanceConfig.setter
    def AdvanceConfig(self, AdvanceConfig: WorkflowAdvanceConfiguration):
        self._AdvanceConfig = AdvanceConfig

    def _deserialize(self, params: typing.Dict[str, typing.Any]) -> None:
        if params.get("Trigger") is not None:
            self._Trigger = WorkflowTriggerConfiguration()
            self._Trigger._deserialize(params.get("Trigger"))
        if params.get("AdvanceConfig") is not None:
            self._AdvanceConfig = WorkflowAdvanceConfiguration()
            self._AdvanceConfig._deserialize(params.get("AdvanceConfig"))
        member_set = set(params.keys())
        for name, value in vars(self).items():
            if name in member_set:
                member_set.remove(name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class CreateOnlineTableRequest(AbstractModel):
    """
    WeData3.0 创建在线特征表请求体
    Property:
        WorkspaceId: 工作空间ID
        ResourceGroupId: 资源组ID
        TargetPath: 目标路径
        OfflineFeatureConfiguration: 离线表信息
        TaskSchedulerConfiguration: 任务调度配置
    """

    def __init__(self) -> None:
        self._WorkspaceId = None
        self._ResourceGroupId = None
        self._TargetPath = None
        self._ConnectionId = None
        self._OfflineFeatureConfiguration = None
        self._TaskSchedulerConfiguration = None

    @property
    def WorkspaceId(self) -> str:
        return self._WorkspaceId

    @WorkspaceId.setter
    def WorkspaceId(self, WorkspaceId: str):
        self._WorkspaceId = WorkspaceId

    @property
    def ResourceGroupId(self) -> str:
        return self._ResourceGroupId

    @ResourceGroupId.setter
    def ResourceGroupId(self, ResourceGroupId: str):
        self._ResourceGroupId = ResourceGroupId

    @property
    def TargetPath(self) -> OfflineFeatureTable:
        return self._TargetPath

    @TargetPath.setter
    def TargetPath(self, TargetPath: OfflineFeatureTable):
        self._TargetPath = TargetPath

    @property
    def ConnectionId(self) -> str:
        return self._ConnectionId

    @ConnectionId.setter
    def ConnectionId(self, ConnectionId: str):
        self._ConnectionId = ConnectionId

    @property
    def OfflineFeatureConfiguration(self) -> OfflineFeatureTableConfiguration:
        return self._OfflineFeatureConfiguration

    @OfflineFeatureConfiguration.setter
    def OfflineFeatureConfiguration(self, OfflineFeatureConfiguration: OfflineFeatureTableConfiguration):
        self._OfflineFeatureConfiguration = OfflineFeatureConfiguration

    @property
    def TaskSchedulerConfiguration(self) -> SchedulerConfiguration:
        return self._TaskSchedulerConfiguration

    @TaskSchedulerConfiguration.setter
    def TaskSchedulerConfiguration(self, TaskSchedulerConfiguration: SchedulerConfiguration):
        self._TaskSchedulerConfiguration = TaskSchedulerConfiguration

    def _deserialize(self,
                    params: typing.Dict[str, typing.Any]) -> None:
        self._WorkspaceId = params.get("WorkspaceId")
        self._ResourceGroupId = params.get("ResourceGroupId")
        self._ConnectionId = params.get("ConnectionId")
        if params.get("TargetPath") is not None:
            self._TargetPath = OfflineFeatureTable()
            self._TargetPath._deserialize(params.get("TargetPath"))
        if params.get("OfflineFeatureConfiguration") is not None:
            self._OfflineFeatureConfiguration = OfflineFeatureConfiguration()
            self._OfflineFeatureConfiguration._deserialize(params.get("OfflineFeatureConfiguration"))
        if params.get("TaskSchedulerConfiguration") is not None:
            self._TaskSchedulerConfiguration = TaskSchedulerConfiguration()
            self._TaskSchedulerConfiguration._deserialize(params.get("TaskSchedulerConfiguration"))
        member_set = set(params.keys())
        for name, value in vars(self).items():
            if name in member_set:
                member_set.remove(name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class CreateOnlineTableData(AbstractModel):
    """
    WeData3.0 创建在线特征表数据
    Property:
        Status: 状态
    """
    def __init__(self) -> None:
        self._Status = None

    @property
    def Status(self) -> bool:
        return self._Status

    @Status.setter
    def Status(self, Status: bool):
        self._Status = Status

    def _deserialize(self,
                    params: typing.Dict[str, typing.Any]) -> None:
        self._Status = params.get("Status")
        member_set = set(params.keys())
        for name, value in vars(self).items():
            if name in member_set:
                member_set.remove(name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class CreateOnlineTableResponse(AbstractModel):
    """
    WeData3.0 创建在线特征表响应体
    Property:
        Data: 状态
        RequestId: 请求ID
    """
    def __init__(self) -> None:
        self._Data = None
        self._RequestId = None

    @property
    def Data(self) -> CreateOnlineTableData:
        return self._Data

    @Data.setter
    def Data(self, Data: CreateOnlineTableData):
        self._Data = Data

    @property
    def RequestId(self) -> str:
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId: str):
        self._RequestId = RequestId

    def _deserialize(self,
                    params: typing.Dict[str, typing.Any]) -> None:
        if params.get("Data") is not None:
            self._Data = CreateOnlineTableData()
            self._Data._deserialize(params.get("Data"))
        self._RequestId = params.get("RequestId")
        member_set = set(params.keys())
        for name, value in vars(self).items():
            if name in member_set:
                member_set.remove(name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class DeleteOnlineTableRequest(AbstractModel):
    """
    WeData3.0 删除在线特征表请求体
    Property:
        WorkspaceId: 工作空间ID
        CatalogName: 数据目录名称
        SchemaName: 数据库名称
        TableName: 表名称
    """
    def __init__(self) -> None:
        self._WorkspaceId = None
        self._CatalogName = None
        self._SchemaName = None
        self._TableName = None

    @property
    def WorkspaceId(self) -> str:
        return self._WorkspaceId

    @WorkspaceId.setter
    def WorkspaceId(self, WorkspaceId: str):
        self._WorkspaceId = WorkspaceId

    @property
    def CatalogName(self) -> str:
        return self._CatalogName

    @CatalogName.setter
    def CatalogName(self, CatalogName: str):
        self._CatalogName = CatalogName

    @property
    def SchemaName(self) -> str:
        return self._SchemaName

    @SchemaName.setter
    def SchemaName(self, SchemaName: str):
        self._SchemaName = SchemaName

    @property
    def TableName(self) -> str:
        return self._TableName

    @TableName.setter
    def TableName(self, TableName: str):
        self._TableName = TableName

    def _deserialize(self,
                    params: typing.Dict[str, typing.Any]) -> None:
        self._WorkspaceId = params.get("WorkspaceId")
        self._CatalogName = params.get("CatalogName")
        self._SchemaName = params.get("SchemaName")
        self._TableName = params.get("TableName")
        member_set = set(params.keys())
        for name, value in vars(self).items():
            if name in member_set:
                member_set.remove(name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class DeleteOnlineTableData(AbstractModel):
    """
    WeData3.0 删除在线特征表数据
    Property:
        Status: 状态
    """
    def __init__(self) -> None:
        self._Status = None

    @property
    def Status(self) -> bool:
        return self._Status

    @Status.setter
    def Status(self, Status: bool):
        self._Status = Status

    def _deserialize(self,
                    params: typing.Dict[str, typing.Any]) -> None:
        self._Status = params.get("Status")
        member_set = set(params.keys())
        for name, value in vars(self).items():
            if name in member_set:
                member_set.remove(name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class DeleteOnlineTableResponse(AbstractModel):
    """
    WeData3.0 删除在线特征表响应体
    Property:
        Data: 删除在线特征表数据
        RequestId: 请求ID
    """

    def __init__(self) -> None:
        self._Data = None
        self._RequestId = None

    @property
    def Data(self) -> DeleteOnlineTableData:
        return self._Data

    @Data.setter
    def Data(self, Data: DeleteOnlineTableData):
        self._Data = Data

    @property
    def RequestId(self) -> str:
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId: str):
        self._RequestId = RequestId

    def _deserialize(self,
                    params: typing.Dict[str, typing.Any]) -> None:
        if params.get("Data") is not None:
            self._Data = DeleteOnlineTableData()
            self._Data._deserialize(params.get("Data"))
        self._RequestId = params.get("RequestId")
        member_set = set(params.keys())
        for name, value in vars(self).items():
            if name in member_set:
                member_set.remove(name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class ListComputeResourcesRequest(AbstractModel):
    """
    WeData3.0 获取计算资源列表
    Property:
        WorkspaceId: 工作空间ID
        ResourceTypes: 资源类型列表
        ResourceStatuses: 资源状态列表
        PageNumber: 页数
        PageSize: 页大小
    """
    def __init__(self) -> None:
        self._WorkspaceId = None
        self._ResourceTypes = None
        self._ResourceStatuses = None
        self._PageNumber = None
        self._PageSize = None

    @property
    def WorkspaceId(self) -> str:
        return self._WorkspaceId

    @WorkspaceId.setter
    def WorkspaceId(self, WorkspaceId: str):
        self._WorkspaceId = WorkspaceId

    @property
    def ResourceTypes(self) -> typing.List[int]:
        return self._ResourceTypes

    @ResourceTypes.setter
    def ResourceTypes(self, ResourceTypes: typing.List[int]):
        self._ResourceTypes = ResourceTypes

    @property
    def ResourceStatuses(self) -> typing.List[int]:
        return self._ResourceStatuses

    @ResourceStatuses.setter
    def ResourceStatuses(self, ResourceStatuses: typing.List[int]):
        self._ResourceStatuses = ResourceStatuses

    @property
    def PageNumber(self) -> int:
        return self._PageNumber

    @PageNumber.setter
    def PageNumber(self, PageNumber: int):
        self._PageNumber = PageNumber

    @property
    def PageSize(self) -> int:
        return self._PageSize

    @PageSize.setter
    def PageSize(self, PageSize: int):
        self._PageSize = PageSize

    def _deserialize(self,
                    params: typing.Dict[str, typing.Any]) -> None:
        self._WorkspaceId = params.get("WorkspaceId")
        self._ResourceTypes = params.get("ResourceTypes")
        self._ResourceStatuses = params.get("ResourceStatuses")
        self._PageNumber = params.get("PageNumber")
        self._PageSize = params.get("PageSize")
        member_set = set(params.keys())
        for name, value in vars(self).items():
            if name in member_set:
                member_set.remove(name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class ComputeResourceBasicInfo(AbstractModel):
    """
    计算资源组基础信息
    """
    def __init__(self) -> None:
        self._ResourceId = None
        self._ResourceName = None
        self._ResourceType = None
        self._ResourceStatus = None

    @property
    def ResourceId(self) -> str:
        return self._ResourceId

    @ResourceId.setter
    def ResourceId(self, ResourceId: str):
        self._ResourceId = ResourceId

    @property
    def ResourceName(self) -> str:
        return self._ResourceName

    @ResourceName.setter
    def ResourceName(self, ResourceName: str):
        self._ResourceName = ResourceName

    @property
    def ResourceType(self) -> int:
        return self._ResourceType

    @ResourceType.setter
    def ResourceType(self, ResourceType: int):
        self._ResourceType = ResourceType

    @property
    def ResourceStatus(self) -> int:
        return self._ResourceStatus

    @ResourceStatus.setter
    def ResourceStatus(self, ResourceStatus: int):
        self._ResourceStatus = ResourceStatus

    def _deserialize(self,
                    params: typing.Dict[str, typing.Any]) -> None:
        self._ResourceId = params.get("ResourceId")
        self._ResourceName = params.get("ResourceName")
        self._ResourceType = params.get("ResourceType")
        self._ResourceStatus = params.get("ResourceStatus")
        member_set = set(params.keys())
        for name, value in vars(self).items():
            if name in member_set:
                member_set.remove(name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class ComputeResourceInfo(AbstractModel):
    """资源组信息"""
    def __init__(self) -> None:
        self._BasicInfo = None
        self._BillType = None
        self._CUQuota = None
        self._AutoStopSeconds = None

    @property
    def BasicInfo(self) -> ComputeResourceBasicInfo:
        return self._BasicInfo

    @BasicInfo.setter
    def BasicInfo(self, BasicInfo: ComputeResourceBasicInfo):
        self._BasicInfo = BasicInfo

    @property
    def BillType(self) -> str:
        return self._BillType

    @BillType.setter
    def BillType(self, BillType: str):
        self._BillType = BillType

    @property
    def CUQuota(self) -> int:
        return self._CUQuota

    @CUQuota.setter
    def CUQuota(self, CUQuota: int):
        self._CUQuota = CUQuota

    @property
    def AutoStopSeconds(self) -> int:
        return self._AutoStopSeconds

    @AutoStopSeconds.setter
    def AutoStopSeconds(self, AutoStopSeconds: int):
        self._AutoStopSeconds = AutoStopSeconds

    def _deserialize(self,
                    params: typing.Dict[str, typing.Any]) -> None:
        if params.get("BasicInfo") is not None:
            self._BasicInfo = ComputeResourceBasicInfo()
            self._BasicInfo._deserialize(params.get("BasicInfo"))
        self._BillType = params.get("BillType")
        self._CUQuota = params.get("CUQuota")
        self._AutoStopSeconds = params.get("AutoStopSeconds")
        member_set = set(params.keys())
        for name, value in vars(self).items():
            if name in member_set:
                member_set.remove(name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class ListComputeResourcesData(AbstractModel):
    """
    WeData3.0 获取计算资源列表数据
    Property:
        Resources: 资源列表
    """
    def __init__(self) -> None:
        self._Resources = None

    @property
    def Resources(self) -> typing.List[ComputeResourceInfo]:
        return self._Resources

    @Resources.setter
    def Resources(self, Resources: typing.List[ComputeResourceInfo]):
        self._Resources = Resources

    def _deserialize(self,
                    params: typing.Dict[str, typing.Any]) -> None:
        if params.get("Resources") is not None:
            self._Resources = []
            for item in params.get("Resources"):
                resource = ComputeResourceInfo()
                resource._deserialize(item)
                self._Resources.append(resource)
        member_set = set(params.keys())
        for name, value in vars(self).items():
            if name in member_set:
                member_set.remove(name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class ListComputeResourcesResponse(AbstractModel):
    """
    WeData3.0 获取计算资源列表
    Property:
        Data: 响应数据
        RequestId: 请求ID
    """
    def __init__(self) -> None:
        self._Data = None
        self._RequestId = None

    @property
    def Data(self) -> ListComputeResourcesData:
        return self._Data

    @Data.setter
    def Data(self, Data: ListComputeResourcesData):
        self._Data = Data

    @property
    def RequestId(self) -> str:
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId: str):
        self._RequestId = RequestId

    def _deserialize(self,
                    params: typing.Dict[str, typing.Any]) -> None:
        if params.get("Data") is not None:
            self._Data = ListComputeResourcesData()
            self._Data._deserialize(params.get("Data"))
        self._RequestId = params.get("RequestId")
        member_set = set(params.keys())
        for name, value in vars(self).items():
            if name in member_set:
                member_set.remove(name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class ListConnectionsRequest(AbstractModel):
    """
    获取Connection列表
    """
    def __init__(self) -> None:
        self._WorkspaceId = None
        self._ConnectionId = None
        self._ConnectionType = None
        self._Status = None

    @property
    def WorkspaceId(self) -> str:
        return self._WorkspaceId

    @WorkspaceId.setter
    def WorkspaceId(self, WorkspaceId: str):
        self._WorkspaceId = WorkspaceId

    @property
    def ConnectionId(self) -> typing.List[str]:
        return self._ConnectionId

    @ConnectionId.setter
    def ConnectionId(self, ConnectionId: typing.List[str]):
        self._ConnectionId = ConnectionId

    @property
    def ConnectionType(self) -> typing.List[str]:
        return self._ConnectionType

    @ConnectionType.setter
    def ConnectionType(self, ConnectionType: typing.List[str]):
        self._ConnectionType = ConnectionType

    @property
    def Status(self) -> typing.List[str]:
        return self._Status

    @Status.setter
    def Status(self, Status: typing.List[str]):
        self._Status = Status

    def _deserialize(self,
                    params: typing.Dict[str, typing.Any]) -> None:
        self._WorkspaceId = params.get("WorkspaceId")
        self._ConnectionId = params.get("ConnectionId")
        self._ConnectionType = params.get("ConnectionType")
        self._Status = params.get("Status")
        member_set = set(params.keys())
        for name, value in vars(self).items():
            if name in member_set:
                member_set.remove(name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class ConnectionInfo(AbstractModel):
    def __init__(self) -> None:
        self._ConnectionName = None
        self._DisplayName = None
        self._ConnectionType = None
        self._DeployType = None
        self._AuthType = None
        self._ConnectionDetail = None
        self._ConnectionId = None
        self._Status = None

    @property
    def ConnectionName(self) -> str:
        return self._ConnectionName

    @ConnectionName.setter
    def ConnectionName(self, ConnectionName: str):
        self._ConnectionName = ConnectionName

    @property
    def DisplayName(self) -> str:
        return self._DisplayName

    @DisplayName.setter
    def DisplayName(self, DisplayName: str):
        self._DisplayName = DisplayName

    @property
    def ConnectionType(self) -> str:
        return self._ConnectionType

    @ConnectionType.setter
    def ConnectionType(self, ConnectionType: str):
        self._ConnectionType = ConnectionType

    @property
    def DeployType(self) -> str:
        return self._DeployType

    @DeployType.setter
    def DeployType(self, DeployType: str):
        self._DeployType = DeployType

    @property
    def AuthType(self) -> str:
        return self._AuthType

    @AuthType.setter
    def AuthType(self, AuthType: str):
        self._AuthType = AuthType

    @property
    def ConnectionDetail(self) -> str:
        return self._ConnectionDetail

    @ConnectionDetail.setter
    def ConnectionDetail(self, ConnectionDetail:
                         str):
        self._ConnectionDetail = ConnectionDetail

    @property
    def ConnectionId(self) -> str:
        return self._ConnectionId

    @ConnectionId.setter
    def ConnectionId(self, ConnectionId: str):
        self._ConnectionId = ConnectionId

    @property
    def Status(self) -> str:
        return self._Status

    @Status.setter
    def Status(self, Status: str):
        self._Status = Status

    def _deserialize(self,
                    params: typing.Dict[str, typing.Any]) -> None:
        self._ConnectionName = params.get("ConnectionName")
        self._DisplayName = params.get("DisplayName")
        self._ConnectionType = params.get("ConnectionType")
        self._DeployType = params.get("DeployType")
        self._AuthType = params.get("AuthType")
        self._ConnectionDetail = params.get("ConnectionDetail")
        self._ConnectionId = params.get("ConnectionId")
        self._Status = params.get("Status")
        member_set = set(params.keys())
        for name, value in vars(self).items():
            if name in member_set:
                member_set.remove(name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class ListConnectionsData(AbstractModel):
    def __init__(self) -> None:
        self._Items = None

    @property
    def Items(self) -> typing.List[ConnectionInfo]:
        return self._Items

    @Items.setter
    def Items(self, Items: typing.List[ConnectionInfo]):
        self._Items = Items

    def _deserialize(self,
                    params: typing.Dict[str, typing.Any]) -> None:
        if params.get("Items") is not None:
            self._Items = []
            for item in params.get("Items"):
                obj = ConnectionInfo()
                obj._deserialize(item)
                self._Items.append(obj)
        member_set = set(params.keys())
        for name, value in vars(self).items():
            if name in member_set:
                member_set.remove(name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))


class ListConnectionsResponse(AbstractModel):
    def __init__(self) -> None:
        self._Data = None
        self._RequestId = None

    @property
    def Data(self) -> ListConnectionsData:
        return self._Data

    @Data.setter
    def Data(self, Data: ListConnectionsData):
        self._Data = Data

    @property
    def RequestId(self) -> str:
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId: str):
        self._RequestId = RequestId

    def _deserialize(self,
                    params: typing.Dict[str, typing.Any]) -> None:
        if params.get("Data") is not None:
            self._Data = ListConnectionsData()
            self._Data._deserialize(params.get("Data"))
        self._RequestId = params.get("RequestId")
        member_set = set(params.keys())
        for name, value in vars(self).items():
            if name in member_set:
                member_set.remove(name)
        if len(member_set) > 0 and is_warning():
            warnings.warn("%s fields are useless." % ",".join(member_set))
