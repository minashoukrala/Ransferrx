resource "azurerm_resource_group" "res-0" {
  location = "westus2"
  name     = "rg-ransferrx-prod"
}
resource "azurerm_key_vault" "res-1" {
  location            = "westus2"
  name                = "ransferrx-keyvault"
  resource_group_name = "rg-ransferrx-prod"
  sku_name            = "premium"
  tenant_id           = "07dd1dd1-3c75-439b-a01d-62eb70f28108"
  depends_on = [
    azurerm_resource_group.res-0
  ]
}
resource "azurerm_key_vault_secret" "res-2" {
  key_vault_id = azurerm_key_vault.res-1.id
  name         = "pharmacy-1"
  value        = "GTI3D,MDtp*#{r8}&-<H,mb-k=`t[;}^]ybD})nwOSwtVnKjj`{A@E0TFi5wcXC"
}
resource "azurerm_key_vault_secret" "res-3" {
  key_vault_id = azurerm_key_vault.res-1.id
  name         = "pharmacy-2"
  value        = "GTI3D,MDtp*#{r8}&-<H,mb-k=`t[;}^]ybD})nwOSwtVnKjj`{A@E0TFi5wcXC"
}
resource "azurerm_network_security_group" "res-4" {
  location            = "westus2"
  name                = "nsg-api-subnet"
  resource_group_name = "rg-ransferrx-prod"
  depends_on = [
    azurerm_resource_group.res-0
  ]
}
resource "azurerm_network_security_group" "res-5" {
  location            = "westus2"
  name                = "nsg-app-subnet"
  resource_group_name = "rg-ransferrx-prod"
  depends_on = [
    azurerm_resource_group.res-0
  ]
}
resource "azurerm_network_security_group" "res-6" {
  location            = "westus2"
  name                = "nsg-db-subnet"
  resource_group_name = "rg-ransferrx-prod"
  depends_on = [
    azurerm_resource_group.res-0
  ]
}
resource "azurerm_network_security_group" "res-7" {
  location            = "westus2"
  name                = "nsg-queue-subnet"
  resource_group_name = "rg-ransferrx-prod"
  depends_on = [
    azurerm_resource_group.res-0
  ]
}
resource "azurerm_private_dns_zone" "res-8" {
  name                = "privatelink.database.windows.net"
  resource_group_name = "rg-ransferrx-prod"
  depends_on = [
    azurerm_resource_group.res-0
  ]
}
resource "azurerm_private_dns_a_record" "res-9" {
  name                = "ransferrx-sql-primary"
  records             = ["10.0.2.4"]
  resource_group_name = "rg-ransferrx-prod"
  ttl                 = 3600
  zone_name           = "privatelink.database.windows.net"
  depends_on = [
    azurerm_private_dns_zone.res-8
  ]
}
resource "azurerm_private_dns_zone_virtual_network_link" "res-11" {
  name                  = "sqz5sn5mhw222"
  private_dns_zone_name = "privatelink.database.windows.net"
  resource_group_name   = "rg-ransferrx-prod"
  virtual_network_id    = azurerm_virtual_network.res-18.id
  depends_on = [
    azurerm_private_dns_zone.res-8
  ]
}
resource "azurerm_private_dns_zone" "res-12" {
  name                = "privatelink.queue.core.windows.net"
  resource_group_name = "rg-ransferrx-prod"
  depends_on = [
    azurerm_resource_group.res-0
  ]
}
resource "azurerm_private_dns_a_record" "res-13" {
  name                = "ransferrxqueue"
  records             = ["10.0.3.4"]
  resource_group_name = "rg-ransferrx-prod"
  ttl                 = 3600
  zone_name           = "privatelink.queue.core.windows.net"
  depends_on = [
    azurerm_private_dns_zone.res-12
  ]
}
resource "azurerm_private_dns_zone_virtual_network_link" "res-15" {
  name                  = "sqz5sn5mhw222"
  private_dns_zone_name = "privatelink.queue.core.windows.net"
  resource_group_name   = "rg-ransferrx-prod"
  virtual_network_id    = azurerm_virtual_network.res-18.id
  depends_on = [
    azurerm_private_dns_zone.res-12
  ]
}
resource "azurerm_private_endpoint" "res-16" {
  location            = "westus2"
  name                = "pe-ransferrx-queue"
  resource_group_name = "rg-ransferrx-prod"
  subnet_id           = "/subscriptions/6622e711-f53b-4b22-a83e-050e9f01d7a3/resourceGroups/rg-ransferrx-prod/providers/Microsoft.Network/virtualNetworks/ransferrx-vnet/subnets/queue-subnet"
  private_service_connection {
    is_manual_connection           = false
    name                           = "pe-ransferrx-queue_8411147f-882d-4327-90f6-6e41925120ed"
    private_connection_resource_id = "/subscriptions/6622e711-f53b-4b22-a83e-050e9f01d7a3/resourcegroups/rg-ransferrx-prod/providers/Microsoft.Storage/storageAccounts/ransferrxqueue"
    subresource_names              = ["queue"]
  }
  depends_on = [
    azurerm_resource_group.res-0
    # One of azurerm_subnet.res-27,azurerm_subnet_network_security_group_association.res-28 (can't auto-resolve as their ids are identical)
  ]
}
resource "azurerm_private_endpoint" "res-17" {
  location            = "westus2"
  name                = "ransferrx-sql-pe"
  resource_group_name = "rg-ransferrx-prod"
  subnet_id           = "/subscriptions/6622e711-f53b-4b22-a83e-050e9f01d7a3/resourceGroups/rg-ransferrx-prod/providers/Microsoft.Network/virtualNetworks/ransferrx-vnet/subnets/db-subnet"
  private_service_connection {
    is_manual_connection           = false
    name                           = "ransferrx-sql-pe"
    private_connection_resource_id = azurerm_mssql_server.res-665.id
    subresource_names              = ["SqlServer"]
  }
  depends_on = [
    # One of azurerm_subnet.res-23,azurerm_subnet_network_security_group_association.res-24 (can't auto-resolve as their ids are identical)
  ]
}
resource "azurerm_virtual_network" "res-18" {
  address_space       = ["10.0.0.0/16"]
  location            = "westus2"
  name                = "ransferrx-vnet"
  resource_group_name = "rg-ransferrx-prod"
  depends_on = [
    azurerm_resource_group.res-0
  ]
}
resource "azurerm_subnet" "res-19" {
  address_prefixes     = ["10.0.5.0/24"]
  name                 = "api-subnet"
  resource_group_name  = "rg-ransferrx-prod"
  virtual_network_name = "ransferrx-vnet"
  delegation {
    name = "delegation"
    service_delegation {
      actions = ["Microsoft.Network/virtualNetworks/subnets/action"]
      name    = "Microsoft.Web/serverFarms"
    }
  }
  depends_on = [
    azurerm_virtual_network.res-18
  ]
}
resource "azurerm_subnet_network_security_group_association" "res-20" {
  network_security_group_id = azurerm_network_security_group.res-4.id
  subnet_id                 = azurerm_subnet.res-19.id
}
resource "azurerm_subnet" "res-21" {
  address_prefixes     = ["10.0.1.0/24"]
  name                 = "app-subnet"
  resource_group_name  = "rg-ransferrx-prod"
  service_endpoints    = ["Microsoft.Storage"]
  virtual_network_name = "ransferrx-vnet"
  delegation {
    name = "delegation"
    service_delegation {
      actions = ["Microsoft.Network/virtualNetworks/subnets/action"]
      name    = "Microsoft.Web/serverFarms"
    }
  }
  depends_on = [
    azurerm_virtual_network.res-18
  ]
}
resource "azurerm_subnet_network_security_group_association" "res-22" {
  network_security_group_id = azurerm_network_security_group.res-5.id
  subnet_id                 = azurerm_subnet.res-21.id
}
resource "azurerm_subnet" "res-23" {
  address_prefixes     = ["10.0.2.0/24"]
  name                 = "db-subnet"
  resource_group_name  = "rg-ransferrx-prod"
  virtual_network_name = "ransferrx-vnet"
  depends_on = [
    azurerm_virtual_network.res-18
  ]
}
resource "azurerm_subnet_network_security_group_association" "res-24" {
  network_security_group_id = azurerm_network_security_group.res-6.id
  subnet_id                 = azurerm_subnet.res-23.id
}
resource "azurerm_subnet" "res-25" {
  address_prefixes     = ["10.0.0.0/24"]
  name                 = "default"
  resource_group_name  = "rg-ransferrx-prod"
  virtual_network_name = "ransferrx-vnet"
  depends_on = [
    azurerm_virtual_network.res-18
  ]
}
resource "azurerm_subnet" "res-26" {
  address_prefixes     = ["10.0.4.0/24"]
  name                 = "monitoring-subnet"
  resource_group_name  = "rg-ransferrx-prod"
  virtual_network_name = "ransferrx-vnet"
  depends_on = [
    azurerm_virtual_network.res-18
  ]
}
resource "azurerm_subnet" "res-27" {
  address_prefixes     = ["10.0.3.0/24"]
  name                 = "queue-subnet"
  resource_group_name  = "rg-ransferrx-prod"
  virtual_network_name = "ransferrx-vnet"
  depends_on = [
    azurerm_virtual_network.res-18
  ]
}
resource "azurerm_subnet_network_security_group_association" "res-28" {
  network_security_group_id = azurerm_network_security_group.res-7.id
  subnet_id                 = azurerm_subnet.res-27.id
}
resource "azurerm_log_analytics_workspace" "res-29" {
  location            = "westus2"
  name                = "ransferrx-law"
  resource_group_name = "rg-ransferrx-prod"
  depends_on = [
    azurerm_resource_group.res-0
  ]
}
resource "azurerm_log_analytics_saved_search" "res-30" {
  category                   = "General Exploration"
  display_name               = "All Computers with their most recent data"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_General|AlphabeticallySortedComputers"
  query                      = "search not(ObjectName == \"Advisor Metrics\" or ObjectName == \"ManagedSpace\") | summarize AggregatedValue = max(TimeGenerated) by Computer | limit 500000 | sort by Computer asc\r\n// Oql: NOT(ObjectName=\"Advisor Metrics\" OR ObjectName=ManagedSpace) | measure max(TimeGenerated) by Computer | top 500000 | Sort Computer // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PTT: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-31" {
  category                   = "General Exploration"
  display_name               = "Stale Computers (data older than 24 hours)"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_General|StaleComputers"
  query                      = "search not(ObjectName == \"Advisor Metrics\" or ObjectName == \"ManagedSpace\") | summarize lastdata = max(TimeGenerated) by Computer | limit 500000 | where lastdata < ago(24h)\r\n// Oql: NOT(ObjectName=\"Advisor Metrics\" OR ObjectName=ManagedSpace) | measure max(TimeGenerated) as lastdata by Computer | top 500000 | where lastdata < NOW-24HOURS // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PTT: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-32" {
  category                   = "General Exploration"
  display_name               = "Which Management Group is generating the most data points?"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_General|dataPointsPerManagementGroup"
  query                      = "search * | summarize AggregatedValue = count() by ManagementGroupName\r\n// Oql: * | Measure count() by ManagementGroupName // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PTT: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-33" {
  category                   = "General Exploration"
  display_name               = "Distribution of data Types"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_General|dataTypeDistribution"
  query                      = "search * | extend Type = $table | summarize AggregatedValue = count() by Type\r\n// Oql: * | Measure count() by Type // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PTT: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-34" {
  category                   = "Log Management"
  display_name               = "All Events"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|AllEvents"
  query                      = "Event | sort by TimeGenerated desc\r\n// Oql: Type=Event // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PTT: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-35" {
  category                   = "Log Management"
  display_name               = "All Syslogs"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|AllSyslog"
  query                      = "Syslog | sort by TimeGenerated desc\r\n// Oql: Type=Syslog // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PTT: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-36" {
  category                   = "Log Management"
  display_name               = "All Syslog Records grouped by Facility"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|AllSyslogByFacility"
  query                      = "Syslog | summarize AggregatedValue = count() by Facility\r\n// Oql: Type=Syslog | Measure count() by Facility // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PTT: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-37" {
  category                   = "Log Management"
  display_name               = "All Syslog Records grouped by ProcessName"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|AllSyslogByProcessName"
  query                      = "Syslog | summarize AggregatedValue = count() by ProcessName\r\n// Oql: Type=Syslog | Measure count() by ProcessName // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PTT: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-38" {
  category                   = "Log Management"
  display_name               = "All Syslog Records with Errors"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|AllSyslogsWithErrors"
  query                      = "Syslog | where SeverityLevel == \"error\" | sort by TimeGenerated desc\r\n// Oql: Type=Syslog SeverityLevel=error // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PTT: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-39" {
  category                   = "Log Management"
  display_name               = "Average HTTP Request time by Client IP Address"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|AverageHTTPRequestTimeByClientIPAddress"
  query                      = "search * | extend Type = $table | where Type == W3CIISLog | summarize AggregatedValue = avg(TimeTaken) by cIP\r\n// Oql: Type=W3CIISLog | Measure Avg(TimeTaken) by cIP // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PEF: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-40" {
  category                   = "Log Management"
  display_name               = "Average HTTP Request time by HTTP Method"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|AverageHTTPRequestTimeHTTPMethod"
  query                      = "search * | extend Type = $table | where Type == W3CIISLog | summarize AggregatedValue = avg(TimeTaken) by csMethod\r\n// Oql: Type=W3CIISLog | Measure Avg(TimeTaken) by csMethod // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PEF: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-41" {
  category                   = "Log Management"
  display_name               = "Count of IIS Log Entries by Client IP Address"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|CountIISLogEntriesClientIPAddress"
  query                      = "search * | extend Type = $table | where Type == W3CIISLog | summarize AggregatedValue = count() by cIP\r\n// Oql: Type=W3CIISLog | Measure count() by cIP // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PEF: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-42" {
  category                   = "Log Management"
  display_name               = "Count of IIS Log Entries by HTTP Request Method"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|CountIISLogEntriesHTTPRequestMethod"
  query                      = "search * | extend Type = $table | where Type == W3CIISLog | summarize AggregatedValue = count() by csMethod\r\n// Oql: Type=W3CIISLog | Measure count() by csMethod // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PEF: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-43" {
  category                   = "Log Management"
  display_name               = "Count of IIS Log Entries by HTTP User Agent"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|CountIISLogEntriesHTTPUserAgent"
  query                      = "search * | extend Type = $table | where Type == W3CIISLog | summarize AggregatedValue = count() by csUserAgent\r\n// Oql: Type=W3CIISLog | Measure count() by csUserAgent // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PEF: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-44" {
  category                   = "Log Management"
  display_name               = "Count of IIS Log Entries by Host requested by client"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|CountOfIISLogEntriesByHostRequestedByClient"
  query                      = "search * | extend Type = $table | where Type == W3CIISLog | summarize AggregatedValue = count() by csHost\r\n// Oql: Type=W3CIISLog | Measure count() by csHost // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PEF: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-45" {
  category                   = "Log Management"
  display_name               = "Count of IIS Log Entries by URL for the host \"www.contoso.com\" (replace with your own)"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|CountOfIISLogEntriesByURLForHost"
  query                      = "search csHost == \"www.contoso.com\" | extend Type = $table | where Type == W3CIISLog | summarize AggregatedValue = count() by csUriStem\r\n// Oql: Type=W3CIISLog csHost=\"www.contoso.com\" | Measure count() by csUriStem // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PEF: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-46" {
  category                   = "Log Management"
  display_name               = "Count of IIS Log Entries by URL requested by client (without query strings)"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|CountOfIISLogEntriesByURLRequestedByClient"
  query                      = "search * | extend Type = $table | where Type == W3CIISLog | summarize AggregatedValue = count() by csUriStem\r\n// Oql: Type=W3CIISLog | Measure count() by csUriStem // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PEF: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-47" {
  category                   = "Log Management"
  display_name               = "Count of Events with level \"Warning\" grouped by Event ID"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|CountOfWarningEvents"
  query                      = "Event | where EventLevelName == \"warning\" | summarize AggregatedValue = count() by EventID\r\n// Oql: Type=Event EventLevelName=warning | Measure count() by EventID // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PTT: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-48" {
  category                   = "Log Management"
  display_name               = "Shows breakdown of response codes"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|DisplayBreakdownRespondCodes"
  query                      = "search * | extend Type = $table | where Type == W3CIISLog | summarize AggregatedValue = count() by scStatus\r\n// Oql: Type=W3CIISLog | Measure count() by scStatus // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PEF: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-49" {
  category                   = "Log Management"
  display_name               = "Count of Events grouped by Event Log"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|EventsByEventLog"
  query                      = "Event | summarize AggregatedValue = count() by EventLog\r\n// Oql: Type=Event | Measure count() by EventLog // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PTT: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-50" {
  category                   = "Log Management"
  display_name               = "Count of Events grouped by Event Source"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|EventsByEventSource"
  query                      = "Event | summarize AggregatedValue = count() by Source\r\n// Oql: Type=Event | Measure count() by Source // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PTT: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-51" {
  category                   = "Log Management"
  display_name               = "Count of Events grouped by Event ID"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|EventsByEventsID"
  query                      = "Event | summarize AggregatedValue = count() by EventID\r\n// Oql: Type=Event | Measure count() by EventID // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PTT: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-52" {
  category                   = "Log Management"
  display_name               = "Events in the Operations Manager Event Log whose Event ID is in the range between 2000 and 3000"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|EventsInOMBetween2000to3000"
  query                      = "Event | where EventLog == \"Operations Manager\" and EventID >= 2000 and EventID <= 3000 | sort by TimeGenerated desc\r\n// Oql: Type=Event EventLog=\"Operations Manager\" EventID:[2000..3000] // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PTT: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-53" {
  category                   = "Log Management"
  display_name               = "Count of Events containing the word \"started\" grouped by EventID"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|EventsWithStartedinEventID"
  query                      = "search in (Event) \"started\" | summarize AggregatedValue = count() by EventID\r\n// Oql: Type=Event \"started\" | Measure count() by EventID // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PTT: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-54" {
  category                   = "Log Management"
  display_name               = "Find the maximum time taken for each page"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|FindMaximumTimeTakenForEachPage"
  query                      = "search * | extend Type = $table | where Type == W3CIISLog | summarize AggregatedValue = max(TimeTaken) by csUriStem\r\n// Oql: Type=W3CIISLog | Measure Max(TimeTaken) by csUriStem // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PEF: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-55" {
  category                   = "Log Management"
  display_name               = "IIS Log Entries for a specific client IP Address (replace with your own)"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|IISLogEntriesForClientIP"
  query                      = "search cIP == \"192.168.0.1\" | extend Type = $table | where Type == W3CIISLog | sort by TimeGenerated desc | project csUriStem, scBytes, csBytes, TimeTaken, scStatus\r\n// Oql: Type=W3CIISLog cIP=\"192.168.0.1\" | Select csUriStem,scBytes,csBytes,TimeTaken,scStatus // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PEF: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-56" {
  category                   = "Log Management"
  display_name               = "All IIS Log Entries"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|ListAllIISLogEntries"
  query                      = "search * | extend Type = $table | where Type == W3CIISLog | sort by TimeGenerated desc\r\n// Oql: Type=W3CIISLog // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PEF: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-57" {
  category                   = "Log Management"
  display_name               = "How many connections to Operations Manager's SDK service by day"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|NoOfConnectionsToOMSDKService"
  query                      = "Event | where EventID == 26328 and EventLog == \"Operations Manager\" | summarize AggregatedValue = count() by bin(TimeGenerated, 1d) | sort by TimeGenerated desc\r\n// Oql: Type=Event EventID=26328 EventLog=\"Operations Manager\" | Measure count() interval 1DAY // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PTT: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-58" {
  category                   = "Log Management"
  display_name               = "When did my servers initiate restart?"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|ServerRestartTime"
  query                      = "search in (Event) \"shutdown\" and EventLog == \"System\" and Source == \"User32\" and EventID == 1074 | sort by TimeGenerated desc | project TimeGenerated, Computer\r\n// Oql: shutdown Type=Event EventLog=System Source=User32 EventID=1074 | Select TimeGenerated,Computer // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PTT: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-59" {
  category                   = "Log Management"
  display_name               = "Shows which pages people are getting a 404 for"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|Show404PagesList"
  query                      = "search scStatus == 404 | extend Type = $table | where Type == W3CIISLog | summarize AggregatedValue = count() by csUriStem\r\n// Oql: Type=W3CIISLog scStatus=404 | Measure count() by csUriStem // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PEF: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-60" {
  category                   = "Log Management"
  display_name               = "Shows servers that are throwing internal server error"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|ShowServersThrowingInternalServerError"
  query                      = "search scStatus == 500 | extend Type = $table | where Type == W3CIISLog | summarize AggregatedValue = count() by sComputerName\r\n// Oql: Type=W3CIISLog scStatus=500 | Measure count() by sComputerName // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PEF: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-61" {
  category                   = "Log Management"
  display_name               = "Total Bytes received by each Azure Role Instance"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|TotalBytesReceivedByEachAzureRoleInstance"
  query                      = "search * | extend Type = $table | where Type == W3CIISLog | summarize AggregatedValue = sum(csBytes) by RoleInstance\r\n// Oql: Type=W3CIISLog | Measure Sum(csBytes) by RoleInstance // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PEF: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-62" {
  category                   = "Log Management"
  display_name               = "Total Bytes received by each IIS Computer"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|TotalBytesReceivedByEachIISComputer"
  query                      = "search * | extend Type = $table | where Type == W3CIISLog | summarize AggregatedValue = sum(csBytes) by Computer | limit 500000\r\n// Oql: Type=W3CIISLog | Measure Sum(csBytes) by Computer | top 500000 // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PEF: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-63" {
  category                   = "Log Management"
  display_name               = "Total Bytes responded back to clients by Client IP Address"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|TotalBytesRespondedToClientsByClientIPAddress"
  query                      = "search * | extend Type = $table | where Type == W3CIISLog | summarize AggregatedValue = sum(scBytes) by cIP\r\n// Oql: Type=W3CIISLog | Measure Sum(scBytes) by cIP // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PEF: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-64" {
  category                   = "Log Management"
  display_name               = "Total Bytes responded back to clients by each IIS ServerIP Address"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|TotalBytesRespondedToClientsByEachIISServerIPAddress"
  query                      = "search * | extend Type = $table | where Type == W3CIISLog | summarize AggregatedValue = sum(scBytes) by sIP\r\n// Oql: Type=W3CIISLog | Measure Sum(scBytes) by sIP // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PEF: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-65" {
  category                   = "Log Management"
  display_name               = "Total Bytes sent by Client IP Address"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|TotalBytesSentByClientIPAddress"
  query                      = "search * | extend Type = $table | where Type == W3CIISLog | summarize AggregatedValue = sum(csBytes) by cIP\r\n// Oql: Type=W3CIISLog | Measure Sum(csBytes) by cIP // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PEF: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-66" {
  category                   = "Log Management"
  display_name               = "All Events with level \"Warning\""
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|WarningEvents"
  query                      = "Event | where EventLevelName == \"warning\" | sort by TimeGenerated desc\r\n// Oql: Type=Event EventLevelName=warning // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PTT: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-67" {
  category                   = "Log Management"
  display_name               = "Windows Firewall Policy settings have changed"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|WindowsFireawallPolicySettingsChanged"
  query                      = "Event | where EventLog == \"Microsoft-Windows-Windows Firewall With Advanced Security/Firewall\" and EventID == 2008 | sort by TimeGenerated desc\r\n// Oql: Type=Event EventLog=\"Microsoft-Windows-Windows Firewall With Advanced Security/Firewall\" EventID=2008 // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PTT: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_log_analytics_saved_search" "res-68" {
  category                   = "Log Management"
  display_name               = "On which machines and how many times have Windows Firewall Policy settings changed"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.res-29.id
  name                       = "LogManagement(ransferrx-law)_LogManagement|WindowsFireawallPolicySettingsChangedByMachines"
  query                      = "Event | where EventLog == \"Microsoft-Windows-Windows Firewall With Advanced Security/Firewall\" and EventID == 2008 | summarize AggregatedValue = count() by Computer | limit 500000\r\n// Oql: Type=Event EventLog=\"Microsoft-Windows-Windows Firewall With Advanced Security/Firewall\" EventID=2008 | measure count() by Computer | top 500000 // Args: {OQ: True; WorkspaceId: 00000000-0000-0000-0000-000000000000} // Settings: {PTT: True; SortI: True; SortF: True} // Version: 0.1.122"
}
resource "azurerm_mssql_server" "res-665" {
  administrator_login           = "ransferdb"
  location                      = "westus2"
  name                          = "ransferrx-sql-primary"
  public_network_access_enabled = false
  resource_group_name           = "rg-ransferrx-prod"
  version                       = "12.0"
  depends_on = [
    azurerm_resource_group.res-0
  ]
}
resource "azurerm_mssql_database_extended_auditing_policy" "res-678" {
  database_id            = "/subscriptions/6622e711-f53b-4b22-a83e-050e9f01d7a3/resourceGroups/rg-ransferrx-prod/providers/Microsoft.Sql/servers/ransferrx-sql-primary/databases/master"
  enabled                = false
  log_monitoring_enabled = false
}
resource "azurerm_mssql_database" "res-684" {
  name                 = "ransferrx-db"
  server_id            = azurerm_mssql_server.res-665.id
  storage_account_type = "Zone"
}
resource "azurerm_mssql_database_extended_auditing_policy" "res-690" {
  database_id            = azurerm_mssql_database.res-684.id
  enabled                = false
  log_monitoring_enabled = false
}
resource "azurerm_mssql_server_microsoft_support_auditing_policy" "res-696" {
  enabled                = false
  log_monitoring_enabled = false
  server_id              = azurerm_mssql_server.res-665.id
}
resource "azurerm_mssql_server_transparent_data_encryption" "res-697" {
  server_id = azurerm_mssql_server.res-665.id
}
resource "azurerm_mssql_server_extended_auditing_policy" "res-698" {
  enabled                = false
  log_monitoring_enabled = false
  server_id              = azurerm_mssql_server.res-665.id
}
resource "azurerm_mssql_server_security_alert_policy" "res-701" {
  resource_group_name = "rg-ransferrx-prod"
  server_name         = "ransferrx-sql-primary"
  state               = "Disabled"
  depends_on = [
    azurerm_mssql_server.res-665
  ]
}
resource "azurerm_mssql_server_vulnerability_assessment" "res-703" {
  server_security_alert_policy_id = azurerm_mssql_server_security_alert_policy.res-701.id
  storage_container_path          = ""
}
resource "azurerm_storage_account" "res-704" {
  account_replication_type        = "ZRS"
  account_tier                    = "Standard"
  allow_nested_items_to_be_public = false
  location                        = "westus2"
  name                            = "ransferrxlogarchive"
  resource_group_name             = "rg-ransferrx-prod"
  depends_on = [
    azurerm_resource_group.res-0
  ]
}
resource "azurerm_storage_container" "res-706" {
  name               = "insights-logs-appserviceantivirusscanauditlogs"
  storage_account_id = "/subscriptions/6622e711-f53b-4b22-a83e-050e9f01d7a3/resourceGroups/rg-ransferrx-prod/providers/Microsoft.Storage/storageAccounts/ransferrxlogarchive"
  depends_on = [
    # One of azurerm_storage_account.res-704,azurerm_storage_account_queue_properties.res-716 (can't auto-resolve as their ids are identical)
  ]
}
resource "azurerm_storage_container" "res-707" {
  name               = "insights-logs-appserviceconsolelogs"
  storage_account_id = "/subscriptions/6622e711-f53b-4b22-a83e-050e9f01d7a3/resourceGroups/rg-ransferrx-prod/providers/Microsoft.Storage/storageAccounts/ransferrxlogarchive"
  depends_on = [
    # One of azurerm_storage_account.res-704,azurerm_storage_account_queue_properties.res-716 (can't auto-resolve as their ids are identical)
  ]
}
resource "azurerm_storage_container" "res-708" {
  name               = "insights-logs-appservicefileauditlogs"
  storage_account_id = "/subscriptions/6622e711-f53b-4b22-a83e-050e9f01d7a3/resourceGroups/rg-ransferrx-prod/providers/Microsoft.Storage/storageAccounts/ransferrxlogarchive"
  depends_on = [
    # One of azurerm_storage_account.res-704,azurerm_storage_account_queue_properties.res-716 (can't auto-resolve as their ids are identical)
  ]
}
resource "azurerm_storage_container" "res-709" {
  name               = "insights-logs-appservicehttplogs"
  storage_account_id = "/subscriptions/6622e711-f53b-4b22-a83e-050e9f01d7a3/resourceGroups/rg-ransferrx-prod/providers/Microsoft.Storage/storageAccounts/ransferrxlogarchive"
  depends_on = [
    # One of azurerm_storage_account.res-704,azurerm_storage_account_queue_properties.res-716 (can't auto-resolve as their ids are identical)
  ]
}
resource "azurerm_storage_container" "res-710" {
  name               = "insights-logs-appserviceplatformlogs"
  storage_account_id = "/subscriptions/6622e711-f53b-4b22-a83e-050e9f01d7a3/resourceGroups/rg-ransferrx-prod/providers/Microsoft.Storage/storageAccounts/ransferrxlogarchive"
  depends_on = [
    # One of azurerm_storage_account.res-704,azurerm_storage_account_queue_properties.res-716 (can't auto-resolve as their ids are identical)
  ]
}
resource "azurerm_storage_container" "res-711" {
  name               = "insights-logs-functionapplogs"
  storage_account_id = "/subscriptions/6622e711-f53b-4b22-a83e-050e9f01d7a3/resourceGroups/rg-ransferrx-prod/providers/Microsoft.Storage/storageAccounts/ransferrxlogarchive"
  depends_on = [
    # One of azurerm_storage_account.res-704,azurerm_storage_account_queue_properties.res-716 (can't auto-resolve as their ids are identical)
  ]
}
resource "azurerm_storage_container" "res-712" {
  name               = "insights-logs-storagedelete"
  storage_account_id = "/subscriptions/6622e711-f53b-4b22-a83e-050e9f01d7a3/resourceGroups/rg-ransferrx-prod/providers/Microsoft.Storage/storageAccounts/ransferrxlogarchive"
  depends_on = [
    # One of azurerm_storage_account.res-704,azurerm_storage_account_queue_properties.res-716 (can't auto-resolve as their ids are identical)
  ]
}
resource "azurerm_storage_container" "res-713" {
  name               = "insights-logs-storageread"
  storage_account_id = "/subscriptions/6622e711-f53b-4b22-a83e-050e9f01d7a3/resourceGroups/rg-ransferrx-prod/providers/Microsoft.Storage/storageAccounts/ransferrxlogarchive"
  depends_on = [
    # One of azurerm_storage_account.res-704,azurerm_storage_account_queue_properties.res-716 (can't auto-resolve as their ids are identical)
  ]
}
resource "azurerm_storage_container" "res-714" {
  name               = "insights-metrics-pt1m"
  storage_account_id = "/subscriptions/6622e711-f53b-4b22-a83e-050e9f01d7a3/resourceGroups/rg-ransferrx-prod/providers/Microsoft.Storage/storageAccounts/ransferrxlogarchive"
  depends_on = [
    # One of azurerm_storage_account.res-704,azurerm_storage_account_queue_properties.res-716 (can't auto-resolve as their ids are identical)
  ]
}
resource "azurerm_storage_account_queue_properties" "res-716" {
  storage_account_id = azurerm_storage_account.res-704.id
  hour_metrics {
    version = "1.0"
  }
  logging {
    delete  = false
    read    = false
    version = "1.0"
    write   = false
  }
  minute_metrics {
    version = "1.0"
  }
}
resource "azurerm_storage_account" "res-718" {
  account_replication_type          = "ZRS"
  account_tier                      = "Standard"
  allow_nested_items_to_be_public   = false
  infrastructure_encryption_enabled = true
  location                          = "westus2"
  name                              = "ransferrxqueue"
  queue_encryption_key_type         = "Account"
  resource_group_name               = "rg-ransferrx-prod"
  table_encryption_key_type         = "Account"
  depends_on = [
    azurerm_resource_group.res-0
  ]
}
resource "azurerm_storage_account_queue_properties" "res-722" {
  storage_account_id = azurerm_storage_account.res-718.id
  hour_metrics {
    version = "1.0"
  }
  logging {
    delete  = false
    read    = false
    version = "1.0"
    write   = false
  }
  minute_metrics {
    version = "1.0"
  }
}
resource "azurerm_storage_queue" "res-723" {
  name                 = "prescription-retry-queue"
  storage_account_name = "ransferrxqueue"
  depends_on = [
    azurerm_storage_account_queue_properties.res-722
  ]
}
resource "azurerm_storage_account" "res-725" {
  account_replication_type        = "LRS"
  account_tier                    = "Standard"
  allow_nested_items_to_be_public = false
  default_to_oauth_authentication = true
  location                        = "westus2"
  name                            = "rgransferrxprodb884"
  resource_group_name             = "rg-ransferrx-prod"
  depends_on = [
    azurerm_resource_group.res-0
  ]
}
resource "azurerm_storage_container" "res-727" {
  name               = "azure-webjobs-hosts"
  storage_account_id = "/subscriptions/6622e711-f53b-4b22-a83e-050e9f01d7a3/resourceGroups/rg-ransferrx-prod/providers/Microsoft.Storage/storageAccounts/rgransferrxprodb884"
  depends_on = [
    # One of azurerm_storage_account.res-725,azurerm_storage_account_queue_properties.res-731 (can't auto-resolve as their ids are identical)
  ]
}
resource "azurerm_storage_container" "res-728" {
  name               = "azure-webjobs-secrets"
  storage_account_id = "/subscriptions/6622e711-f53b-4b22-a83e-050e9f01d7a3/resourceGroups/rg-ransferrx-prod/providers/Microsoft.Storage/storageAccounts/rgransferrxprodb884"
  depends_on = [
    # One of azurerm_storage_account.res-725,azurerm_storage_account_queue_properties.res-731 (can't auto-resolve as their ids are identical)
  ]
}
resource "azurerm_storage_share" "res-730" {
  name               = "ransferrx-retry-handler84fd"
  quota              = 102400
  storage_account_id = "/subscriptions/6622e711-f53b-4b22-a83e-050e9f01d7a3/resourceGroups/rg-ransferrx-prod/providers/Microsoft.Storage/storageAccounts/rgransferrxprodb884"
  depends_on = [
    # One of azurerm_storage_account.res-725,azurerm_storage_account_queue_properties.res-731 (can't auto-resolve as their ids are identical)
  ]
}
resource "azurerm_storage_account_queue_properties" "res-731" {
  storage_account_id = azurerm_storage_account.res-725.id
  hour_metrics {
    version = "1.0"
  }
  logging {
    delete  = false
    read    = false
    version = "1.0"
    write   = false
  }
  minute_metrics {
    version = "1.0"
  }
}
resource "azurerm_storage_table" "res-733" {
  name                 = "AzureFunctionsDiagnosticEvents202507"
  storage_account_name = "rgransferrxprodb884"
}
resource "azurerm_service_plan" "res-734" {
  location            = "westus2"
  name                = "ASP-rgransferrxprod-9b65"
  os_type             = "Linux"
  resource_group_name = "rg-ransferrx-prod"
  sku_name            = "EP1"
  depends_on = [
    azurerm_resource_group.res-0
  ]
}
resource "azurerm_service_plan" "res-735" {
  location            = "westus2"
  name                = "ransferrx-func-plan"
  os_type             = "Linux"
  resource_group_name = "rg-ransferrx-prod"
  sku_name            = "P1v3"
  depends_on = [
    azurerm_resource_group.res-0
  ]
}
resource "azurerm_linux_function_app" "res-736" {
  builtin_logging_enabled                  = false
  client_certificate_mode                  = "Required"
  ftp_publish_basic_authentication_enabled = false
  https_only                               = true
  location                                 = "westus2"
  name                                     = "ransferrx-retry-handler"
  resource_group_name                      = "rg-ransferrx-prod"
  service_plan_id                          = azurerm_service_plan.res-734.id
  storage_account_access_key               = "[REDACTED - Storage Account Access Key]="
  storage_account_name                     = "rgransferrxprodb884"
  tags = {
    "hidden-link: /app-insights-resource-id" = azurerm_application_insights.res-743.id
  }
  virtual_network_subnet_id                      = "/subscriptions/6622e711-f53b-4b22-a83e-050e9f01d7a3/resourceGroups/rg-ransferrx-prod/providers/Microsoft.Network/virtualNetworks/ransferrx-vnet/subnets/app-subnet"
  webdeploy_publish_basic_authentication_enabled = false
  site_config {
    application_insights_connection_string = "InstrumentationKey=abdcab09-096d-4202-b54e-320687ed434c;IngestionEndpoint=https://westus2-2.in.applicationinsights.azure.com/;LiveEndpoint=https://westus2.livediagnostics.monitor.azure.com/;ApplicationId=6077a2ff-a3ce-4292-ad96-f99497c23ac6"
    ftps_state                             = "FtpsOnly"
    ip_restriction_default_action          = ""
    scm_ip_restriction_default_action      = ""
    vnet_route_all_enabled                 = true
    application_stack {
      python_version = "3.11"
    }
    cors {
      allowed_origins = ["https://portal.azure.com"]
    }
  }
  depends_on = [
    # One of azurerm_subnet.res-21,azurerm_subnet_network_security_group_association.res-22 (can't auto-resolve as their ids are identical)
  ]
}
resource "azurerm_app_service_custom_hostname_binding" "res-740" {
  app_service_name    = "ransferrx-retry-handler"
  hostname            = "ransferrx-retry-handler.azurewebsites.net"
  resource_group_name = "rg-ransferrx-prod"
  depends_on = [
    azurerm_linux_function_app.res-736
  ]
}
resource "azurerm_monitor_action_group" "res-741" {
  name                = "Application Insights Smart Detection"
  resource_group_name = "rg-ransferrx-prod"
  short_name          = "SmartDetect"
  arm_role_receiver {
    name                    = "Monitoring Contributor"
    role_id                 = "749f88d5-cbae-40b8-bcfc-e573ddc772fa"
    use_common_alert_schema = true
  }
  arm_role_receiver {
    name                    = "Monitoring Reader"
    role_id                 = "43d0d8ad-25c7-4714-9337-8ba259a9fe05"
    use_common_alert_schema = true
  }
  depends_on = [
    azurerm_resource_group.res-0
  ]
}
resource "azurerm_application_insights" "res-742" {
  application_type    = "web"
  location            = "westus2"
  name                = "ransferrx-api"
  resource_group_name = "rg-ransferrx-prod"
  sampling_percentage = 0
  depends_on = [
    azurerm_resource_group.res-0
  ]
}
resource "azurerm_application_insights" "res-743" {
  application_type    = "web"
  location            = "westus2"
  name                = "ransferrx-retry-handler"
  resource_group_name = "rg-ransferrx-prod"
  sampling_percentage = 0
  depends_on = [
    azurerm_resource_group.res-0
  ]
}
