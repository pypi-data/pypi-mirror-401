from datetime import datetime
from typing import Optional

import pandas as pd
import pandera as pa
from pandera.typing import Series

from brynq_sdk_functions import BrynQPanderaDataFrameModel


class WorkSchema(BrynQPanderaDataFrameModel):
    can_be_deleted: Series[pa.Bool] = pa.Field(coerce=True, description="Can Be Deleted", alias="canBeDeleted")
    work_change_type: Series[str] = pa.Field(coerce=True, description="Work Change Type", alias="workChangeType")
    creation_date: Series[datetime] = pa.Field(coerce=True, nullable=True, description="Creation Date", alias="creationDate")
    title: Series[str] = pa.Field(coerce=True, nullable=True, description="Title", alias="title")
    is_current: Series[pa.Bool] = pa.Field(coerce=True, description="Is Current", alias="isCurrent")
    modification_date: Series[datetime] = pa.Field(coerce=True, nullable=True, description="Modification Date", alias="modificationDate")
    site: Series[str] = pa.Field(coerce=True, nullable=True, description="Site", alias="site")
    site_id: Series[pd.Int64Dtype] = pa.Field(coerce=True, description="Site ID", alias="siteId")
    id: Series[pd.Int64Dtype] = pa.Field(coerce=True, description="ID", alias="id")
    end_effective_date: Series[datetime] = pa.Field(coerce=True, nullable=True, description="End Effective Date", alias="endEffectiveDate")
    active_effective_date: Series[datetime] = pa.Field(coerce=True, nullable=True, description="Active Effective Date", alias="activeEffectiveDate")
    department: Series[str] = pa.Field(coerce=True, nullable=True, description="Department", alias="department")
    effective_date: Series[datetime] = pa.Field(coerce=True, nullable=True, description="Effective Date", alias="effectiveDate")
    change_reason: Series[str] = pa.Field(coerce=True, nullable=True, description="Change Reason", alias="change.reason")
    change_changed_by: Series[str] = pa.Field(coerce=True, nullable=True, description="Change Changed By", alias="change.changedBy")
    change_changed_by_id: Series[str] = pa.Field(coerce=True, nullable=True, description="Change Changed By ID", alias="change.changedById")
    reports_to_id: Optional[Series[str]] = pa.Field(coerce=True, nullable=True, description="Reports To ID", alias="reportsTo.id")
    reports_to_first_name: Optional[Series[str]] = pa.Field(coerce=True, nullable=True, description="Reports To First Name", alias="reportsTo.firstName")
    reports_to_surname: Optional[Series[str]] = pa.Field(coerce=True, nullable=True, description="Reports To Surname", alias="reportsTo.surname")
    reports_to_email: Optional[Series[str]] = pa.Field(coerce=True, nullable=True, description="Reports To Email", alias="reportsTo.email")
    reports_to_display_name: Optional[Series[str]] = pa.Field(coerce=True, nullable=True, description="Reports To Display Name", alias="reportsTo.displayName")
    reports_to: Optional[Series[pd.Int64Dtype]] = pa.Field(coerce=True, nullable=True, description="Reports To", alias="reportsTo")
    employee_id: Series[str] = pa.Field(coerce=True, description="Employee ID", alias="employeeId")

    class Config:
        coerce = True
