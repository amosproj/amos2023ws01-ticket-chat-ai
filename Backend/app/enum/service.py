from enum import Enum


class ServiceEnum(str, Enum):
    sap_erp = "SAP ERP"
    atlassian = "Atlassian"
    adobe = "Adobe"
    salesforce = "Salesforce"
    reporting = "Reporting"
    microsoft_power_platform = "Microsoft Power Platform"
    microsoft_sharepoint = "Microsoft SharePoint"
    snowflake = "Snowflake"
    microsoft_office = "Microsoft Office"
